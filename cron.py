#import test modules and define tests to be run
import smtp_test
import imap_test
import pop3_test
import mysql_test
import ftp_test
import ssh_test
import websites_test

tests = [ ['SMTP', smtp_test],
          ['IMAP', imap_test],
          ['POP3', pop3_test],
          ['MySQL', mysql_test],
          ['FTP', ftp_test],
          ['SSH', ssh_test],
          ['HTTP', http_test],
          ['Websites', websites_test],
        ]

num_tries = 5

import socket
socket.setdefaulttimeout(4)

#notification infrastructure
import os
import smtplib
import sqlite3
import sys
import time

def send_report(report):

    header = 'From: "Webservice Watcher" <your.account@gmail.com>\r\nTo: "First Admin" <first.admin@gmail.com>, "Second Admin" <second.admin@gmail.com>\r\nSubject: Webservice status report\r\n\r\n'
    message = header + report

    try:
    
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login('your.account', 'yourpassword')
        s.sendmail('your.account@gmail.com', ['first.admin@gmail.com', 'second.admin@gmail.com'], message)
        s.quit()

    except Exception, error:
       print str(error)     

#run tests
error = 0
results = []

for test in tests:

    result = test[1].test()
    i = 1
    
    while result[0] != 0:
    
        result = test[1].test()
        i = i + 1
        
        if i == num_tries:
            break
    
    results.append( [test[0], result[0], result[1]] )
    
    if result[0] != 0:
        error = 1
        
    #time.sleep(1.0)

#create report
report = ''

for result in results:
    
    if result[1] == 0:
        report += result[0] + ': ok'
    else:
        report += result[0] + ': ' + result[2]
    
    report += '\n'

#retrieve last report and send notification if status changed
db_conn = sqlite3.connect(os.path.join(sys.path[0], 'statuslog.db'))
db_cursor = db_conn.cursor()

previous_report = db_cursor.execute('select report from reports order by id desc limit 0,1;').fetchone();

if previous_report == None:
    send_report(report)
elif report != previous_report[0]:
    send_report(report)
    
#store report
db_cursor.execute( 'INSERT INTO reports (time, error, report ) VALUES (datetime("now", "localtime"), ?, ? );', [error, report] );
db_conn.commit()
db_conn.close()
