import imaplib
import socket

def test():

    try:
    
        M = imaplib.IMAP4('hostname', 143)
        M.login('test.account@hostname', 'password')
        M.select('Inbox')
        typ, data = M.search(None, 'ALL')
        for num in data[0].split():
            M.store(num, '+FLAGS', '\\Deleted')
        M.expunge()
        M.close()
        M.logout()

    except Exception, error:
        return 1, str(error)
    else:
        return 0, ''


if __name__ == "__main__":

  result = test()
  print result[1]
  exit(result[0])
