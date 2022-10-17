import requests
import time
class LineMassage:
    def SendErrMassage(MsgWord,Swich):
        if Swich==1:
            headers = {'Authorization': 'Bearer 4WU3fy82DR24JOgQj0xTy2SFBupewXSlMzWrek3nIfg'}
            my_data = {'message': MsgWord}
            r = requests.post("https://notify-api.line.me/api/notify", headers=headers,data = my_data)
if __name__ == "__main__":
    result = time.localtime(time.time())
    LineMassage.SendErrMassage("Neal哥 給我錢錢~~~",1)