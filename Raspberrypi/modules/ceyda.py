import requests
import json

class CEYDA:
    def __init__(self,username,token):
        self.username = username
        self.token = token
        self.url = 'http://beta.ceyd-a.com/jsonengine.jsp'
        self.veri = None
        self.headers = {'Content-Type': 'application/json'}
    
    def sor(self,soru):
        self.veri = {
        "username": self.username,
        "token": self.token,
        "code": soru,
        "type": "text"
        }
        raw = requests.post(self.url, data=json.dumps(self.veri), headers=self.headers)
        start_value = raw.text.find('"answer":')
        list_value = list(raw.text)
        sonlandırma = 0
        cevap = str()
        for i in range(start_value+9,len(list_value)):
            if sonlandırma != 2:
                if list_value[i] == '"':
                    sonlandırma += 1
                else:
                    cevap += list_value[i]
        return cevap
