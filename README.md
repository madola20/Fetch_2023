# Fetch_2023
receipt_processor

Donna Madeline Laurance
Code Excercise for Backend Engineering Apprenticeship 


This application requires Docker to run and a web browser to interact with.


First, pull the repository from github to your local machine and make Fetch_23 your current directory. 
Then, build the the container by using the following command: 
docker build . -t python-flask:latest

Next, run the docker container with the following command: 
docker run -p 5000:5000 python-flask:latest

The port and forwarded port must be specified, otherwise the webservice will only be available from within the docker container.

Running docker will start the application. You will then need to open a web browser and enter in the following address: 
http://127.0.0.1:5000/receipts/process

This will read JSON from http://127.0.0.1:5000/json_test and return a JSON key value pair. 

    NOTE: 
    The file from app.py can be edited to process different receipts, starting at line 23. Replace the JSON in the parenthesis and rebuild the docker container. 
    
    Another method would be to edit line 144: 
    
    request = requests.get(baseurl + "json_test").json()
    
    to
    
    request = requests.get("{x}").json()
    
    where {x} is the URL of the receipt resource
    
    The docker container will need to be rebuilt in this case as well.

Finally, copy the address below into your web browser and replace the text "{x}" with the id value returned from the above route to determine the points awarded. 
http://127.0.0.1:5000/{x}/points

For example:
-> http://127.0.0.1:5000/receipts/process returns: {"id":"f66d345d-602c-f5d9-e3fa-b4590328c586"} 
-> So http://127.0.0.1:5000/f66d345d-602c-f5d9-e3fa-b4590328c586/points will return the key-value pair of the points awarded.

