# CloudITAM Web Project



# Development
Make sure
```python
DEVELOPMENT = True
``` 
in app/settings.py

## Installation
```bash
pip install -r requirements.txt
```
## Running application
```bash
python manage.py migrate
python manage.py runsever
```

# Production
After fetch data from github you have to restart uwsgi
```bash
sudo service uwsgi restart
```
Also if you change css/js files restart to nginx server
```bash
sudo service nginx restart
```
