The steps run the project: 
1. Cloning the project
2. Openning one of projects
3. Reinstalling the libraries: pip install -r requirements.txt
4. Checking database in settings.py and creating an empty database
5. Executing the migrations: python manage.py migrate
6. Creating an superuser (python manage.py createsuperuser) and accessing admin page to test

How to deal with Network error?
1. APIs.js: const BASE_URL = 'http:/+.+.+.+:8000/'; use ip of wi-fi
2. Server: python manage.py runserver 0.0.0.0:8000 => run this
3. file setting.py, retify ALLOWED_HOSTS = ['+.+.+.+'] => done!
