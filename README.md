# sentimental-analysis

# How to use this application:
1. Login with the user.
2. Click on the Process Data button on the top nav bar (This is a one time process)
3. Click on the view results dropdown.
4. Select the chart name from the dropdown.

# Steps to run the current project locally (On Linux Machine):
1. Create Virtual env (https://packaging.python.org/guides/installing-using-pip-and-virtualenv/)
2. Active virtual env
3. Copy the folder sentimental-analysis-master to appropriate location (clone the repository)
4. In my.ini file of MySQL change value of max_allowed_packet to 160 M (max_allowed_packet = 160M)
5. Run following command to install the dependencies (sentimental-analysis-master/sentimental_analysis_project/requirements.txt)
    pip install requirements.txt
6. python manage.py makemigrations
7. python manage.py migrate
8. python manage.py createsuperuser
9. python manage.py runserver
10. try out the url http://localhost:8000
11. Login with super user.

# How To Serve Django Applications with Apache and mod_wsgi on Ubuntu 16
1. install mod_wsgi
```sudo apt-get update```

```sudo apt-get install python3-pip apache2 libapache2-mod-wsgi-py3```

2. Configure a Python Virtual Environment
```sudo pip install virtualenv```

```mkdir ~/myproject```

```cd ~/myproject```

```virtualenv myprojectenv```

```source myprojectenv/bin/activate```

3. Once the virtual env is activated, install the dependancies

```pip install requirements.txt```

4. ```cd ~/myproject```

# Now, we can migrate the initial database schema to our Mysql database using the management script:

```./manage.py makemigrations```

```./manage.py migrate```

5. Create an administrative user for the project by typing:

```python manage.py createsuperuser```

6. Collect static files

```python manage.py collectstatic```

# Configure Apache

To configure the WSGI pass, we'll need to edit the default virtual host file:

```sudo nano /etc/apache2/sites-available/000-default.conf```

For more details Refer the link -  https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-ubuntu-14-04

# Start server

```sudo service apache2 restart```

# Technologies Used:
1. Django (2.0.4) WEB framework.
2. MySQL 5.6
3. C3 Js for data visualisation
4. Jquery
