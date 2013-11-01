import poplib
import socket

def test():

    try:
    
        M = poplib.POP3('hostname')
        M.user('username')
        M.pass_('password')
        
        numMessages = len(M.list()[1])
        
        for i in range(numMessages):
            M.dele(i+1)
        
        M.quit()

    except Exception, error:
        return 1, str(error)
    else:
        return 0, ''


if __name__ == "__main__":

  result = test()
  print result[1]
  exit(result[0])
