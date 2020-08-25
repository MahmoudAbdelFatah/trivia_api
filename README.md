# Trivia API
This is a Trivia API app, The second project of Advanced Web Development Nanodegree Program.

## Getting Setup

This app is composed of two parts:
1. The frontend
2. The backend


## frontend
> _tip_: this frontend is designed to work with [Flask-based Backend](../backend). It is recommended you stand up the backend first, test using Postman or curl, update the endpoints in the frontend, and then the frontend should integrate smoothly.

### Installing Dependencies

#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

>_tip_: **npm i** is shorthand for **npm install**

## Required Tasks

## Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

## Request Formatting

The frontend should be fairly straightforward and disgestible. You'll primarily work within the ```components``` folder in order to edit the endpoints utilized by the components. While working on your backend request handling and response formatting, you can reference the frontend to view how it parses the responses. 

After you complete your endpoints, ensure you return to and update the frontend to make request and handle responses appropriately: 
- Correct endpoints
- Update response body handling 

## backend

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

``` Windows
$env:FLASK_APP="flaskr"
$env:FLASK_ENV="development"
flask run

```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 




### The Website

#### List of questions
 The main webpage will show the user a list of categories and the related questions. If no 
 category was selected, the list will show all the questions in difficulty order. 

#### Questions
 Each item will display the question, the difficulty, an icon related to the category and
 a button to show the answer to that question. 

#### Add
 In this page, the user can add new questions. 

#### Play
 This is a small quizz game. A user can select a topic and the game will start. 
 The quizz will consist of 5 questions related to the category select. 
 If "All" was selected, the questions can be from any category. 

 The game won't show the same question during the quizz and the questions will come in 
 random order. 


### Getting Started

## API Reference


- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.

- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False,
    "eror": 404,
    "message": "Resource Not Found"
}
```

```
{
    "success": False,
    "eror": 422,
    "message": "Not Processable"
}
```

The API will return two error types when requests fail:
 - 404: Resource Not Found
 - 422: Not Processable

### Endpoint Library

#### GET /questions

1. General

    1. Returns a list of question objects, success value, and total number of questions
    2. Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
    
2. ```bash
curl http://127.0.0.1/5000/questions
```
```
{
    "success": true,
    "status": 200,
    "questions": [
        {
        "answer": "answer1",
        "category": "2",
        "difficulty": 1,
        "id": 1,
        "question": "question1?"
        }
    ],
    "total_questions": 1,
    "current_category": "",
    "categories": ["cat1" , "cat2"]     
}
```

#### POST /questions

1. General

    1. This endpoint will search questions when seding a JSON object contains a "searchTerm". If there are not questions, the returned object will contains an empty "questions" list.
    2. Creates a new questions using the submitted question, answer, category, difficulty. 

2. ```bash 
curl http://127.0.0.1/5000/questions -X POST -H "Content-type: application/json" -d '{
    "question" = "question1?",
    "answer" = "answer1",
    "category" = "1",
    "difficulty" = "1"
}'
```

#### Delete /questions/{question_id}

1. General: Deletes the questions of the given ID if it exists. Return the id of the deleted question and a success value. 

2. ```bash 
curl -X DELETE http://127.0.0.1:5000/questions/1 
```


#### Get /categories

1. General: This endpoint will return a categories list and a success value. 

2. ```bash 
curl http://127.0.0.1:5000/categories
```
```
{
    "success": true,
    "categories": [
        "1",
        "2",
        "3",
    ]
}
```

#### Get /categories/{category_id}/questions

1. General: This endpoint will return a JSON object similar to the GET /questions which is the list of questions will be from the selected category ID.  

2. The endpoint includes a request argument to choose the page number, starting from 1.

3. ```bash
curl http://127.0.0.1:5000/categories/1/questions?page=1 
```
```
{
    "success": true,
    "status": 200,
    "questions": [
        {
        "answer": "answer1",
        "category": "2",
        "difficulty": 1,
        "id": 1,
        "question": "question1?"
        }
    ],
    "total_questions": 1,
    "current_category": "",
    "categories": ["cat1" , "cat2"]     
}
```

### Post /quizzes

1. General: This endpoint will expect a JSON object contains a list of previous questions, a quizz category that has the category ID and type.
2. The endpoint will return the next question based on the category. This endpoint won't return a question that was already returned. 

3. ```bash
curl -X POST http://127.0.0.1:5000:quizzes -H "Content-type: application/json" -d 
{
    "previous_questions": [],
    "quiz_category" : {
        "id":"1",
        "type":"1"
    }
}

```
4. Response
```
{ 
    'success': True,
    'question': {
    "id": 1,
    "question": "question1?",
    "answer": "answer1",
    "category": 1,
    "difficulty": 1
    }
}
```


## Reference used:
PEP8 checker - http://pep8online.com/

