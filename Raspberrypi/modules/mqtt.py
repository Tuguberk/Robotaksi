import paho.mqtt.client as mqtt
"""
class mqttsunucu:
    def __init__(self,link:str):
        self.link = link
        self.istemci = mqtt.Client("p1")
        self.istemci.on_connect = mqttsunucu.baglanti_saglandiginda
        self.istemci.on_message = mqttsunucu.mesaj_geldiginde
        self.istemci.connect("iot.eclipse.org",1883,60)
        self.istemci.loop_start()
    
    def baglanti_saglandiginda(client,userdata,flags,rc):
        print("Sunucuya Bağlanıldı.")
        self.istemci.subscribe(self.link)
    
    def mesaj_geldiginde(client,userdata,msg):
        return msg.topic+" "+str(msg.payload)

d = mqttsunucu("/robot")
"""


def baglanti_saglandiginda(client,userdata,flags,rc):
    print("Sunucuya Bağlanıldı.")
    istemci.subscribe("/robotaksi")
    
def mesaj_geldiginde(client,userdata,msg):
    print( msg.topic+" "+str(msg.payload))

istemci = mqtt.Client("p1")
istemci.on_connect = baglanti_saglandiginda
istemci.on_message = mesaj_geldiginde
istemci.connect("iot.eclipse.org",1883,60)
istemci.loop_forever()
