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


## Deploying on heroku
* Create a heroku account
* Install heroku command line interfae
    * `sudo add-apt-repository "deb https://cli-assets.heroku.com/branches/stable/apt ./"`
    * `curl -L https://cli-assets.heroku.com/apt/release.key | sudo apt-key add -`
    * `sudo apt-get update`
    * `sudo apt-get install heroku`
* Login to your account via the CLI - type `heroku login`
* create and upload the website: `heroku create`
* add node.js support for bower: `heroku buildpacks:add --index 1 heroku/nodejs`

Since Heroku dynos (virtual machine) do not have persistent storage, add external S3 storage
* Create AWS S3 bucket and make it publicly accessible by setting the following bucket policy
    ` {
    "Version": "2008-10-17",
    "Statement": [
        {
            "Sid": "AllowPublicRead",
            "Effect": "Allow",
            "Principal": {
                "AWS": "*"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::<BUCKET NAME>/*"
        }
    ]
}` 

* Configure the AWS S3 + CloudFront access by providing the following 
    * AWS key id: `heroku config:set AWS_ACCESS_KEY_ID=<key_id>`
    * AWS secret key: `heroku config:set AWS_SECRET_KEY=<secret_key>`
    * AWS S3 bucket name: `heroku config:set AWS_STORAGE_BUCKET_NAME=<bucket_name>`
    * AWS CloudFront domain name: `heroku config:set AWS_CLOUDFRONT_DOMAIN=<CloudFront_domain_name>`
    
Get the worker running: 
* push repo to heroku master in order to deploy the app: `git push heroku master`
* `heroku run python manage.py migrate`
* load data into the database `heroku run python manage.py load_data_from_csv ./app_data/`
* create superuser with `heroku run manage.py createsuperuser`
* open in browser `heroku open`

