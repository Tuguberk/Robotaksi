import smbus2
import time

class i2c:
    bus = smbus2.SMBus(1)
    def __init__(self,adres):
        self.adres = adres

    def VeriGonder(self,veri):
        veri_listesi = list(veri)+[":"]
        for i in veri_listesi:
            i2c.bus.write_byte(self.adres,int(ord(i)))
            time.sleep(.1)

        #i2c.bus.write_byte(self.adres,int(0x0A))

    def VeriOku(self):
        veri = i2c.bus.read_byte(self.adres)
        return veri
