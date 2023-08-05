================================
        Backup2CSV
================================

Backup2CSV is a simple Django app that allow you to download and 
restore your models content in a csv file.

Quick start
-----------

1. Add "backup2csv" to your INSTALLED_APPS setting like this::

	INSTALLED_APPS = [
        	...
        	'backups',
	]

2. Include the backup2csv URLconf in your project urls.py like this::
	...
	from django.urls import include 

	urlpatterns = [
		...
		path('backup/', include('backups.urls', namespace='bkups')),
		...
	
    ]

3. Start the development server and visit http://127.0.0.1:8000/backup/
   to see the list of all apps and models you have.
