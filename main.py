import tegarbot
import tegarbot.namedtuple
from tegarbot.namedtuple import File, InlineKeyboardMarkup, InlineKeyboardButton
from tegarbot.namedtuple import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, ForceReply
import random
import requests
from bs4 import BeautifulSoup
import time
import os
import json
from glob import glob
import pytz
from datetime import datetime
from config import TOKEN, ADMIN, OWNER, CHANNEL, GROUP, PROJECT_NAME

token = TOKEN
bot = tegarbot.Bot(token)

queue = {
	"free":[],
	"occupied":{}
}
users = []
user3 = []

def saveConfig(data):
	return open('app.json', 'w').write(json.dumps(data))

if __name__ == '__main__':
	s = time.time()
	print(f'[#] Buatan\n[i] Created by @{OWNER}\n')
	print('[#] mengecek config...')
	if not os.path.isfile('app.json'):
		print('[#] memebuat config file...')
		open('app.json', 'w').write('{}')
		print('[#] Done')
	else:
		print('[#] Config found!')
	print('[i] Bot online ' + str(time.time() - s) + 's')
def exList(list, par):
	a = list
	a.remove(par)
	return a

def handle(update):
		
	global queue
	try:
		config = json.loads(open('app.json', 'r').read())
		if 'text' in update:
			text = update["text"]
		else:
			text = ""
		uid = update["chat"]["id"]
		
		if uid not in user3:
			users.append(uid)
		
		if not uid in config and text != "/nopics":
			config[str(uid)] = {"pics":True}
			saveConfig(config)

		if uid in queue["occupied"]:
			if 'text' in update:
				if text != "/stop" and text != "❌ Akhiri" and text != "➡ Skip️" and text != "/next":
					bot.sendMessage(queue["occupied"][uid], "" + text)
			
			if 'photo' in update:
				photo = update['photo'][0]['file_id']
				bot.sendPhoto(queue["occupied"][uid], photo)
                                
			if 'video' in update:
				video = update['video']['file_id']
				bot.sendVideo(queue["occupied"][uid], video)
			
			if 'document' in update:
				document = update['document']['file_id']
				bot.sendDocument(queue["occupied"][uid], document)
				
			if 'audio' in update:
				audio = update['audio']['file_id']
				bot.sendAudio(queue["occupied"][uid], audio)
				
			if 'video_note' in update:
				video_note = update['video_note']['file_id']
				bot.sendVideoNote(queue["occupied"][uid], video_note)
			        
			if 'voice' in update:
				voice = update['voice']['file_id']
				bot.sendVoice(queue["occupied"][uid], voice)
                                
			if 'sticker' in update:
				sticker = update['sticker']['file_id']
				bot.sendSticker(queue["occupied"][uid], sticker)

			if 'contact' in update:
				nama = update["contact"]["first_name"]
				contact = update['contact']['phone_number']
				bot.sendContact(queue["occupied"][uid], contact, first_name=nama, last_name=None)
		                
 
		if text == "/start" or text == "/refresh":
			if not uid in queue["occupied"]:
				keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="ɢʀᴜᴘ ᴄʜᴀᴛ", url=f"t.me/{GROUP}"),InlineKeyboardButton(text="ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{CHANNEL}")]])
				keyboard2 = ReplyKeyboardMarkup(keyboard=[['Cari Partner🔍'],['Pengguna👤','MENU BOT✅']], resize_keyboard=True, one_time_keyboard=True)
				bot.sendMessage(uid, "_🔄 Memulai bot..._", parse_mode='MarkDown', disable_web_page_preview=True, reply_markup=keyboard2)
				bot.sendMessage(uid, f"╭━━◈━━◈━━━━━━━━━━━━━━━━━━━━━\n┃• Selamat Datang Di Anonymous Chat ⚡\n┃• Temukan Pasangan Anda Secara Anonim🙈\n┃• Ketik /search untuk mencari partner\n╰━━◈━━◈━━━━━━━━━━━━━━━━━━━━━\n", parse_mode='MarkDown', disable_web_page_preview=True , reply_markup=keyboard)
		if 'message_id' in update:
			if not uid in queue["occupied"]:
				if text != "/start" and text != "Pengguna👤" and text !="➡ Skip️" and text != "/refresh" and text != "/help" and text != "/search" and text != "Cari Partner🔍" and text != "MENU BOT✅" and text != "🔄 Kembali" and text != "Info Profile 📌" and text != "Covid-19〽️"  and text != "/user" and text != "nulis✍":
					news = ReplyKeyboardRemove()
					bot.sendMessage(uid, "_[❗️] Maap kamu sedang tidak dalam obrolan\nSilahkan Klik /refresh atau /search pada bot_", parse_mode="MarkDown",reply_markup=news, reply_to_message_id=update['message_id'])


		if text == "/test":
			if not uid in queue["occupied"]:
				lolt = ReplyKeyboardMarkup(keyboard=[
                    ['Plain text', KeyboardButton(text='Text only')],
					[dict(text='phone', request_contact=True), KeyboardButton(text='Location', request_location=True)]], resize_keyboard=True)
				bot.sendMessage(uid, "contoh", reply_markup=lolt)

		elif text == "Pengguna👤":
			file = json.loads(open("app.json", "r").read())
			text = "Total Pengguna Bot Ini : " + str(len(file)) + " Pengguna👤"
			bot.sendMessage(uid, text)

		elif text == "/user":
			if str(uid) ==  ADMIN :
				file = open("is.txt", "r")
				text = "Pengguna : " + str(len(file.readlines())) + " Online👤"
				bot.sendMessage(uid, text)
			else:
				bot.sendMessage(uid, "⚡️ Perintah ini hanya untuk admin ⚡️")
		elif text == 'Info Profile 📌':
			if str(uid) == ADMIN :
				name = update["from"]["first_name"]
				_id = update["from"]["id"]
				username = update["from"]["username"]
				tipe = update["chat"]["type"]
				date1 = datetime.fromtimestamp(update["date"], tz=pytz.timezone("asia/jakarta")).strftime("%d/%m/%Y %H:%M:%S").split()
				text = "*Nama : " + str(name)+"*" +"\n"
				text += "*ID Kamu :* " +"`"+ str(_id) +"`"+"\n"
				text += "*Username :* @{username}"+ "\n"
				text += "*Tipe Chat* : " +"_"+ str(tipe)+"_" +"\n"
				text += "*Tanggal :* " + str(date1[0]) +"\n"
				text += "*Waktu :* " + str(date1[1]) + " WIB" "\n"
				bot.sendMessage(uid, text, parse_mode='MarkDown', reply_to_message_id=update['message_id'])
			else:
				bahasa = update["from"]["language_code"]
				name = update["from"]["first_name"]
				_id = update["from"]["id"]
				bot.sendMessage(uid, f"Nama = {name}\nID = `{_id}`\nBahasa = {bahasa}", parse_mode="MarkDown")

		elif text == 'Cari Partner🔍' or text == "/search":
			if not uid in queue["occupied"]:
				keyboard = ReplyKeyboardRemove()
				bot.sendMessage(uid, '_Mencari pasangan..._',parse_mode='MarkDown', reply_markup=keyboard)
				print("[SB] " + str(uid) + " Join ke obrolan")
				queue["free"].append(uid)

		elif text == '❌ Akhiri' or text == '/stop' and uid in queue["occupied"]:
			print('[SB] ' + str(uid) + ' meninggalkan jodohnya ' + str(queue["occupied"][uid]))
			keyboard = ReplyKeyboardMarkup(keyboard=[['Cari Partner🔍'],['Pengguna👤','MENU BOT✅']], resize_keyboard=True, one_time_keyboard=True)
			bot.sendMessage(uid, "_Kamu mengakhiri obrolan!_", parse_mode='MarkDown', reply_markup=keyboard)
			bot.sendMessage(queue["occupied"][uid], "_Partner kamu keluar dari obrolan_", parse_mode='MarkDown', reply_markup=keyboard)
			del queue["occupied"][queue["occupied"][uid]]
			del queue["occupied"][uid]

		elif text == 'MENU BOT✅':
			keyboard = ReplyKeyboardMarkup(keyboard=[
				['/refresh', 'Covid-19〽️'],['🔄 Kembali'],['nulis✍']
			], resize_keyboard=True, one_time_keyboard=True)
			bot.sendMessage(uid, f"MENU BOT", reply_markup=keyboard)
		elif text == 'nulis✍':
			bot.sendMessage(uid, "_fitur akan segera hadir.._")
		elif text == 'Covid-19〽️':
			web = requests.get('https://www.worldometers.info/coronavirus/country/indonesia/')
			tampilan = BeautifulSoup(web.content, 'html.parser')
			dataweb = tampilan.find_all("div", {"class": "maincounter-number"})
			ouy = "*KASUS VIRUS COVID-19 DI INDONESIA 🇮🇩*\n\nTerpapar Virus : {} Orang\nMeninggal : {} Orang\nSembuh : {} Orang".format(dataweb[0].span.text,dataweb[1].span.text,dataweb[2].span.text)
			bot.sendMessage(uid, ouy, parse_mode='MarkDown')
		elif text == '🔄 Kembali':
			keyboard = ReplyKeyboardMarkup(keyboard=[['Cari Partner🔍'],['Pengguna👤','MENU BOT✅']], resize_keyboard=True, one_time_keyboard=True)
			bot.sendMessage(uid, "_🔄 Kembali_", parse_mode='MarkDown', disable_web_page_preview=True, reply_markup=keyboard)
		elif text == "➡ Skip️" or text == "/next" and uid in queue["occupied"]:
			print('[SB] ' + str(uid) + ' meninggalkan obrolan dengan ' + str(queue["occupied"][uid]))
			keyboard = ReplyKeyboardMarkup(keyboard=[['Cari Partner🔍', '🔄 Kembali']], resize_keyboard=True, one_time_keyboard=True)
			bot.sendMessage(uid, "_Kamu mengakhiri obrolan!_",parse_mode="MarkDown")
			bot.sendMessage(queue["occupied"][uid], "_Partnermu mengakhiri obrolan!_",parse_mode="MarkDown", reply_markup=keyboard)
			del queue["occupied"][queue["occupied"][uid]]
			del queue["occupied"][uid] 
			if not uid in queue["occupied"]:
				key = ReplyKeyboardRemove()
				bot.sendMessage(uid, '_Mencari pasangan baru..._',parse_mode="MarkDown" ,reply_markup=key)
				print("[SB] " + str(uid) + " Join ke obrolan") 
				queue["free"].append(uid)
		
		if len(queue["free"]) > 1 and not uid in queue["occupied"]:
			partner = random.choice(exList(queue["free"], uid))
			if partner != uid:
				keyboard = ReplyKeyboardMarkup(keyboard=[
					['➡ Skip️', '❌ Akhiri'],[dict(text='☎️ Beri Kontak Saya', request_contact=True)]
				],resize_keyboard=True, one_time_keyboard=True)
				print('[SB] ' + str(uid) + ' Berjodoh dengan ' + str(partner))
				queue["free"].remove(partner)
				queue["occupied"][uid] = partner
				queue["occupied"][partner] = uid
				bot.sendMessage(uid, '_Partner ditemukan🙈\n/next -- cari partner baru\n/stop -- akhiri obrolan_',parse_mode='MarkDown', reply_markup=keyboard)
				bot.sendMessage(partner, '_Partner ditemukan🙈\n/next -- cari partner baru\n/stop -- akhiri obrolan_',parse_mode='MarkDown', reply_markup=keyboard)
	except 	Exception as e:
		print('[!] Error: ' + str(e))

if __name__ == '__main__':
	bot.message_loop(handle)

	while 1:
		time.sleep(3)
