import datetime
import os
import sqlite3
import subprocess
import sys

db_conn = sqlite3.connect(os.path.join(sys.path[0], 'statuslog.db'))
db_cursor = db_conn.cursor()

smtp_fails = db_cursor.execute('select strftime("%H", time), count(*) from reports where report not like "%SMTP: ok%" group by strftime("%H", time);').fetchall();
imap_fails = db_cursor.execute('select strftime("%H", time), count(*) from reports where report not like "%IMAP: ok%" group by strftime("%H", time);').fetchall();
pop3_fails = db_cursor.execute('select strftime("%H", time), count(*) from reports where report not like "%POP3: ok%" group by strftime("%H", time);').fetchall();
mysql_fails = db_cursor.execute('select strftime("%H", time), count(*) from reports where report not like "%MySQL: ok%" group by strftime("%H", time);').fetchall();
ftp_fails = db_cursor.execute('select strftime("%H", time), count(*) from reports where report not like "%FTP: ok%" group by strftime("%H", time);').fetchall();
ssh_fails = db_cursor.execute('select strftime("%H", time), count(*) from reports where report not like "%SSH: ok%" group by strftime("%H", time);').fetchall();
websites_fails = db_cursor.execute('select strftime("%H", time), count(*) from reports where report not like "%Websites: ok%" group by strftime("%H", time);').fetchall();

db_conn.close()

gnuplot_datafile = open('failure_stats_hourly.dat', 'w')
gnuplot_datafile.write('#hour smtp__errorcount imap_errorcount pop3_errorcount mysql_errorcount ftp_errorcount ssh_errorcount websites_errorcount\n')

interation_index = [0, 0, 0, 0, 0, 0, 0] 

for i in range(0, 24):

    hour = '%02d' % i
    gnuplot_datafile.write(hour + ' ')
    
    if interation_index[0] < len(smtp_fails) and smtp_fails[interation_index[0]][0] == hour:
        gnuplot_datafile.write(str(smtp_fails[interation_index[0]][1]) + ' ')
        interation_index[0] += 1
    else:
        gnuplot_datafile.write('0 ')
    
    if interation_index[1] < len(imap_fails) and imap_fails[interation_index[1]][0] == hour:
        gnuplot_datafile.write(str(imap_fails[interation_index[1]][1]) + ' ')
        interation_index[1] += 1
    else:
        gnuplot_datafile.write('0 ')
    
    if interation_index[2] < len(pop3_fails) and pop3_fails[interation_index[2]][0] == hour:
        gnuplot_datafile.write(str(pop3_fails[interation_index[2]][1]) + ' ')
        interation_index[2] += 1
    else:
        gnuplot_datafile.write('0 ')
    
    if interation_index[3] < len(mysql_fails) and mysql_fails[interation_index[3]][0] == hour:
        gnuplot_datafile.write(str(mysql_fails[interation_index[3]][1]) + ' ')
        interation_index[3] += 1
    else:
        gnuplot_datafile.write('0 ')
    
    if interation_index[4] < len(ftp_fails) and ftp_fails[interation_index[4]][0] == hour:
        gnuplot_datafile.write(str(ftp_fails[interation_index[4]][1]) + ' ')
        interation_index[4] += 1
    else:
        gnuplot_datafile.write('0 ')
    
    if interation_index[5] < len(ssh_fails) and ssh_fails[interation_index[5]][0] == hour:
        gnuplot_datafile.write(str(ssh_fails[interation_index[5]][1]) + ' ')
        interation_index[5] += 1
    else:
        gnuplot_datafile.write('0 ')
    
    if interation_index[6] < len(websites_fails) and websites_fails[interation_index[6]][0] == hour:
        gnuplot_datafile.write(str(websites_fails[interation_index[6]][1]))
        interation_index[6] += 1
    else:
        gnuplot_datafile.write('0')
      
    gnuplot_datafile.write('\n')
    
gnuplot_datafile.close()

gnuplot_command  = '''echo "'''

gnuplot_command += '''set out 'failure_stat_hourly.svg'; '''
gnuplot_command += '''set term svg; '''
gnuplot_command += '''set key below; '''
gnuplot_command += '''set ylabel '#errors out of 6 tests/hour per service'; '''
gnuplot_command += '''set object 1 rect from screen 0, 0, 0 to screen 1, 1, 0 behind; '''
gnuplot_command += '''set object 1 rect fc rgb 'white' fillstyle solid 1.0; '''
gnuplot_command += '''set style data histograms; '''
gnuplot_command += '''set style histogram rowstacked; '''
gnuplot_command += '''set boxwidth 0.75 relative; '''
gnuplot_command += '''set style fill solid 1.0 border -1; '''

gnuplot_command += '''plot'''
gnuplot_command += ''' 'failure_stats_hourly.dat' u 8:xticlabel(1) lc rgb '#FF0000' ti 'Websites','''
gnuplot_command += ''' '' u 5 lc rgb '#FF8000' ti 'MySQL', '''
gnuplot_command += ''' '' u 6 lc rgb '#FFFF00' ti 'FTP','''
gnuplot_command += ''' '' u 3 lc rgb '#FF00FF' ti 'IMAP','''
gnuplot_command += ''' '' u 2 lc rgb '#0000FF' ti 'SMTP', '''
gnuplot_command += ''' '' u 7 lc rgb '#00FFFF' ti 'SSH','''
gnuplot_command += ''' '' u 4 lc rgb '#008000' ti 'POP3' '''

gnuplot_command += '''" | gnuplot'''

subprocess.call(gnuplot_command, shell=True)

os.remove('failure_stats_hourly.dat')
