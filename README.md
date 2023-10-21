# Tour Forecast

To run this app, run the following commands in your terminal:

```
git clone https://github.com/rifatrakib/tour-forecast.git
cd tour-forecast
virtualenv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

Then run either of the following commands:

```
python manage.py deploy
python manage.py deploy --mode development
python manage.py deploy --mode staging
python manage.py deploy --mode production
```

To stop the application:

```
python manage.py terminate
```
