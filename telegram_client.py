exec(open("/home/mango/configs/telegram_client.config").read())

from telethon import TelegramClient, events
# ~ from telethon import sync
# ~ import asyncio
from tqdm import tqdm
import os
import pickledb
import telethon.sync
import subprocess

api_id = APIID
api_hash = APIHASH
client = TelegramClient('session_name', api_id, api_hash)
def download_progress(recvd, total):
	print("downloading... %.2f" %((recvd/total)*100))

	
	
async def CheckDownloadFile(event):
	file_name = event.media.document.attributes[0].file_name
	file_id = event.media.document.id
	file_path = DLD_PATH+"/"+file_name
	file_size = event.media.document.size
	print("checking file..")
	print("file id:", file_id)
	print("file name:", file_name)
	print("file path:", file_path)
	print("file size: (%.1f)"%(file_size/1024/1024), "MB")
	#check if file already downloaded
	try:
		fh = open(file_path, 'r')
		print("open successfull")
	except FileNotFoundError:
		await event.reply("File is not found in nas default location")
		#check if file downloaded in the past , check record
		
		db = open(DLD_DB, "r").read()
		print(db)
		if str(file_id) in open(DLD_DB, "r").read():
			# ~ print("file present in db")
			await event.reply("but, we downloaded this file in the past")
		else: 
			#download the file
			print("downloading the file", file_name)
			return True
	return False
	#check if file fully downloaded
	# ~ if file_size == os.path.getsize(file_path):
		# ~ print("file fully downloaded")

async def HandleTextMessage(event):
	text = event.text
	if "cmd" in str(text):
		print("cmd for execution")
		cmd = ''
		args = ' '
		cmd_text = text.split("cmd ")[1]
		try:
			cmd = cmd_text.split(" ")[0]
			args = cmd_text.split(" ")[1]
		except:
			# ~ print("no args - fall through")
			cmd = cmd_text
		print(cmd)
		print(args)
		if args == "":
			# ~ print("with args")
			result = subprocess.Popen([cmd, args], stdout=subprocess.PIPE,
											 stderr=subprocess.PIPE)
		else:
			# ~ print("without args")
			result = subprocess.Popen(cmd, stdout=subprocess.PIPE,
											 stderr=subprocess.PIPE)

			
		out, err = result.communicate()
		# ~ print("out",out)
		# ~ print("err",err)
		await event.reply(out.decode('utf-8'))
		await event.reply(err.decode('utf-8'))

		

@client.on(events.NewMessage)
async def event_handler(event):
	db = pickledb.load(DLD_DB, False)
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
		await HandleTextMessage(event)
		
	else: 
		print ("file for download")
		#event.reply("file for download")
		if(await CheckDownloadFile(event)):
			await event.reply("Downlaoding.. ")
			output = await client.download_media(event.media, 
						file=DLD_PATH , 
						progress_callback=download_progress)	
			db.set(event.media.document.id, 'file_id')
			await event.reply("Download completed.")

		else:
			await event.reply("Download cancelled")


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
