# README

This is template project for a school project.

## How to setup

## 1. Clone the repository

        git clone https://github.com/Papiermond/RPM.git
        oder
        gh repo clone Papiermond/RPM

## 2. Install dependencies

- Python3

- Nodejs (for npm and frontend)

        python3 -m venv Venv

        ./Venv/bin/activate
        alertentivly:
          source .Venv/bin/activate

        pip install --upgrade pip

        pip install -r requirements.txt

  #npm could need Sudo or admin privlages to run correctly

        npm install -g @vue/cli

        npm install -save-dev fontend/package.json

## 3. Run the project

- Start the backend server

        cd backend
        python3 app.py

- Start the frontend server

        cd frontend
        npm run serve

## 4. Access the application

Open your web browser and navigate to `http://localhost:8080` to access the application.

## 5. Stop the servers

To stop the servers, you can use `Ctrl+C` in the terminal where the servers are running.

## 6. Additional Information

- The backend server runs on port 5000 by default.
- The frontend server runs on port 8080 by default.
- Make sure to have the necessary permissions to run the servers.

## 7. Troubleshooting

If you encounter any issues, please check the following:

- Ensure that all dependencies are installed correctly.
- Check the terminal for any error messages.
- Make sure the servers are running on the correct ports.
