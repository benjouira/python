import os
import paramiko


class VM:
    def __init__(self):
        self.ssh = paramiko.SSHClient() 
        self.ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        self.ssh.connect('192.168.10.198', username='root', password='a12345678')
        self.sftp = self.ssh.open_sftp()
        #sftp.put("mssql-jdbc-9.2.0.jre8.jar", '/usr/share/logstash/logstash-core/lib/jars/mssql-jdbc-9.2.0.jre8.jar')
        self.dirlist = self.sftp.listdir("/usr/share/logstash")
        print("Dirlist: %s" % self.dirlist)
    

    def Transfer(self,url1,url2):
        with open(url1, "r") as f:
            x=f.read()
        with self.sftp.open(url2, "wb") as f:
            f.write(x)
        self.sftp.close()
        self.ssh.close()

    def Recive(self,url1,url2):
        with self.sftp.open(url1, "r") as f:
            x=f.read()
        with open(url2, "wb") as f:
            f.write(x)
        self.sftp.close()
        self.ssh.close()
    
    def CMD(self,cmd):
        command = cmd #'ls -al /usr'
        (stdin, stdout, stderr) = self.ssh.exec_command(command)
        result = stdout.readlines()
        if len(result)==0:
                # self.sftp.close()
                # self.ssh.close()
                return False
        else :
            for line in result:
                print(line)
            # self.sftp.close()
            # self.ssh.close()
            return result
        



# p=VM()
# p.CMD(input("Write your Command : "))
#p.Transfer(input("Write your local file source path : "),input("Write your ssh file source path : "))
#p.Recive(input("Write your ssh file source path : "),input("Write your local file source path : "))