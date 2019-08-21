#!/usr/bin/env python3
import RPi.GPIO as GPIO

import time

from threading import Thread

from subprocess import Popen, PIPE

import os

import pyaudio

import speech_recognition as sr

import smbus2

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import serial

import requests

import json

from gtts import gTTS

#################
#from modules import servo ##Servo sürücü bekleniyor
from modules import i2c
from modules import ceyda

###########################################################################
PortRF = serial.Serial("/dev/ttyS0",9600) #Seri iletişimi başlattık

#Gpio ayarları
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#Rotary Encoder ayarı
clk = 20
dt = 26
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
derece = int()
max_derece = int()
clkLastState = GPIO.input(clk)

#i2c ayarı
Açizgi = i2c.i2c(0x04)
#Servo ayarı
#############

#Asistan Ayarı
asistan = ceyda.CEYDA("MacigMirror","55f0f5112ecb771ca78a8778b9c080ba")

#Oled Ekran ayarları
RST = None
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)
padding = -2
top = padding
bottom = height-padding
x = 0
font = ImageFont.load_default()
draw.rectangle((0,0,width,height), outline=0, fill=0)

#########################################

def konus(metin):
    tts = gTTS(text=metin, lang='tr')
    tts.save("ses.mp3")
    process = Popen(['mpg123','ses.mp3'], stdout=PIPE, stderr=PIPE) #linuxa göre ses çalma komutu

#çeviri
def cevir(metin):
    liste = {"ı": "i",
             "İ": "I",
             "Ç": "c",
             "ç": "c",
             "ş": "s",
             "Ş": "s",
             "Ğ": "g",
             "ğ": "g",
             "Ü": "u",
             "ü": "u",
             "Ö": "O",
             "ö": "o"}
    karakter = str()
    for i in list(metin):
        try:
            karakter += liste[i]
        except:
            karakter += i
    #print(karakter)
    return karakter

def RfidBekle(kart):
    while True:
        kart_degeri= str() ##Kart okuma
        okunan_byte = PortRF.read()
        #print(read_byte)
        if okunan_byte == b"\x02":
            for i in range(12):
                okunan_byte=PortRF.read()
                kart_degeri = kart_degeri + okunan_byte.decode("utf-8")
            print(kart_degeri)
            if (kart_degeri == kart):
                Açizgi.VeriGonder("0")
                OledYaz("Hedefe Varıldı")
                print("Hedefe Varıldı")
                konus("Hedefe varıldı.")
                break
        

def OledYaz(metin):
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((x, top),cevir(str(metin)), font=font, fill=255)
    disp.image(image)
    disp.display()
    time.sleep(.3)

def RotarySwitch():
    global derece
    try:
        while True:
            derece = Rotary(derece)
            
    finally:
        GPIO.cleanup()

def Rotary(açı):
    global clkState
    global dtState
    global clkLastState
    clkState = GPIO.input(clk)
    dtState = GPIO.input(dt)
    if clkState != clkLastState:
        if dtState != clkState:
            if açı < max_derece:
                açı += 1
            else:
                if açı > 10:
                    açı -= 1
        clkLastState = clkState
    return açı
    

###############
söylendi = "Komut Gelmedi"

duraklar = list(list())
duraklar_e = list()
duraklar_d = dict()


#Merkezlerimiz veri tabanından okunuyor
if os.path.isfile("modules/merkezler.txt"):
    with open("modules/merkezler.txt","r",encoding='utf8') as dosya:
        veri = dosya.readlines()
        for i in veri:
            if i[0] != "#":
                i = i.replace("\n","")
                istasyon = str()
                rfid = str()
                anahtar = True
                for j in i:
                    if j == ":":
                        anahtar = False
                    elif anahtar == True:
                        istasyon += j
                    else:
                        rfid += j
                duraklar += [[istasyon,rfid]]
        for f in duraklar:
            duraklar_d[f[0]]=f[1]
        print(duraklar_d)
        duraklar_e += [" "]
        for s in duraklar:
            duraklar_e.append(s[0])
        duraklar_e += [" "] 
else:
   print("merkezler.txt bulunamadı.")
   raise ValueError("Merkezler.txt Bulunamadı")

max_derece = 10*len(duraklar)
derece = round(max_derece/2)
print(len(duraklar),"tane durak var.")
print("Derece:",derece)
print("Max_derece:",max_derece)
print("Duraklar_e {} elemenalı".format(len(duraklar_e)))
print(duraklar_e)


def callback(recognizer, audio):
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("çalıştı")
        söylendi = recognizer.recognize_google(audio,language = "tr-TR")
        print(söylendi)
        OledYaz(söylendi)
        söylendi_l = söylendi.lower()
        if duraklar_d.get(söylendi_l) != None:
            konus("Hedefe Gidiliyor. {}".format(söylendi))
            Açizgi.VeriGonder("0")
            OledYaz("Hedefe Gidiliyor")
            print("Beklenen kart:",söylendi_l[5:])
            print("Beklenen numara:",str(duraklar_d[söylendi_l]))
            RfidBekle(str(duraklar_d[söylendi_l]))
        else:
            ceyda_cevap = asistan.sor(söylendi))
            print("Ceyda:",ceyda_cevap)
            konus(ceyda_cevap)
    except sr.UnknownValueError:
        söylendi = "Anlayamadım"
    except sr.RequestError as e:
        söylendi = "Veri alınamadı; {0}".format(e)

############################
OledYaz("Hoş Geldiniz")
r = sr.Recognizer()
m = sr.Microphone()
with m as source:
    r.adjust_for_ambient_noise(source)  # dinlemeden önce arka plan seslerini almamak için kalibre ediyoruz
stop_listening = r.listen_in_background(m, callback)

time.sleep(2)
##########################
def main(): #Ekran için komutlar
    sayac_max = 25
    k_derece = Rotary(derece)
    k_konum = int((k_derece - (k_derece%10))/10)
    onayla = list()
    sayac = 0
    hareket = False
    while True:
        konum = int((derece - (derece%10))/10)
        print("Konum:",konum," Son konum:",k_konum)
        if sayac == sayac_max+1:
            sayac = 0
        if konum != k_konum:
            onayla = list()
            hareket = True
            print("Hareket True")
            sayac = 0
            k_konum = konum
            
        if hareket == True:
            onayla.append(konum)
        if sayac == sayac_max and hareket == True:
            onaykontrol = True
            print(onayla)
            for i in onayla:
                if onayla[0] != i:
                    onaykontrol = False
                    print("onaykontrol false")
            if onaykontrol == True:
                print("onaykontrol true")
                Açizgi.VeriGonder("0")
                OledYaz("Hedefe Gidiliyor")
                print("İstenenkart :"+str(duraklar_e[konum]))
                print("Beklenen numara :"+str(duraklar_d[duraklar_e[konum]]))
                RfidBekle(str(duraklar_d[duraklar_e[konum]]))
                k_konum = int((k_derece - (k_derece%10))/10)
                hareket = False
                onayla = list()
            sayac = 0
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((x, top+3),cevir(duraklar_e[konum-1]),  font=font, fill=255)
        draw.text((x, top+11),cevir("-->"+duraklar_e[konum]),  font=font, fill=255)
        draw.text((x, top+19),cevir(duraklar_e[konum+1]),  font=font, fill=255)
        disp.image(image)
        disp.display()
        print("Sayac:",sayac)
        sayac += 1
        time.sleep(.1)

##########################
rotary = Thread(target=RotarySwitch)
program = Thread(target=main)

rotary.deamon = True
program.deamon = True

rotary.start()
program.start()
    
    
print("durdu")

