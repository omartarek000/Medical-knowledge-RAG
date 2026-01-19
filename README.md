# Medical RAG 
this is an implemneation of RAG archiecutre for answering questions related to the medical field 

# Requirments
python 3.8 or above the version used was 3.12.3 using WSL on windows or using linux 
natively is completly up to you i prefer linux at this point as it is easier in some cases

to create a virtual enviroment use the following command 
```bash
python -m venv venv
```
the second venv is the name of the virtual enviroment you can change it to any name you like
to activate the virtual enviroment use the following command 
```bash
source venv/bin/activate
```
on windows use the following command
```bash
venv\Scripts\activate
```
after activating the virtual enviroment you need to install the requirments using the following command 
```bash
pip install -r requirements.txt
```
# running the app 
if you want to run the app use the following  command 
```bash
uvicorn src.app.main:app --reload --host 0.0.0.0 --port 5000
```
this will run the app on localhost port 8000 you can change the port to any port you like also you can change localhost to `0.0.0.0` to make it accessible from other devices on the same network  `remove it to run the app in development ` and -- reload is used to reload the app automatically when you make changes to the code to make sure everything is working you can access the following endpoint 
you can just use 
```bash
uvicorn src.app.main:app
```
# testing the app
to test the apis you can use pytest and use the file test_api.py to test the apis as you would create more apis you can add more tests to the test_api.py file to test the new apis
to run the tests use the following command
```bash
pytest
```

# docker and MongoDB
in order to store the chunks we generated from the documents we need to store it in a database
beacuse of this we need to use mongoDB , just you need to famalirize yourself just a bit with docker and docker-compose 
first thing you need is to install docker 
this is the docker url

[Docker Desktop for windows](https://www.docker.com/products/docker-desktop/)

[how to install docker on linux ](https://docs.docker.com/desktop/setup/install/linux/)

afer verifying that docker works on your system go the directory where the docker file presents 
```bash
cd docker , docker compose up --watch
```
[a quick guide on docker compose](https://docs.docker.com/compose/gettingstarted/) and what the commands mean 

your mongodb will be running on port 27017 we can download  studio 3t to view your database
[studio 3t ](https://studio3t.com/download/)
