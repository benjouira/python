import base64
from datetime import datetime
from matplotlib.pyplot import cla
import pandas as pd

class PwdEncryptor:
    def __init__(self) -> None:
        pass
    def Encrypt(self,password):
        myEncryptedPwd=base64.b64encode(password.encode("utf-8"))
        return myEncryptedPwd
    def Decrypt(self,password):
        retour=""
        myDecryptedPwd=base64.b64decode(password).decode("utf-8")        
        return myDecryptedPwd
    def AddNewPassword(self,plateforme,ip,username,password):
        file=""
        with open('static/security/password.epwd','r') as f:
            file=f.readlines()
            f.close()
        newContent=[]
        encPwd=str(self.Encrypt(password))
        if len(file)>0:
            headers=file[0]
            
            newContent=[plateforme,ip,username,encPwd,str(datetime.now())]    
            with open ('static/security/password.epwd','a') as f:
                f.write('\n'+",".join(newContent))                
                f.close()  
        else:
            headers=['plateforme','ip_adress','username','password','added_at']
            content=[plateforme,ip,username,encPwd,str(datetime.now())]
            newContent=[",".join(headers),",".join(content)]            
            with open ('static/security/password.epwd','a') as f:
                    f.write('\n'.join(newContent))                
                    f.close()
    def getAllCredentials(self):
        df=pd.read_csv('static/security/password.epwd')
        print(df)
        print(df.info())
    def getSpecificCredentials(self,plateforme):
        df=pd.read_csv('static/security/password.epwd')
        df=df[df['plateforme']==plateforme]
        return df
    def updateCredentials(self,plateforme,username,password):
        encPwd=str(self.Encrypt(password))
        df=pd.read_csv('static/security/password.epwd')
        index=df.index[(df['plateforme']==plateforme) & (df['username']==username)].tolist()
        df.at[index,'password']=encPwd
        df.to_csv('static/security/password.epwd')





