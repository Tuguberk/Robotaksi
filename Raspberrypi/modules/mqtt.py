import paho.mqtt.client as mqtt

class mqtt:
    def __init__(self,link:str):
        self.link = link
        self.istemci = mqtt.Client()
        self.istemci.on_connect = self.baglanti_saglandiginda
        self.istemci.on_message = self.mesaj_geldiginde
        self.istemci.connect("iot.eclipse.org",1883,60)
        self.istemci.loop_forever()
    
    def baglanti_saglandiginda(client,userdata,flags,rc):
        print("Sunucuya Bağlanıldı.")
        client.subscribe(self.link)
    
    def mesaj_geldiginde(client,userdata,msg):
        return msg.topic+" "+str(msg.payload)
