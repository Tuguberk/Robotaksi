import paho.mqtt.client as mqtt

def baglanti_saglandiginda(client,userdata,flags,rc):
    print("Sunucuya Bağlanıldı.")
    istemci.subscribe("/robotaksi")
    
def mesaj_geldiginde(client,userdata,msg):
    print(str(msg.payload))
    sıra.put(str(msg.payload))

istemci = mqtt.Client("p1")
istemci.on_connect = baglanti_saglandiginda
istemci.on_message = mesaj_geldiginde
istemci.connect("mqtt.eclipse.org",1883,60)
istemci.loop_start()
"""
class mqttbaglanti:

    def __init__(self,baglanti:str):
        istemci = mqtt.Client("p1")
    istemci.on_connect = baglanti_saglandiginda
    istemci.on_message = mesaj_geldiginde
    istemci.connect("mqtt.eclipse.org",1883,60)
    istemci.loop_forever()
        """
