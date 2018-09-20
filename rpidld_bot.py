execfile("/home/pi/configs/rpidld.config")
import sys
import time
import telepot

def DownloadFile(file_id, file_name, file_size):
	file_id

def handler(msg):
	from_id = msg['from']['id']
	chat_id = msg['chat']['id']
	if str(from_id) in  valid_users:
		bot.sendMessage(chat_id, 'Valid User')
	else:
		bot.sendMessage(chat_id, 'Invalid User')
		return

#	msg['text']['file_namse']:

	print('Got Message: %s' % str(msg))
	print('File ID: %s' % msg['document']['file_id'])
	print('user id: %s' % from_id)
	print('File Name: %s' % msg['document']['file_name'])
	print('File size: %s' % msg['document']['file_size'])
	print('File size: %s' % msg['document']['file_id'])
	bot.sendMessage(chat_id, 'thank you for your input.. kunju..')

bot = telepot.Bot(BOT_TOKEN)
bot.message_loop(handler)
print('I am listening...')
5
while 1:
    try:
        time.sleep(10)
    
    except KeyboardInterrupt:
        print('\n Program interrupted')
        exit()
    
    except:
        print('Other error or exception occured!')
