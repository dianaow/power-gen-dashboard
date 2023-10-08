import os
from flask import Flask, send_from_directory, request
from flask_cors import CORS
from dotenv import load_dotenv
import requests
import json
import pandas as pd
import numpy as np

load_dotenv()

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get('API_KEY')

def fix_outliers_missing_values(df):
  outliers = []
  for col in df:
    try:
      if(len(df[col].unique()) > len(df[col])/2):
        # Outliers are deemed to be outside the 10th and 90th percentile
        Q1 = np.percentile(df[col], 10, method='midpoint')
        Q3 = np.percentile(df[col], 90, method='midpoint')
        IQR = Q3 - Q1
        lower = Q1 - 1.5*IQR
        upper = Q3 + 1.5*IQR
        # Find the outliers based on index in dataframe
        upper_array = np.where(df[col]>=upper)[0] 
        lower_array = np.where(df[col]<=lower)[0]
        outliers.extend(upper_array)
        outliers.extend(lower_array)
    except:
      continue

  # Removing the outliers
  #print(outliers)
  df_copy = df.copy()
  df_copy.drop(index=outliers, inplace=True)
  
  # Replace all missing values with 0 (countries are missing large chunks of values for certain fuel sources only, suggesting that the country does not utilize these as fuel sources)
  #print(df.isnull().sum())
  df_copy = df_copy.fillna(0)

  return df_copy
  
def aggregate_by(df):
  # Convert 'date_id' column to datetime type and as index before resampling
  df['date_id'] = pd.to_datetime(df['date_id'])
  df.set_index('date_id', inplace=True)

  # Resample the dataFrame for each 'region' separately
  agg_hourly_dfs = {}
  agg_daily_dfs = {}
  agg_monthly_dfs = {}
  agg_hourly_percs_dfs = {}
  agg_daily_percs_dfs = {}
  agg_monthly_percs_dfs = {}

  for region, group_df in df.groupby('region'):
      agg_daily_df = group_df.resample('D').sum().reset_index()  # Resample by month and calculate the sum
      agg_daily_df['region'] = region
      agg_daily_dfs[region] = agg_daily_df

      agg_daily_df1 = agg_daily_df.copy()
      agg_daily_df1['sum'] = agg_daily_df1.iloc[:, 3:].sum(axis=1)
      agg_daily_percs_df = agg_daily_df1.iloc[:, 3:].divide(agg_daily_df1['sum'], axis='index').drop(columns=['sum'])
      agg_daily_percs_df['date_id'] = agg_daily_df1.iloc[:, 0]
      agg_daily_percs_df['region'] = region
      agg_daily_percs_dfs[region] = agg_daily_percs_df

      agg_monthly_df = group_df.resample('M').sum().reset_index()  # Resample by day and calculate the sum
      agg_monthly_df['region'] = region
      agg_monthly_dfs[region] = agg_monthly_df

      agg_hourly_df = group_df.resample('60min').sum().reset_index()  # Resample by hourly and calculate the sum
      agg_hourly_df['region'] = region
      agg_hourly_dfs[region] = agg_hourly_df
      
  # Combine the resampled dataFrames into a single dataFrame
  return {
     'daily': pd.concat(agg_daily_dfs, axis=0).to_json(orient='records'), 
     'monthly':  pd.concat(agg_monthly_dfs, axis=0).to_json(orient='records'),
     'perc_daily': pd.concat(agg_daily_percs_dfs, axis=0).to_json(orient='records'), 
    }

def categorize_value(value):
  renewables = ['Wind onshore', 'Natural Gas', 'Biomass', 'Wind offshore', 'Nuclear', 'Solar', 'Run-of-River Hydro', 'Pumped storage generation', 'Other renewables', 'Dam Hydro', 'Geothermal']
  non_renewables = ['Lignite', 'Hard Coal', 'Other fossil fuel', 'Oil']
  if value in renewables:
      return 'renewable'
  elif value in non_renewables:
      return 'non-renewable'
  else:
      return 'uncategorized'

@app.route('/')
def root():
    return send_from_directory('../client/dist', 'index.html')

# Path for the rest of the static files (JS/CSS)
@app.route('/<path:path>')
def assets(path):
    return send_from_directory('../client/dist', path)

@app.route('/data', methods=['GET'])
def get_data():
    from_date = request.args.get('from')
    to_date = request.args.get('to')
    print(from_date, to_date)
    parameters = {
        "from": from_date if from_date else "2022-10-01", 
        "to": to_date if to_date else "2022-12-31",
        "dataset": "task_generation_h"
    }
    response = requests.get("https://api.agora-energy.org/publicdata/api?", headers={"api-key" : API_KEY}, params=parameters)

    if response.status_code == 200:
      print("Request successful")
      response_json = json.loads(response.text)
      df = pd.DataFrame(response_json['data'], columns=response_json['columns'])
      df['value_Gwh'] = df['value'] / 1000 # change MwH to GwH
      df['category'] = df['generation'].apply(categorize_value) # categorize fuel sources into renewables and non-renewables

      pivot_df = df.pivot(index=['date_id', 'region'], columns='generation', values='value_Gwh')
      pivot_df.reset_index(inplace=True) # reset the index to make 'date_id' the index 
      df_processed = fix_outliers_missing_values(pivot_df)
      data_json = aggregate_by(df_processed)

      pivot_df_cat = df.pivot_table(index=['date_id', 'region'], columns='category', values='value_Gwh', aggfunc='sum')
      pivot_df_cat.reset_index(inplace=True) # reset the index to make 'date_id' the index 
      df_processed_cat = fix_outliers_missing_values(pivot_df_cat)
      data_json_cat = aggregate_by(df_processed_cat)

      return {"type": data_json, "categorized": data_json_cat}
    else:
      # handle errors here
      print("Request failed with status code:", response.status_code)
      return {'data': []}

server = app.server

if __name__ == '__main__':
    app.run(debug=True)
