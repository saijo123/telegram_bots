exec(open("/home/mango/configs/telegram_client.config").read())

from telethon import TelegramClient, events
# ~ from telethon import sync
# ~ import asyncio
from tqdm import tqdm
import os
import pickledb
import telethon.sync

api_id = APIID
api_hash = APIHASH
client = TelegramClient('session_name', api_id, api_hash)
def download_progress(recvd, total):
	print("downloading... ",(recvd/total)*100)
	
	
def CheckDownloadFile(event):
	file_name = event.media.document.attributes[0].file_name
	file_id = event.media.document.id
	file_path = DLD_PATH+"/"+file_name
	file_size = event.media.document.size
	print("checking file..")
	print("file id:", file_id)
	print("file name:", file_name)
	print("file path:", file_path)
	print("file size: (%d)", file_size/1024/1024, "MB")
	#check if file already downloaded
	try:
		fh = open(file_path, 'r')
		print("open successfull")
	except FileNotFoundError:
		print("file not found in nas")
		#check if file downloaded in the past , check record
		
		db = pickledb.load('downloaded.db', False)
		print(db.get(file_id))
		if str(db.get(file_id)) == "file_id":
			print("we downloaded this file before",file_id)
		else: 
			#download the file
			print("downloading the file", file_name)
			return True
	return False
	#check if file fully downloaded
	# ~ if file_size == os.path.getsize(file_path):
		# ~ print("file fully downloaded")

@client.on(events.NewMessage)
async def event_handler(event):
	db = pickledb.load('downloaded.db', False)
	# check valid use r
	if str(event.from_id) not in  valid_users:
		print("invalid user")
		return
		
	#check valid interface (rpidld)
	if event.to_id.user_id !=  RPIDLD_ID:
		print("invalid interface")
		return
	
	# ~ print(event.stringify())
	#check text or file for download
	if event.media == None:
		print ("text message")
		#HandleTextMessage(msg['text'])
		
	else: 
		print ("file for download")
		#event.reply("file for download")
		if(CheckDownloadFile(event)):
			print("downlaoding")
			output = await client.download_media(event.media, 
						file=DLD_PATH , 
						progress_callback=download_progress)	
			db.set(event.media.document.id, 'file_id')
			print("db set")
			print(db.dump())
			print(db.getall())

		else:
			print("file not downloaded")


client.start()
myself = client.get_me()

client.run_until_disconnected()

#for msg in tqdm(messages):
#	print (msg.stringify())
#	client.download_media(msg)
#client.list_event_handlers()
# ~ while True:
	# ~ #time.sleep(1)
	# ~ status = client.catch_up()
	# ~ print(status)
	# ~ messages = client.get_messages('rpidld', limit=1)
