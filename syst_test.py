import GRI
import functions
import schedule
import threading
import subprocess
import snowboydecoder
import signal

def jtalk(t):
    open_jtalk=['open_jtalk']
    mech=['-x','/var/lib/mecab/dic/open-jtalk/naist-jdic']
    htsvoice=['-m','/home/rkn/Projects/jtalk/htsvoice_files/Miku-Type-b.htsvoice']
    speed=['-r','0.9']
    outwav=['-ow','open_jtalk.wav']
    cmd=open_jtalk+mech+htsvoice+speed+outwav
    c = subprocess.Popen(cmd,stdin=subprocess.PIPE)
    c.stdin.write(t.encode())
    c.stdin.close()
    c.wait()
    aplay = ['aplay','-q','open_jtalk.wav']
    wr = subprocess.Popen(aplay)


def talk_mode(gri,vr,fnc):
    
    def command_recog():
        jtalk("はい")
        result=vr.voice_recognize()
        print(result)
        if result:
            if result=="終了":
                jtalk("システムを終了するよ")
                exit()
            elif result=="コンソールモード":
                jtalk("コンソールモードに移行するよ")
                console_mode(gri,vr,fnc)
            else:
                label=gri.guess(result)
                print(label)
                if label=="ask_time":
                    fnc.ask_time(mode="talk")
                elif label=="ask_weather_today":
                    fnc.weather("today","osaka",mode="talk")
                elif label=="ask_weather_tomorrow":
                    fnc.weather("tomorrow","osaka",mode="talk")
                elif label=="greeting":
                    fnc.greeting(result,mode="talk")
                else:
                    jtalk("ごめんね、まだそれはできないよ")
        else:
            print("recognition error")
            jtalk("聞き取れなかったよ")


    def signal_handler(signal, frame):
        global interrupted
        interrupted = True

    signal.signal(signal.SIGINT, signal_handler)

    detector = snowboydecoder.HotwordDetector("/home/rkn/Softwares/snowboy/snowboy/examples/Python3/resources/models/computer.umdl", sensitivity=0.5)
    
    flag=True
    while True:
        if flag:
            print("recognize available")
            flag=False
        detector.start(detected_callback=command_recog,sleep_time=0.03)
        detector.terminate()
        flag=True

def console_mode(gri,vr,fnc):
    while (result:=input()):
        if result=="終了":
            print("システムを終了するよ")
            exit()
        elif result=="トークモード":
            print("トークモードに移行")
            talk_mode(gri,vr,fnc)
        else:
            label=gri.guess(result)
            print(label)
            if label=="ask_time":
                fnc.ask_time(mode="console")
            elif label=="ask_weather_today":
                fnc.weather("today","osaka",mode="console")
            elif label=="ask_weather_tomorrow":
                fnc.weather("tomorrow","osaka",mode="console")
            elif label=="greeting":
                        fnc.greeting(result,mode="console")

if __name__=="__main__":
    gri=GRI.GuessReferenceIntention("/home/rkn/Projects/pi_interact/talk_template_data")
    vr=GRI.VoiceRecognize()
    fnc=functions.Functions()

    gri.train()
    print("t:トークモードで開始 c:コンソールモードで開始")
    mode=input()
    if mode=="t":
        talk_mode(gri,vr,fnc)
    elif mode=="c":
        console_mode(gri,vr,fnc)