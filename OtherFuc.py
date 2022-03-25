import socket
import ctypes
import csv
import os
import time


class UsefulFuction:

    #將權限提升為系統管理員
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    
    def GetIPAdress():
        IpAdress=""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80)) #DNS 位址
        IpAdress=s.getsockname()[0]
        s.close()
        
        return IpAdress
    
    def GetDeviceInfo(RepairFile):
        DeviceInfo={}
        IP_Position=1
        with open(RepairFile, newline='') as csvfile:
          rows = csv.reader(csvfile)
          for row in rows:
              DeviceInfo[row[0]]=IP_Position
              IP_Position+=1
          return DeviceInfo
      
    def WriteConfigFile(DeviceID,IP_Position):
        LocalDir="./BV_FTPData/{}/TestMode".format(DeviceID)
        data = str(time.strftime("%Y%m%d%H%M"))
        content='''DeviceID,{}
DeviceTime,{}
LanLocalIP,192.168.1.{}
LanHostIP,192.168.1.200
WlanLocalIP,192.168.3.111
WlanHostIP,192.168.3.1
WlanSSID,FEWiFi
WlanPassword,12345678'''.format(DeviceID,data,IP_Position)
        if not os.path.exists(LocalDir): #確認是否存在儲存路徑
            os.makedirs(LocalDir)
    
        f=open("./BV_FTPData/{}/TestMode/Config.csv".format(DeviceID),'w')
        f.write(content)
    def ErrReport(ErrMessage,DeviceID):
        f=open("ErrReport.csv","a")
        f.write("{},,{}\n".format(DeviceID,ErrMessage))
        f.close()
        
    def GetFTPLoginInfo(FTPInfoFileName):
        if os.path.exists(FTPInfoFileName):
            FTPFile=open(FTPInfoFileName)
            FTPUser=FTPFile.readline().strip()
            FTPPw=FTPFile.readline().strip()
        else:
            while(1):
                FTPUser=input('請輸入FTP帳號')
                if FTPUser!='':
                    FTPPw=input('請輸入密碼')
                    f=open(FTPInfoFileName,mode='a+')
                    f.write(FTPUser)
                    if FTPPw=='':
                        f.write(FTPPw)
                    break
                else:
                    print('帳號不可為空值!!')

        return FTPUser,FTPPw
        
        
        
        
        
        
        
        
        