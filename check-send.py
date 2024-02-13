# Программа регулярного чтения датчика температуры и посылки сообщения телеботу
#pip install requests
#pip install --upgrade pip
import requests
import threading
import datetime
import yaml
import socket

with open('/home/pi/repo/check-send.yml') as _fi:
    _param = yaml.safe_load(_fi)
#print(_param["token"])

def send_telegram(text: str):
    _TOKEN=_param["token"]
    _url = "https://api.telegram.org/bot"
    _channel_id = _param["chat_id"]
    _method = _url + _TOKEN + "/sendMessage"

    r = requests.post(_method, data={
         "chat_id": _channel_id,
         "text": text
          })

    if r.status_code != 200:
        #raise Exception("post_text error")
        print("Ошибка",r.status_code)
    else:
        print("Послано удачно")

def f():
    threading.Timer(_param["timeout"], f).start()  # Перезапуск через 3600 секунд - каждый час
    _dt=str(datetime.datetime.today().strftime("%Y-%m-%d_%H.%M"))
    tfile=open(_param["dirbus1w"])
    ttext=tfile.read()
    tfile.close()
    temp=ttext.split("\n")[1].split(" ")[9]
    _temp=float(temp[2:])/1000
    _msg="👉 температура "+str(_temp)

    #print(_temp)
    if _temp < _param["min_threshold"]:
        _msg=" 🚨🚨🚨❄️❄️❄️❄️❄️❄️❄️🚨🚨🚨 Внимание предельный нижний порог темпратуры "+str(_temp)
        send_telegram(_msg)
    elif _temp > _param["max_threshold"]:
        _msg=" 🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨 Внимание предельный верхний порог темпратуры "+str(_temp)
        send_telegram(_msg)
    elif _param["dubug_print"]:
        send_telegram(_msg)
    print(_dt+_msg)

if __name__ == '__main__':
    msg=" ✅ Старт 2️⃣ мониторинга температурного датчика. Периодичность: "+str(_param["timeout"])+", пороги оповещения: "+str(_param["min_threshold"])+" <> "+str(_param["max_threshold"])
    send_telegram(msg+ " "+socket.gethostname())
    print(msg)
    f()
