from FTPwork import myFtp
from OtherFuc import UsefulFuction
import os
import ctypes, sys


def SetDeviceStatus(RetryCount,DeviceID,IP_Position,FtpUser,FtpPw):
    
        while(RetryCount>0):            
            try:
                ftp = myFtp("192.168.1.{}".format(IP_Position))
                ftp.Login(FtpUser, FtpPw)
                #設定目標路徑
                ftp.ChangeRount('/') #移至根目錄
                try:
                    ftp.CreatFolder(DeviceID)               
                except:
                    print("已存在該設備ID資料夾")
                
                #下載原始linuxrc檔
                print("下載原始linuxrc")

                local_path = './BV_FTPData/'+DeviceID
                
                if not os.path.exists(local_path): #確認是否存在儲存路徑
                    os.makedirs(local_path)                
                    romte_path = 'linuxrc'                    
                    ftp.DownLoadFile(local_path+'/linuxrc' ,romte_path)  
                    print("成功")
                else:
                    print("skip Download linuxrc file")
                
                print("上傳掛載用linuxrc")
                #上傳用於自動掛載CF卡的linuxrc檔
                ftp.Uploadfile("linuxrc","linuxrc")
                print("成功")
                
                ftp.ChangeRount('bv')
                print("上傳設備設定值")
                #創建該設備ID並上傳
                UsefulFuction.WriteConfigFile(DeviceID,IP_Position)
                
                local_path = './BV_FTPData/'+DeviceID+'/TestMode'
                romte_path = 'TestMode'
                    
                ftp.UploadfileTree(local_path,romte_path)  
                print("成功")
                
                break
            
            except:
                print("Log in Retry...")
                RetryCount-=1
                
        ftp.close()        
            

if UsefulFuction.is_admin():
    if __name__ == "__main__":
        
        RetryCount=1
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
                        SetDeviceStatus(RetryCount,DVID,DeviceInfo[DVID],FTPUser,FTPPw)
                    except:
                        print("Unknow Err")
                        continue
            break

        input("\n結束")   


else:
    if sys.version_info[0] == 3:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)







