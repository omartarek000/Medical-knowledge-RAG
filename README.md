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
uvicorn main:app --reload --host -- port 8000
```
this will run the app on localhost port 8000 you can change the port to any port you like also you can change localhost to 0.0.0.0 to make it accessible from other devices on the same network and -- reload is used to reload the app automatically when you make changes to the code to make sure everything is working you can access the following endpoint 
you can just use 
```bash
uvicorn main:app
```
# testing the app
to test the apis you can use pytest and use the file test_api.py to test the apis as you would create more apis you can add more tests to the test_api.py file to test the new apis
to run the tests use the following command
```bash
pytest
```