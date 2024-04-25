# A web application to visualize power generation for different fuel sources 

**Technologies: Python and Flask for the backend API, JavaScript and Svelte for the UI**

The dataset comprises power generation data categorized by type of fuel and provided on an hourly basis for four European countries: Germany, Austria, Denmark, and France.

I explored and wrangled the data in Python so that it can be in the correct structure to render easily as a stacked area chart with D3.js on the frontend (Svelte). I calculated the aggregated daily generation for each type of fuel and stored the results. I also categorized the fuel sources into renewables and non-renewables and then calculated aggregated daily and monthly electricity generation from these two categories. An API route is set up in Flask to transmit these datasets to the frontend.

A stacked area chart is chosen to represent the daily data to make it easy to compare the relative proportions of different fuel sources at any given point in time. The height of each stack represents the total for that day, and the segments within the stack show the contribution of each fuel source to the total. 

A dropdown menu allows the user to select different countries from the dataset. When the user selects a country, both charts update automatically to reflect the selected country's power generation data.

<br> 

#### Stacked area chart with tooltips created with D3.js
![Stacked area chart with tooltips created with D3.js](https://github.com/dianaow/power-gen-dashboard/blob/main/ui_snapshot_1.png)

<br> 

#### Aggregated daily electricity generation from fuel sources (%)
![Aggregated daily electricity generation from fuel sources (%)](https://github.com/dianaow/power-gen-dashboard/blob/main/ui_snapshot_2.png)

<br> 

#### Interactivity: Click on a legend item to highlight the fuel source
![Interactivity: Click on a legend item to highlight the fuel source](https://github.com/dianaow/power-gen-dashboard/blob/main/ui_snapshot_3.png)

### Backend: Flask
1. Navigate to the server folder. Create a Python virtual environment where the dependencies for this project will be installed.
```
cd server
python3 -m venv venv
```

2. Activate the environment and install all the packages available in the requirement.txt file.
```
source venv/bin/activate
pip install -r ./requirements.txt
```

3. If a  `.env` file is not present in the server folder, create one to store the private API key, which is required to extract data from the API
```
  API_KEY=XXXXXXXXXX
```

4. Run the server
```
flask run -h localhost -p 3000
```

### Frontend: Svelte
1. Open a new terminal tab and navigate to the client folder. Install the dependencies
```
cd client
npm install
```

2. Run the command below to build the app and have the Vite build tool watch for changes
```
npm run autobuild
```

3. View the app on `http://localhost:3000/`

Note: I have decided not to name the backend and front end files separately with the naming convention specified in the document, because of the interconnectedness of the two.
