# Django

The main Django documentation is available [here](https://docs.djangoproject.com/en/).

## Requirements
* [Python](https://www.python.org/downloads/)
* [Django](https://www.djangoproject.com/download/)

All the required Python packages are listed in `requirements.txt` (to be updatable with `pip freeze > requirements.txt`), run `pip install -r requirements.txt` to load them in your environment.

<a name="pip-freeze-warning">:warning:</a> **Always** run `pip freeze` from a virtual environment! Or it will just go on filling with c**p when deploying from any Cloud platform.

## Random notes
* The project structure is created with `py -m django startproject`
    * The project automatically includes a `db.sqlite` database for testing purposes
* Within the project, there may be several *apps*: each app structure is created with `py -m django startapp`
* The live web server is started with `py -m django manage runserver` and is reachable at http://localhost:8000
* Django follows the MVC architecture (Model-View-Controller), although it uses a non-idiomatic way of naming its parts:  
```
Idiomatic term | Django term | Meaning
Model          | Model       | Contains all the business logic. At the very least the database access logic
View           | Template    | Responsible for generating the HTML and other UI
Controller     | View        | Contains the logic to tie the other parts together and to generate a response to a user request
```
A schematic view is available below:
![Django Structure](./images/django-structure.png)
* The views of the app call the templates saved in `APPLICATION_NAME/templates/APPLICATION_NAME` (according to a Django's convention)
* The templates use a combination of HTML/CSS/JS and Django's `{% block %}` syntax: this lets you modularize the code
* The HTML/CSS/JS templates use [Bootstrap](https://getbootstrap.com/docs/5.1/getting-started/introduction/)
* Bootstrap was not installed, we just copied/edited some templates found online
* Oversimplifying, to add a feature you
  1) Update the model in `models.py` (if needed)
  2) Create or update the corresponding view in `views.py`
  3) If the new feature opens a new page, create the new html page in `templates/` and add it to `urls.py`
* Django is embedded in HTML via [template tags](https://docs.djangoproject.com/en/3.2/ref/templates/builtins/)
* :warning: Do _not_ comment Django template tags with usual HTML comments, as described [here](https://stackoverflow.com/questions/62793267/reverse-for-create-order-with-no-arguments-not-found)!! 
```html
<!-- this is the usual HTML comment -->
<!-- {% This is an uncommented Django tag %} -->
<!-- {#% This is a commented Django tag %#} -->
```
* General application secrets (i.e. database user, database password, secret key, etc.) are decoupled from the application with a JSON file not tracked by Git and using the `get_secret` function in `settings.py`

### About user authentication
* To restrict the user's login, add the `@login_required(login_url='login')` decorator from `django.contrib.auth.decorators` above any restricted view in `views.py` [**manual method**]
* Likewise, you don't want any logged-in user to be able to access the `'login'` or the `'register'` page: add the `if request.user.is_authenticated` in those views to handle it [ **manual method** ]
* Decorators can be listed in a dedicated `\APPLICATION_NAME\decorators.py` file. A **decorator** is a function that takes another function as a parameter. Decorators are called with the `@` symbol
* Adding a property to a user: check [this documentation](https://docs.djangoproject.com/en/dev/topics/auth/customizing/#extending-the-existing-user-model)

### Sending emails (e.g. to reset the user's password)
* The main settings are saved in the `settings.py` file under the `EMAIL_` parameters
* In our example, Gmail was used as the SMTP host; any external login attempt would be blocked by default by Gmail unless you allow "less secure apps" access ([here](https://myaccount.google.com/lesssecureapps)'s the link). BTW it doesn't work directly with MFA accounts, where you'd need a specific [App password](https://support.google.com/accounts/answer/185833?hl=en).
* The `urls.py` must met specific criteria: use the predefined [Authentication Views](https://docs.djangoproject.com/en/3.2/topics/auth/default/#module-django.contrib.auth.views) from `django.contrib.auth` and remember to use the corresponding URLs' names
* If you want to customize all the pre-built forms used by Django's Authentication Views, you can find the templates' names within their [definitions](https://github.com/django/django/blob/master/django/contrib/auth/views.py). Override the default in your `urls.py` by specifying `.as_view(template_name="accounts/TEMPLATE_NAME.html")` in the URL line

### About database and relationships
* To initiate the database, run `py -m manage migrate`: the database's settings are in `SETTINGS.py` and SQLite3 is the default.
* To run progressive migrations, edit your models then run `py -m manage makemigrations` to create your migration files (preparation files before actual migration) in `/APPLICATION_NAME/migrations/`. Remember to register your models in the _admin_ panel to see them.
* To retrieve data from the db, use [this reference guide](https://docs.djangoproject.com/en/2.2/ref/models/querysets):
  1) Open your Django shell (`py -m manage shell`)
  2) Import all your models (`from APPLICATION_NAME.models import *`)
  3) Specific tables are then available as objects with `TABLENAME.objects.all()` and other methods. 
     1) Example: to retrieve all the customers saved with the `Customer` method, run `Customer.objects.all()`
     2) Example: to retrieve all the customers with a specific name, run `Customer.objects.all().filter(name="YOURNAME")`
* A function to specifically create random orders was implemented in the `management\commands\populate-db.py` function, inspired by [this article](https://testdriven.io/blog/django-charts/).

#### Postgresql
* After first testing, migrate the db from SQLite to PostgreSQL using [these instructions](https://medium.com/djangotube/django-sqlite-to-postgresql-database-migration-e3c1f76711e1).
  * To start PostgreSQL CLI, `sudo -u postgres psql`
  * To send a command, `sudo su - postgres -c "COMMAND"` 
  * To list databases, `\l`
  * To choose a database, `\c DATABASE_NAME`
  * To show all the tables in the database, `\dt`
  * To look for a specific table in the database, `\dt *PATTERN*`

### About deployment
* Before deploying, remember to:
  * Turn `Debug = FALSE` in `settings.py`
  * Add the remote host to the `ALLOWED_HOSTS` in `settings.py`, like
```
ALLOWED_HOSTS = [
    get_secret('HEROKU_HOST'),      # For production purposes (Debug=FALSE)
    "127.0.0.1"                     # For testing purposes (Debug=TRUE)
    ]
```

* To deploy on [Heroku](https://www.heroku.com/), your project needs the [Gunicorn](https://gunicorn.org/) and [Whitenoise](http://whitenoise.evans.io/en/stable/) pip modules installed
  * After logging in (`heroku login -i`), connect to your Heroku app using the Heroku CLI an running `heroku git:remote --app=HEROKU_APP_NAME` to add a remote origin to your Git tracking in the project
  * Add a [`procfile`](https://devcenter.heroku.com/articles/procfile) (no extension!) to your project: it's needed by Heroku to specify a process type. Inside of it, just type `web: gunicorn YOUR_APP_WSGI_NAME.wsgi --log-file -`
  * Remember to specific a _build pack_ (i.e. Python) in your Heroku app settings
  * In the manual deploy from the Heroku app page, you may need to remove some specific requirements' versions (as described in [this post](https://stackoverflow.com/questions/47304291/heroku-upload-could-not-find-a-version-that-satisfies-the-requirement-anaconda/56754565)) from `requirements.txt` (but first, remember to [check this](#pip-freeze-warning)!)
  * Heroku doesn't know how to serve static files, so it is better to install [Whitenoise](http://whitenoise.evans.io/en/stable/) and use it in the `MIDDLEWARE` section of your `settings.py` file

* To deploy on [Docker](https://www.docker.com/)

## **Definitely** review:
* [Forms](https://docs.djangoproject.com/en/3.2/topics/forms/) and [Formsets](https://docs.djangoproject.com/en/3.2/topics/forms/formsets/)
* Users' authentication and register page
* How to use decorators