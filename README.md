# A web application to visualize power generation for different fuel sources 

Using Python and Flask for the backend API, JavaScript and Svelte for the UI

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
