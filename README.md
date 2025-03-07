# FinQuery -  UK Banking Products Assistant

## Installation Guide:
- The Front-end, Back-end, and Database all need to be running at the same time for the application to function correctly.

## Front-end Setup (React.js):
- 1. Install dependencies
`npm i`
- 2. Start the development server
`npm run dev`
- 3. Open the application in your browser at
`http://localhost:5173/`
- Get the Groq key through the link and save it in the front-end chat

## Back-end Setup (Python):
- 1. Create a virtual environment
`python -m venv venv`
- 2. Activate it
`.\venv\Scripts\activate`
- 3. Install Python dependencies
`pip install -r requirements.txt`
- 4. Run the FastAPI server
`uvicorn main:app --reload`


## Database Setup:
- 1. Make sure you have Docker installed
- 2. Download the .tar file
- 3. Load the .tar image into docker
`docker load -i arangodb.tar`
- 4. Double Check the image docker file name and then run it
`docker run -d -p 8529:8529 --name arangodb-container arangodb`
- 5. Default Database Credentials are:
username: root
password: openSesame


