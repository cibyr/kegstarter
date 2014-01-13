![KegStarter](https://github.com/cibyr/kegstarter/raw/master/main/static/logo.png)
==========

A system for spending our beer fund

Installing
==========

* Ensure `python` and `pip` is installed. See http://www.pip-installer.org/en/latest/installing.html
* Clone the repo.
* Run:
    
```bash
# Install all prerequisites
pip install -r requirements.txt
# Create database tables
python manage.py syncdb
# Create a superuser for local administration
python manage.py createsuperuser
# Start server
python manage.py runserver
```
