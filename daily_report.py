import smtplib
import sqlite3


#notification infrastructure
def send_report(report):

    header = 'From: "Webservice Watcher" <your.account@gmail.com>\r\nTo: "First Admin" <first.admin@gmail.com>, "Second Admin" <second.admin@gmail.com>\r\nSubject: Daily summary\r\n\r\n'
    message = header + report

    try:
    
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login('your.account', 'password')
        s.sendmail('your.account@gmail.com', ['first.admin@gmail.com', 'second.admin@gmail.com'], message)
        s.quit()

    except Exception, error:
       print str(error)     

 
#service failure report
db_conn = sqlite3.connect('statuslog.db')
db_cursor = db_conn.cursor()

num_tests = db_cursor.execute('select count(*) from reports where strftime("%s", time)-strftime("%s") >= -86400;').fetchone()[0]
smtp_fails = db_cursor.execute('select count(*) from reports where strftime("%s", time)-strftime("%s") >= -86400 and report not like "%SMTP: ok%";').fetchone()[0]
imap_fails = db_cursor.execute('select count(*) from reports where strftime("%s", time)-strftime("%s") >= -86400 and report not like "%IMAP: ok%";').fetchone()[0]
pop3_fails = db_cursor.execute('select count(*) from reports where strftime("%s", time)-strftime("%s") >= -86400 and report not like "%POP3: ok%";').fetchone()[0]
mysql_fails = db_cursor.execute('select count(*) from reports where strftime("%s", time)-strftime("%s") >= -86400 and report not like "%MySQL: ok%";').fetchone()[0]
ftp_fails = db_cursor.execute('select count(*) from reports where strftime("%s", time)-strftime("%s") >= -86400 and report not like "%FTP: ok%";').fetchone()[0]
ssh_fails = db_cursor.execute('select count(*) from reports where strftime("%s", time)-strftime("%s") >= -86400 and report not like "%SSH: ok%";').fetchone()[0]
http_fails = db_cursor.execute('select count(*) from reports where strftime("%s", time)-strftime("%s") >= -86400 and report not like "%HTTP: ok%";').fetchone()[0]
website_fails = db_cursor.execute('select count(*) from reports where strftime("%s", time)-strftime("%s") >= -86400 and report not like "%Websites: ok%";').fetchone()[0]

db_conn.close()

report += 'Number of executed service tests: ' + str(num_tests) + '\n\n'
report += 'Number of failed tests\n'
report += 'SMTP: ' + str(smtp_fails) + '\n'
report += 'IMAP: ' + str(imap_fails) + '\n'
report += 'POP3: ' + str(pop3_fails) + '\n'
report += 'MySQL: ' + str(mysql_fails) + '\n'
report += 'FTP: ' + str(ftp_fails) + '\n'
report += 'SSH: ' + str(ssh_fails) + '\n'
report += 'HTTP: ' + str(http_fails) + '\n'
report += 'Websites: ' + str(website_fails) + '\n'
report += '\n'

send_report(report)
