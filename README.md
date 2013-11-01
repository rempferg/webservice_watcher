webservice_watcher
==================

This is a python based system to keep track of the availability of a number of web services. Individual tests consist of simple, standardized python modules. Test modules for HTTP, MySQL, SMTP, IMAP, POP3 and SSH exist. Several administrators can be notified via email in case of a status change and will be provided with a summary of the situation. All scripts are compatible with Optware Python 2.5 and can therefore be run on a router using the DD-WRT (http://www.dd-wrt.com/) operating system. Every status reports is stored in a sqlite database for later use. Scripts to create plots visualizing the daily and hourly failure frequency of all services as staggered histograms are included.

#Requirements

- cron deamon for automatic scheduled execution of tests
- python2.5, python2.6, or python 2.7
- sqlite3 for storage of reports
- python modules required for individual tests
- gnuplot for visualization of statistics (optional)

#Setup

- Copy the whole folder to the machine which is supposed to run the tests.
- Comment out the tests you don't want to use in the tests list in cron.py and provide email adresses for the people to be notified in case of status change.
- Open the scripts for the tests you want to use and provide the necessary information.
- All test scripts can be executed individually for testing purposes. Do this, fix the information where neccessary and install missing python modules.
- Add cron.py to your crontab. Make sure cron.py is executed using the correct python executable (python2.5 in case of DD-WRT)

##Notes for individual tests

- The IMAP and POP3 tests delete all emails in the test account. DO NOT USE an account that is not purely for testing.
- The websites test the availability of several domains (via HTTP) and checks the HTTP status code against a reference given in the list websites per domain.

#General notes

- The main point is to be notified when one of your services goes down. It makes no sense to deliver the notifications using the SMTP/IMAP/POP3 service that is being monitored, since this will prevent the notifications from reaching you in case of failure. I recomment using a third party service such as Gmail (https://mail.google.com/) for this task.
- Since the system does only send out notifications in case of failure (and restore), you would not notice the monitoring system being down itself. To prevent this, there is a script provided, sending a small summary of the days test results. It makes sense to train yourself to expect this email at a specific time, once a day.
- By default each test is performed up to 5 times with a timeout of 4 seconds until the test. Only if all of those tests fail, the serice is assumed to be unavailable. This behaviour can be changed in cron.py.

##Setup of the daily summary

- Open daily_summary.py and provide the neccessary account data
- Set up a cron job running daily_summary.py with python

#Visualization of past availability data

- Install gnuplot
- Run create_statusplots_daily.py to create a svg containing daily failure rates as staggered histogram for all services
- Run create_statusplots_hourly.py to create a svg containing hourly failure rates as staggered histogram for all services
