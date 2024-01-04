import time,os
import logging
import telethon
from telethon import functions,types,events
import asyncio

id = 15307186
hash = "c175436f6e2dfaa182b655441fefab94"

from flask import Flask
from threading import Thread
import datetime

app = Flask(__name__)

@app.route('/')
def main_func():
    
    content = "<p>" + "Online @ " + str(datetime.datetime.now()) + "</p>"
    return content

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()


client=telethon.TelegramClient("+9647763031740",id,hash)

client.start()

mesages = []
data = {"is":False,"index":0,"sleep":120}

@client.on(events.NewMessage(chats=[6322278622]))
async def msgs(event):
    text = str(event.text)
    id = event.chat_id
    id_msg = event.message.id
    if "/add" in text:
        b = text.replace("/add ","")
        mesages.append(b)
        await client.send_message(id,f"تم حفظ رسالة ، رقم رسالة : {mesages.index(b)}")
    elif "/delet" in text:
        b = int(text.replace("/delet ",""))
        mesages.remove(mesages[b])
        await client.send_message(id,f"تم حذف الرسالة رقم {b}")
    elif "/setmsg" in text:
        index = int(text.replace("/setmsg ",""))
        data.update({"index":index})
        await client.send_message(id,f"تم تعين رسالة رقم {index}")
    elif text == "/msg":
        for i in mesages:
            await client.send_message(id,i+f"\n\n رقم رسالة : {mesages.index(i)}")
    elif "/time" in text:
        index = int(text.replace("/time ",""))
        data.update({"sleep":index})
        await client.send_message(id,f"تم تعين لوقت الى {index} ثانية")
    elif text == "/stop":
        data.update({"is":False})
        await client.send_message(id,f"تم توقيف النشر 💪")
    elif text == "/start":
        did = 0
        folder=None
        request = await client(functions.messages.GetDialogFiltersRequest())
        for dialog_filter in request:
            if type(dialog_filter) == types.DialogFilterDefault:
                continue
            if dialog_filter.title=="share":folder=dialog_filter
        data.update({"is":True})
        await client.send_message(id,"جاري النشر")
        while data["is"]:
           for peer in folder.include_peers:
                try:
                    await client.send_message(peer,message=mesages[data["index"]])
                except Exception as er:
                    print("Send Error : ",er)
           try:
               did+=1
               sleep = data["sleep"]
               for i in range(sleep):
                   if data["is"] == False:
                       break
                   h = sleep-i
                   await client.edit_message(id,id_msg+1,f"جاري أرسال الرسائل بنجاح ✅\nعدد الرسائل المرسلة : {did}\nوقت التوقف بلثانية : {h} ⏳\nللتوقف أرسل : /stop")
                   await asyncio.sleep(1)
           except Exception as ee:
               print("Time Error : ",ee)
keep_alive()
while True:
    print("Done Run ✅")
    client.run_until_disconnected()