# SoftwareProjectTracker

Project is not containerised or particularly nicely deployable.

There are many dependencies.

The system is writen in python and javascript.

Two command prompts must be used.

To run the Django API server and the React application run the following in separate terminals:

SoftwareProjectTracker\mysite python manage.py runserver

SoftwareProjectTracker\mysite\frontend\web-app npm start

Dependencies:

	Python/Django/pip:

		pip install Django==4.1.7

		pip install "django-phonenumber-field[phonenumbers]"
		
		pip install -U scikit-learn

		pip install djangorestframework

		pip install django-cors-headers

		pip install djangorestframework-simplejwt

	Node/React/npm:

		npm install react
		
		npm install react-google-charts

		npm install react-calendar

		npm install jwt-decode
		
		npm install react-icons

		npm install styled-components

		npm install react-bootstrap

		npm install react-scripts

		npm install react-modal