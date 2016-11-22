#!/usr/bin/env python
# -*- coding: utf-8 -*-
import binascii
import os
import nfc
import gspread
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
    row = [timezone('Asia/Tokyo').localize(datetime.now()).isoformat(), ByteToHex(tag.idm)]
    global q
    q.put(row)

def get_data():
    while True:
        if not q.empty() :
            worksheet.append_row(q.get())

def wait_on_user():
    while True:
        clf.connect(rdwr={'on-connect': connected})
        sleep(0.5)

th1 = Thread(target=get_data)
th1.start()
th2 = Thread(target=wait_on_user)
th2.start()

th1.join()
th2.join()
