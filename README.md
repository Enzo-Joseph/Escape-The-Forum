# Escape-The-Forum
An escape game dashboard for an academic project

For an academic project, we realized an escape game and a dashboard to vizualize data from it. 
This repository contains the dashboard (frontend and backend)

# Run the dashboard locally
To run the dashboard locally, first install Node and Python depedencies. 
For that, open a command prompt in this directory and run the following commands :

```npm install```
```pip install -r requirements.txt```

Then, double click on the run.py file and go to the link http://localhost:5173/
Voila !

# How it works
When opening run.py, it runs the ```server/app.py``` file and the command ```npm run dev``` from the folder ```/client/```
The first file with fetch the data from google sheets by using ```server/connect_gsheet.py``` functions. From that, an application is created with Flask in order to send the data to the web application.
The second command creates the application created the web application locally.

# How we did it
The backend is only build in python, using flask, gspread and basic python modules for data analysis.
For the frontend, we used the Javascript framework Vue.js. 