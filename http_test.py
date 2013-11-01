import httplib
import socket

def test():

    try:
  
        conn = httplib.HTTPConnection("hostname")
        conn.request("GET", "/testdir/testfile")
        r = conn.getresponse()
        
        if r.status != 200:
            raise Exception(str(r.status) + " " + r.reason)
            
        data = r.read()
        conn.close()

    except Exception, error:
        return 1, str(error)
    else:
        return 0, ''


if __name__ == "__main__":

    result = test()
    print result[1]
    exit(result[0])
