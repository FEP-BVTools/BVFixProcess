from FTPwork import myFtp
from OtherFuc import UsefulFuction
import ctypes, sys
from os import listdir
import os

def UpData(RetryCount,DeviceID,IP_Position,FtpUser,FtpPw):
    
        while(RetryCount>0):            
            try:
                ftp = myFtp("192.168.1.{}".format(IP_Position))
                ftp.Login(FtpUser, FtpPw)
                print()
                
                #設定目標路徑
                ftp.ChangeRount('/') #移至根目錄
                
                if(ftp.CheckFolderExist(DeviceID)==True):                
                    #還原原始linuxrc
                    local_path = './BV_FTPData/'+DeviceID+'/linuxrc'
                    try:
                        ftp.Uploadfile("linuxrc",local_path)
                    except:
                        print("上傳原始linuxrc失敗")
                        UsefulFuction.ErrReport("orignal linuxrc Updata Fail",DeviceID)
                    
                
                    ftp.ChangeRount('bv')                    
                    #上傳備份的檔案
                    local_path = './BV_FTPData/'+DeviceID+'/InBox'
                    romte_path = 'InBox'                    
                    
                    try:
                        ftp.UploadfileTree(local_path,romte_path)   
                    except:
                        print("InBox資料獲取失敗")
                        UsefulFuction.ErrReport("Get InBox Fail",DeviceID)
                    
                       
                    
                    local_path = './BV_FTPData/'+DeviceID+'/Transfered'
                    romte_path = 'Transfered'
                    try:
                        ftp.UploadfileTree(local_path,romte_path)  
                    except:
                        print("Transfered資料獲取失敗")
                        UsefulFuction.ErrReport("Get Transfered Fail",DeviceID)

                    break
                else:
                    print("該IP位置非目標設備:",DeviceID)
                    break
            
            except:
                print("Log in Retry...")
                RetryCount-=1
                
        ftp.close()      

def CheckFileExist(FileName):
    files = listdir("./")
    
    for x in files:
        if(x==FileName):
            return True
    
    return False

    
if UsefulFuction.is_admin():
    if __name__ == "__main__":      
        DeviceInfo={}        
        RetryCount=1
        FTPUser, FTPPw = UsefulFuction.GetFTPLoginInfo('FTPInfoFile.ini')

        while(1):
            if not os.path.exists("./RepairList.txt"): #確認是否存在儲存路徑
                print("RepairList.txt不存在!請重新確認!")

            else:
                DeviceInfo=UsefulFuction.GetDeviceInfo("./RepairList.txt")

                #上傳各設備機台資料
                for DVID in DeviceInfo.keys():
                    print("\nLogin Device:{}".format(DVID))
                    try:
                        UpData(RetryCount,DVID,DeviceInfo[DVID],FtpUser,FtpPw)
                    except:
                        print("Unknow Err")
                        UsefulFuction.ErrReport("Unknow Err",DVID)
                        continue
            break
        input("\n結束")   
else:
    if sys.version_info[0] == 3:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)







