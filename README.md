# genkon_app

## Installation

*NOTE: Requires [python3](https://www.python.org/download/releases/3.0/),*
[Node.js](http://nodejs.org/)

* `$ wget https://nodejs.org/dist/v8.9.1/node-v8.9.1-linux-x64.tar.xz`
* `$ apt install python3`
* `$ apt install python3-pip`
* `$ git clone https://github.com/jonasrothfuss/genkon_app.git`
* `$ cd genkon_app/`
* `$ pip install -r requirements.txt'
* `$ npm install -g bower'
* `$ npm install`
* `$ bower install`
* `$ python manage.py migrate`
* `$ python manage.py runserver`


## Loading initial data into the database

python manage.py load_data_from_csv <data_dir>
