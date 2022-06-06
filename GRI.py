import os
import pandas
import MeCab
import re
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import speech_recognition as sr

class GuessReferenceIntention:
    def __init__(self,folderpath) -> None:
        self.folderpath=folderpath
        self.filelist=os.listdir(folderpath)
        self.labeldict={}
        for i,label in enumerate(self.filelist):
            self.labeldict[i]=label[:-4]
    
    def generate_df(self):
        talk_df=pandas.DataFrame(columns=["sample_talk","label"])
        for i,filename in enumerate(self.filelist):
            filepath=self.folderpath+"/"+filename
            file=open(filepath,'r',encoding="utf-8")
            talk_datas=file.readlines()
            label=i
            for talk_data in talk_datas:
                series=pandas.Series([talk_data,label],index=["sample_talk","label"])
                talk_df=talk_df.append(series,ignore_index=True)
            file.close()
        
        return talk_df

    def togenkei(self,nodes):
        output=[]
        while nodes:
            if not nodes.surface:
                nodes=nodes.next
                continue
            feature=re.split("[,\t]",nodes.feature.replace('*','').replace('\n','').replace('\0','').replace("EOS",''))
            output.append(feature[6] if feature[6] else nodes.surface)
            nodes=nodes.next
        
        return ' '.join(output)

    def morp_analyze(self,df):
        analyzed_df=pandas.DataFrame(columns=["wakatied_text","label"])
        mecab=MeCab.Tagger("-Ochasen")
        for row in df.itertuples():
            wakatied_text=self.togenkei(mecab.parseToNode(row.sample_talk))
            series=pandas.Series([wakatied_text,row.label],index=["wakatied_text","label"])
            analyzed_df=analyzed_df.append(series,ignore_index=True)
        
        return analyzed_df

    def prepare(self):
        df=self.morp_analyze(self.generate_df())
        text_x=df["wakatied_text"].values
        label_y=df["label"].values.astype('int')
        #df[["wakatied_text"]].to_csv("text_x.csv",header=False,index=False)
        #df[["label"]].to_csv("label_y.csv",header=False,index=False)
        return text_x,label_y

    def train(self):
        self.tfidf=TfidfVectorizer(strip_accents=None,lowercase=False,preprocessor=None,smooth_idf=True)
        text_x,y=self.prepare()
        x=self.tfidf.fit_transform(text_x)
        self.vocabulary=list(self.tfidf.vocabulary_.keys())
        self.svm=SVC(kernel="rbf",C=100.0,gamma=0.1)
        self.svm.fit(x,y)
        return

    def guess(self,text):
        mecab=MeCab.Tagger('-Ochasen')
        text=self.togenkei(mecab.parseToNode(text))
        pred_x=self.tfidf.transform(np.array([text]))
        
        return self.labeldict[self.svm.predict(pred_x)[0]]


class VoiceRecognize:
    def __init__(self):
        self.recognizer=sr.Recognizer()
        self.mic=sr.Microphone()
        self.recognizer.non_speaking_duration=0.1
        self.recognizer.pause_threshold=0.2
    
    def voice_recognize(self):
        self.recognizer.pause_threshold=0.4
        with self.mic as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio=self.recognizer.listen(source)
        self.recognizer.pause_threshold=0.2
        try:
            result=self.recognizer.recognize_google(audio,language='ja-JP')
            return result
        except:
            return False
    
    def hotword_recognize(self,hotword):
        with self.mic as source:
                #self.recognizer.adjust_for_ambient_noise(source)
                audio=self.recognizer.listen(source)
            
        try:
            result=self.recognizer.recognize_google(audio,language='ja-JP')
            return result==hotword
        except:
            return False
