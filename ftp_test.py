import ftplib
import socket

def ftp_output(line):
    pass

def test():

    try:
    
        ftp = ftplib.FTP('hostname')
        ftp.login('username', 'password')
        ftp.retrlines('LIST', ftp_output)
        ftp.quit()

    except Exception, error:
        return 1, str(error)
    else:
        return 0, ''


if __name__ == "__main__":

    result = test()
    print result[1]
    exit(result[0])
