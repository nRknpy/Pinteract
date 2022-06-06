import datetime
import subprocess
import json
from urllib import request
import random
import conf_

class Functions:
    def __init__(self) -> None:
        pass

    def jtalk(self,t):
        open_jtalk=['open_jtalk']
        mech=['-x',conf_.mech]
        htsvoice=['-m',conf_.htsvoice]
        speed=['-r','0.9']
        outwav=['-ow','open_jtalk.wav']
        cmd=open_jtalk+mech+htsvoice+speed+outwav
        c = subprocess.Popen(cmd,stdin=subprocess.PIPE)
        c.stdin.write(t.encode())
        c.stdin.close()
        c.wait()
        aplay = ['aplay','-q','open_jtalk.wav']
        wr = subprocess.Popen(aplay)

    def ask_time(self,mode):
        dt_now=datetime.datetime.now()
        if dt_now.hour<12:
            h=dt_now.hour
            m=dt_now.minute
            ampm="午前"
        else:
            h=dt_now.hour-12
            m=dt_now.minute
            ampm="午後"
            
        if mode=="talk":
            self.jtalk(f"今は{ampm}{h}時{m}ふんだよ")
        elif mode=="console":
            print(f"今は{ampm}{h}時{m}分だよ")
        else:
            print("モード判定でエラーが発生したよ")
            self.jtalk("モード判定でエラーが発生したよ")
        
        return
        
    def weather(self,date,place,mode):
        weather_id={100:"晴れ",
                    101:"晴れ 時々 くもり",
                    102:"晴れ 時々 雨",
                    103:"晴れ 時々 雨",
                    104:"晴れ 一時 雪",
                    105:"晴れ 一時 雪",
                    106:"晴れ 時々 雨",
                    107:"晴れ 時々 雨",
                    108:"晴れ 時々 雨",
                    110:"晴れ のち くもり",
                    111:"晴れ のち くもり",
                    112:"晴れ のち 雨",
                    113:"晴れ のち 雨",
                    114:"晴れ のち 雨",
                    115:"晴れ のち 雪",
                    116:"晴れ のち 雪",
                    117:"晴れ のち 雪",
                    118:"晴れ のち 雨",
                    119:"晴れ のち 雨",
                    120:"晴れ 時々 雨",
                    121:"雨 のち 晴れ",
                    122:"晴れ のち 雨",
                    123:"晴れ",
                    124:"晴れ",
                    125:"晴れ のち 雨",
                    126:"晴れ のち 雨",
                    127:"晴れ のち 雨",
                    128:"晴れ のち 雨",
                    129:"晴れ のち 雨",
                    130:"晴れ",
                    131:"晴れ",
                    132:"晴れ 時々 くもり",
                    140:"晴れ 時々 雨",
                    160:"晴れ 一時 雪",
                    170:"晴れ 一時 雪",
                    181:"晴れ のち 雪",
                    200:"くもり",
                    201:"くもり 時々 晴れ",
                    202:"くもり 一時 雨",
                    203:"くもり 時々 雨",
                    204:"くもり 一時 雪",
                    205:"くもり 時々 雪",
                    206:"くもり 一時 雨",
                    207:"くもり 時々 雨",
                    208:"くもり 一時 雨",
                    209:"くもり",
                    210:"くもり のち 晴れ",
                    211:"くもり のち 晴れ",
                    212:"くもり のち 雨",
                    213:"くもり のち 雨",
                    214:"くもり のち 雨",
                    215:"くもり のち 雪",
                    216:"くもり のち 雪",
                    217:"くもり のち 雪",
                    218:"くもり のち 雨",
                    219:"くもり のち 雨",
                    220:"くもり 一時 雨",
                    221:"雨 のち くもり",
                    222:"くもり のち 雨",
                    223:"くもり 時々 晴れ",
                    224:"くもり のち 雨",
                    225:"くもり のち 雨",
                    226:"くもり のち 雨",
                    227:"くもり のち 雨",
                    228:"くもり のち 雪",
                    229:"くもり のち 雪",
                    230:"くもり のち 雪",
                    231:"くもり",
                    240:"くもり 時々 雨",
                    250:"くもり 時々 雪",
                    260:"くもり 一時 雪",
                    270:"くもり 時々 雪",
                    281:"くもり のち 雪",
                    300:"雨",
                    301:"雨 時々 晴れ",
                    302:"雨 一時 くもり",
                    303:"雨 時々 雪",
                    304:"雨 時々 雪",
                    306:"雨",
                    307:"雨",
                    308:"雨",
                    309:"雨 時々 雪",
                    311:"雨 のち 晴れ",
                    313:"雨 のち くもり",
                    314:"雨 のち 雪",
                    315:"雨 のち 雪",
                    316:"雨 のち 晴れ",
                    317:"雨 のち くもり",
                    320:"雨 のち 晴れ",
                    321:"雨 のち くもり",
                    322:"雨 時々 雪",
                    323:"雨 のち 晴れ",
                    324:"雨 のち 晴れ",
                    325:"雨 のち 晴れ",
                    326:"雨 のち 雪",
                    327:"雨 のち 雪",
                    328:"雨",
                    329:"雨 時々 雪",
                    340:"雪 時々 雨",
                    350:"雨",
                    361:"雪 のち 晴れ",
                    371:"雪 のち くもり",
                    400:"雪",
                    401:"雪 時々 晴れ",
                    402:"雪 一時 くもり",
                    403:"雪 時々 雨",
                    405:"雪",
                    406:"雪",
                    407:"雪",
                    409:"雪 時々 雨",
                    450:"雪",
                    411:"雪 のち 晴れ",
                    413:"雪 のち くもり",
                    414:"雪 のち 雨",
                    420:"雪 のち 晴れ",
                    421:"雪 のち くもり",
                    422:"雪 のち 雨",
                    423:"雪 のち 雨",
                    424:"雪 のち 雨",
                    425:"雪",
                    426:"雪 のち 雨",
                    427:"雪 時々 雨"}
        place_id={"tokyo":"130000",
                  "aichi":"230000",
                  "osaka":"270000"}
        
        url=f"https://www.jma.go.jp/bosai/forecast/data/forecast/{place_id[place]}.json"
        request.urlretrieve(url,"weather.json")
        
        with open("weather.json","r",encoding="UTF-8") as f:
            data=json.load(f)
        
        weather_today=weather_id[int(data[0]["timeSeries"][0]["areas"][0]["weatherCodes"][0])]
        weather_tomorrow=weather_id[int(data[0]["timeSeries"][0]["areas"][0]["weatherCodes"][1])]
        if len(data[0]["timeSeries"][2]["areas"][0]["temps"])==2:
            maxtemp_today=None
            mintemp_tomorrow=data[0]["timeSeries"][2]["areas"][0]["temps"][0].replace("-","マイナス")
            maxtemp_tomorrow=data[0]["timeSeries"][2]["areas"][0]["temps"][1].replace("-","マイナス")
        else:
            maxtemp_today=data[0]["timeSeries"][2]["areas"][0]["temps"][1].replace("-","マイナス")
            mintemp_tomorrow=data[0]["timeSeries"][2]["areas"][0]["temps"][2].replace("-","マイナス")
            maxtemp_tomorrow=data[0]["timeSeries"][2]["areas"][0]["temps"][3].replace("-","マイナス")
        
        if date=="today":
            if mode=="talk":
                self.jtalk(f"今日の天気は,{weather_today}"+f",で、にっちゅうの最高気温は,{maxtemp_today}度"*(maxtemp_today!=None)+"だよ！")
            elif mode=="console":
                print(f"今日の天気は,{weather_today}"+f",で、にっちゅうの最高気温は,{maxtemp_today}度"*(maxtemp_today!=None)+"だよ！")
            else:
                self.jtalk("モード判定でエラーが発生したよ")
                print("モード判定でエラーが発生したよ")
        elif date=="tomorrow":
            if mode=="talk":
                self.jtalk(f"明日の天気は,{weather_tomorrow},で、最低気温は,{mintemp_tomorrow}度、最高気温は,{maxtemp_tomorrow}度だよ！")
            elif mode=="console":
                print(f"明日の天気は{weather_tomorrow}で、最低気温は{mintemp_tomorrow}度、最高気温は{maxtemp_tomorrow}度だよ！")
            else:
                self.jtalk("モード判定でエラーが発生したよ")
                print("モード判定でエラーが発生したよ")
    
    def greeting(self,text,mode):
        dt_now=datetime.datetime.now()
        if mode=="talk":
            if "おはよう" in text:
                self.jtalk("おはようございます！"+"マスター！"*(random.random()<=0.35))
            elif dt_now.hour>=19 or dt_now.hour<=2:
                self.jtalk("こんばんわ！"+"マスター！"*(random.random()<=0.3))
            else:
                self.jtalk("こんにちわー！"+"マスター！"*(random.random()<=0.3))
        elif mode=="console":
            if "おはよう" in text:
                self.jtalk("おはようございます！"+"マスター！"*(random.random()<=0.35))
                print("おはようございます！"+"マスター！"*(random.random()<=0.35))
            elif dt_now.hour>=19 or dt_now.hour<=2:
                self.jtalk("こんばんわ！"+"マスター！"*(random.random()<=0.3))
                print("こんばんわ！"+"マスター！"*(random.random()<=0.3))
            else:
                self.jtalk("こんにちわー！"+"マスター！"*(random.random()<=0.3))
                print("こんにちわー！"+"マスター！"*(random.random()<=0.3))
        else:
            self.jtalk("モード判定でエラーが発生したよ")
            print("モード判定でエラーが発生したよ")


if __name__=="__main__":
    fnc=Functions()
    fnc.weather("today","osaka","talk")