#!/usr/bin/env python
# -*- coding: utf-8 -*-
import binascii
import os
import nfc
import gspread
import pygame
import json
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from datetime import timedelta, tzinfo
from pprint import pprint
from pytz import timezone
from threading import Thread
from time import sleep
import Queue

active = True
q = Queue.Queue()
clf = nfc.ContactlessFrontend('usb')
pygame.mixer.init()
pygame.mixer.music.load(u"button01b.mp3")
data = json.load(open("users.json"))

f = open('doc_id')
doc_id = f.readline().strip()
f.close()
scope = ['https://spreadsheets.google.com/feeds']
path = os.path.expanduser("client_secret.json")
credentials = ServiceAccountCredentials.from_json_keyfile_name(path, scope)
client = gspread.authorize(credentials)
gfile   = client.open_by_key(doc_id)
worksheet  = gfile.sheet1

def ByteToHex(byteStr):
    return ''.join(["%02X" % x for x in byteStr]).strip()

def connected(tag):
    pprint(vars(tag))
    row = [(datetime.utcnow() + timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S'), ByteToHex(tag.idm)]
    global q
    q.put(row)

def get_data():
    while True:
        if not q.empty() :
            worksheet.append_row(q.get())

def wait_on_user():
    while True:
        clf.connect(rdwr={'on-connect': connected})
        pygame.mixer.music.play(1)
        sleep(1)

th1 = Thread(target=get_data)
th1.start()
th2 = Thread(target=wait_on_user)
th2.start()

th1.join()
th2.join()

