import asyncio
from pyrogram import Client
from pyrogram.handlers import MessageHandler
from pyrogram.types import KeyboardButton, ReplyKeyboardMarkup,InlineKeyboardMarkup,InlineKeyboardButton
from pyrogram.types import CallbackQuery, InputTextMessageContent
from pyromod import listen
import sqlite3
import re

api_id = 1259503
api_hash = "96c512ea1ed3d9c3355aba64057c6456"

event = Client("my_account")

db = sqlite3.connect("info.db")

db.execute('CREATE TABLE info (id TEXT, Username TEXT, Name TEXT, Phone TEXT)')

Status = 0

@event.on_message()
async def bot(c:event, m):
    try:
        text = m.text
        chat_id = m.chat.id
        message_id = m.id
        
        if text == "/start":
            keyb = ReplyKeyboardMarkup(
            [
                [
                    KeyboardButton('ثبت نام')
                ]
            ],
            resize_keyboard = True
        )
            await c.send_photo(chat_id, "bot.png", caption=f"سلام کاربر __{m.chat.first_name}__ \nبه ربات دریافت هاست **رایگان** خوش امدید \n برای دریافت هاست **رایگان** روی ثبت نام کلیک کنید",reply_markup=keyb)

        if text == "ثبت نام":
            global Status
            name = await c.ask(chat_id ,'لطفا نام خود را وارد کنید : ')
            phone = await c.ask(chat_id ,'لطفا شماره خود را وارد کنید :')
            number = re.findall(r'09\w{2}', phone.text)
            if len(phone.text) == 11:
                if number:
                    Check = db.execute('SELECT Phone FROM info WHERE Phone = "%s"' %phone.text).fetchone()
                    if Check == None:
                        Status += 1
                        if m.chat.username:
                            db.execute('INSERT INTO info (id, Username, Name, Phone) VALUES (?, ?, ?, ?) ', (Status, m.chat.username, name.text, phone.text))
                            db.commit()
                            keyb = ReplyKeyboardMarkup(
                                [
                                    [
                                        KeyboardButton('دریافت هاست'),
                                        KeyboardButton('ارتباط با ما')
                                        
                                    ]
                                ],
                                resize_keyboard = True
                            )
                            
                            await c.send_message(chat_id, 'اطلاعات با موفقیت ثبت شد ✅',reply_markup=keyb)
                        else:
                            db.execute('INSERT INTO info (id, Name, Phone) VALUES (?, ?, ?) ', (Status, name.text, phone.text))
                            db.commit()
                            keyb = ReplyKeyboardMarkup(
                                [
                                    [
                                        KeyboardButton('دریافت هاست'),KeyboardButton('ارتباط با ما')
                                        
                                    ]
                                ],
                                resize_keyboard = True
                            )
                            
                            await c.send_message(chat_id, 'اطلاعات با موفقیت ثبت شد ✅',reply_markup=keyb)
                    else:
                        await m.reply_text('شما قبلا با این شماره ثبت نام کرده اید ❌')
                else:
                    await m.reply("❌ لطفا شماره رو درست وارد کنید \nمانند : 09129999999")
            else:
                await m.reply("❌ تعداد اعداد شماره اشتباه است ")
        if text == "دریافت هاست":
            try:
                await m.reply("هاستی یافت نشد ❌")
            except:
                pass
        if text == "ارتباط با ما":
            try:
                await m.reply("ایدی ادمین :\n@EBLETSM")
            except:
                pass

    except KeyboardInterrupt:
        exit()

event.run()