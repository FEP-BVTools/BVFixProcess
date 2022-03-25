from FTPwork import myFtp
import ctypes, sys
import socket
import time
from OtherFuc import UsefulFuction
import os


#將權限提升為系統管理員
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

    
def SaveBurnTestData(RetryCount,DeviceID,IP_Position,FtpUser,FtpPw):
    
        while(RetryCount>0):            
            try:
                ftp = myFtp("192.168.1.{}".format(IP_Position))
                ftp.Login(FtpUser, FtpPw)
                print()
                
                #設定目標路徑
                ftp.ChangeRount('..') #turn back 
                ftp.ChangeRount('bv')
                
                
                #獲取需備份的檔案
                local_path = './LogReport'
                romte_path = 'LogReport'                    
                ftp.DownLoadFileTree(local_path,romte_path,"192.168.1.{}".format(IP_Position),DeviceID)   
                
                
                break
            
            except:
                print("Log in Retry...")
                RetryCount-=1
                
        ftp.close()        
        


    

if is_admin():
    if __name__ == "__main__":
        
        RetryCount=3
        IP_PositionList=[]
        FTPUser, FTPPw = UsefulFuction.GetFTPLoginInfo('FTPInfoFile.ini')


        while(1):
            if not os.path.exists("./RepairList.txt"): #確認是否存在儲存路徑
                print("RepairList.txt不存在!請重新確認!")

            else:
                DeviceInfo=UsefulFuction.GetDeviceInfo("./RepairList.txt")


                #下載各設備機台資料
                for DVID in DeviceInfo.keys():
                    print("\nLogin Device:{}".format(DVID))
                    try:
                        SaveBurnTestData(RetryCount,DVID,DeviceInfo[DVID],FTPUser,FTPPw)
                    except:
                        print("Unknow Err")
                        continue
            break

        input("\n結束")


else:
    if sys.version_info[0] == 3:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)







