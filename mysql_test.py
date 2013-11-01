import MySQLdb
import socket
import warnings

warnings.filterwarnings('ignore', category=MySQLdb.Warning)

def test():

    try:
    
        con = MySQLdb.connect('hostname', 'testaccount', 'password', 'testdatabase');
        cur = con.cursor()
        
        cur.execute("DROP TABLE IF EXISTS test")
        cur.execute("CREATE TABLE test(id INT PRIMARY KEY AUTO_INCREMENT, value VARCHAR(25))")
        cur.execute("INSERT INTO test(value) VALUES('one')")
        cur.execute("INSERT INTO test(value) VALUES('two')")
        cur.execute("INSERT INTO test(value) VALUES('three')")
        cur.execute("DROP TABLE test")

        con.close()        

    except Exception, error:
        return 1, str(error)
    else:
        return 0, ''


if __name__ == "__main__":

  result = test()
  print result[1]
  exit(result[0])
