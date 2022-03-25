from FTPwork import myFtp
from OtherFuc import UsefulFuction
import os
import ctypes, sys
import csv

def SaveBackupDataProcess(RetryCount,DeviceID,IP_Position,FtpUser,FtpPw):
    
        while(RetryCount>0):            
            try:
                ftp = myFtp("192.168.1.{}".format(IP_Position))
                ftp.Login(FtpUser, FtpPw)
                print()

                #設定目標路徑
                ftp.ChangeRount('/') #移至根目錄
                ftp.ChangeRount('bv')

                #獲取需備份的檔案
                local_path = './BV_FTPData/'+DeviceID+'/InBox'
                romte_path = 'InBox'                   
                try:
                    ftp.DownLoadFileTree(local_path,romte_path,"192.168.1.{}".format(IP_Position),DeviceID)   
                except:
                    print("InBox資料獲取失敗")
                    UsefulFuction.ErrReport("Get InBox Fail",DeviceID)
                    
                local_path = './BV_FTPData/'+DeviceID+'/Transfered'
                romte_path = 'Transfered'
                try:
                    ftp.DownLoadFileTree(local_path,romte_path,"192.168.1.{}".format(IP_Position),DeviceID)  
                except:
                    print("Transfered資料獲取失敗")
                    UsefulFuction.ErrReport("Get Transfered Fail",DeviceID)
                
                #獲取CF卡資料
                ftp.ChangeRount('..') #turn back 
                ftp.ChangeRount('mnt')
                
                
                #獲取需備份的檔案                
                local_path = './BV_FTPData/'+DeviceID+'/CFBackup'
                romte_path = 'CFBackup'
                try:
                    ftp.DownLoadFileTree(local_path,romte_path,"192.168.1.{}".format(IP_Position),DeviceID)  
                    
                    #還原原始linuxrc
                    ftp.ChangeRount('..') #turn back
                    local_path = './BV_FTPData/'+DeviceID+'/linuxrc'
                    try:
                        ftp.Uploadfile("linuxrc",local_path)
                    except:
                        print("上傳原始linuxrc失敗")
                        UsefulFuction.ErrReport("orignal linuxrc Updata Fail",DeviceID)
                
                
                except:
                    print("CF卡資料獲取失敗")
                    UsefulFuction.ErrReport("Get CF Data Fail",DeviceID)
                
                
                
                
                break
            
            except:
                print("Log in Retry...")
                UsefulFuction.ErrReport("Log in Retry",DeviceID)
                RetryCount-=1
                
        ftp.close()        


def GetDeviceInfo(RepairFile):
    DeviceInfo={}
    with open(RepairFile, newline='') as csvfile:
      rows = csv.reader(csvfile)
      for row in rows:
          DeviceInfo[row[0]]=row[1]
      return DeviceInfo
        
if UsefulFuction.is_admin():
    if __name__ == "__main__":      
        DeviceInfo={}
        RetryCount=1
        FTPUser,FTPPw=UsefulFuction.GetFTPLoginInfo('FTPInfoFile.ini')


        while(1):
            if not os.path.exists("./RepairList.txt"): #確認是否存在儲存路徑
                print("RepairList.txt不存在!請重新確認!")

            else:
                DeviceInfo=UsefulFuction.GetDeviceInfo("./RepairList.txt")

                #下載各設備機台資料
                for DVID in DeviceInfo.keys():
                    print("\nLogin Device:{}".format(DVID))
                    try:
                        SaveBackupDataProcess(RetryCount,DVID,DeviceInfo[DVID],FTPUser,FTPPw)
                    except:
                        print("Unknow Err")
                        UsefulFuction.ErrReport("Unknow Err",DVID)
                        continue
            break
                    

        input("\n結束")   


else:
    if sys.version_info[0] == 3:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
