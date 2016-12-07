import http
import urllib
import urllib2
import cookielib
import re
import json

class Jinjer:
    def __init__(self,email,password):
        self.email = email
        self.password = password
        self.jar = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
        self.apitoken = None
        pass
    def japi(self,uri,data=None):
        header = {'x-csrf-token':self.csrftoken}
        if data:
            data = urllib.urlencode(data).encode('utf-8')
        if self.apitoken:
            header['api-token'] = self.apitoken
        conn = self.opener.open(urllib2.Request(uri,headers=header),data)
        return conn.read().decode('utf-8')
    def login(self):
        conn = self.opener.open(urllib2.Request('https://kintai.jinjer.biz/sign_in'))
        s = conn.read().decode('utf-8')
        pat = re.compile('<meta name="csrf-token" content="([^"]+)"')
        res = pat.search(s);
        print(res.group(1))
        self.csrftoken = res.group(1)
        s = self.japi('https://kintai.jinjer.biz/v1/sign_in',{'email': self.email,'password': self.password})
        j = json.loads(s)
        print(j)
        self.apitoken = j['data']['token']
        print(s)
        print(self.apitoken)
    def getshopid(self):
        s = self.japi('https://kintai.jinjer.biz/v1/dashboard/shops')
        print(s)
        shopid = json.loads(s)['data']['shops'][0]['id']
        return shopid
    def checkIn(self):
        shopid = self.getshopid()
        s = self.japi('https://kintai.jinjer.biz/v1/dashboard/shops/'+shopid+'/time_cards',{'type':'check_in'})
        print(s)
    def checkOut(self):
        shopid = self.getshopid()
        s = self.japi('https://kintai.jinjer.biz/v1/dashboard/shops/'+shopid+'/time_cards',{'type':'check_out'})
        print(s)
        

