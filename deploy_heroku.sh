heroku config:set DISABLE_COLLECTSTATIC=1
git push heroku master
heroku run python manage.py migrate
heroku config:set AWS_SECRET_ACCESS_KEY=87VybgHhTuvDTAuie2LRHPTrBk3ZGuyD0rypvaRq
heroku run python manage.py load_data_from_csv ./app_data/
heroku run python manage.py collectstatic --noinput
heroku open
