# Ride My Way Challenge3
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://travis-ci.org/Quantum-35/Ride_My_Way_Challenge2.svg?branch=ft-develop-ch3-signup-%23158626501)](https://travis-ci.org/Quantum-35/Ride_My_Way_Challenge2)
[![Coverage Status](https://coveralls.io/repos/github/Quantum-35/Ride_My_Way_Challenge2/badge.svg?branch=ft-develop-ch3-signup-%23158626501)](https://coveralls.io/github/Quantum-35/Ride_My_Way_Challenge2?branch=ft-develop-ch3-signup-%23158626501)

Ride-my App is a carpooling application that provides drivers with the ability to create ride offers
and passengers to join available ride offers.

You can get the live version in heroku of the backend [here](https://andela-challenge2-ride-with-me.herokuapp.com)
#### To use it 
```
1.Ensure you have postman installed in your system
2.Just copy the link to post man and start making the requests
```

### Prerequisites

You need to have the Following before getting Started

```
1. Python - download the latest version [Recommend]
2. Flask
3. Postman
```
You can get the link to download Latest version the above here:

   1.Python [here](https://www.python.org/downloads/)
    
   2.Flask [here](http://flask.pocoo.org/docs/1.0/installation/)
    
   3. Postman [here](https://www.getpostman.com/apps)


### Quick Start
**Be sure to use the same version of the code as the version of the docs
you're reading.**

1. Clone the repo
  ```
  $ git clone https://github.com/Quantum-35/Ride_My_Way.git
  $ cd Ride_MY_Way/api/v1
  $ git checkout develop
  ```
```Note``` There are two version cd into v1 for non-persisting data and v2 for persisting data

### Installation and Usage
#### First
Create a virtualenv and activate it::

On Linux or macos terminal

    python3 -m venv venv
    . venv/bin/activate

Or on Windows cmd::

    py -3 -m venv venv
    venv\Scripts\activate.bat

Install the dependencies::

    pip install -r requirements.txt 

Run the development server:
  ```
  $ python run.py
  ```

Navigate to [http://localhost:5000](http://localhost:5000)

### User registration.
Send a `POST` request to `/api/v1/auth/register` endpoint with the payload in
`Json`

An example would be
```
{   
  "username":"example",
  "email": "example@gmail.com",
  "address": "122kitale",
  "password": "123456",
  "confirm_password": "123456",
  "role":"driver"
}
```

All fields above must be in valid  format and the password must be
atleast six characters.
If any of the vields is invalid  or empty or the password is empty or less than
six character, the response `status` will be `failed` with the `message` correct `message`
explaining where you went wrong e.g

As shown below:
```
{
    "message": "Failed you cannot submit empty fields",
    "status": "failed"
}
```

If the user already exists then they wont be registered again, the
following response will be returned.
```
{
    "message": "Failed, User already exists, Please sign In",
    "status": "failed"
}
```

### Running tests with coverage
You can also run tests with coverage by running this command in the terminal
```
pytest --cov-report term-missing --cov=app
```
## Authors

* **Quantum35** - *Initial work* - [quantum-35](https://github.com/Quantum-35/Ride_My_Way/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

#### Contribution
Fork the repo, create a PR to this repository's develop.
