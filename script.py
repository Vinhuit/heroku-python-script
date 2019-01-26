import time, sys ,os ,threading
import grequests,requests, schedule
def KillMiner(mtpool):
	mtpool=mtpool.rstrip()
	print("Get Url Kill "+mtpool)
	reqRm = 'http://'+mtpool+'.herokuapp.com/custom?link=pkill+bash%3Bpkill+miner%3Bpkill+run2.sh%3Bpkill+setup_nim.sh&key=&lach='
	return reqRm
	
def StartMiner(pool):
	mtpool=mtpool.rstrip()
	print("Get Url Devices "+pool)
	reqStart = 'http://'+pool+'.herokuapp.com/custom?link=mkdir+miner%3Bcd+miner%3Bwget+https%3A%2F%2Fraw.githubusercontent.com%2FVinhuit%2Fazurenimpool%2Fmaster%2Fazure_script%2Frun2.sh%3Bchmod+u%2Bx+run2.sh%3B+.%2Frun2.sh+'+pool+'&key=&lach='
	# try:
		# f =  requests.get(reqStart,timeout=5,verify=False)
		# print("Start Done "+pool)
	# except:
		# pass
	return reqStart

def SenRequestKillMiner(file,function,timeout=20):
	urls=[]
	for mtpool in file:
		mtpool=mtpool.rstrip()
		urls.append(function(mtpool))
	rs = (grequests.get(u,timeout=timeout) for u in urls)
	print(grequests.map(rs))

def Compare(f1,f2,f3):
	with open(f1, 'r') as file1:
		with open(f2, 'r') as file2:
			same = set(file1).difference(file2)

	same.discard('\n')
	list(set(same))
	with open(f3, 'w') as file_out:
		for line in sorted(same):
			file_out.write(line)

def json_address_for_sushi():
	wallet_address="NQ56 JVMC 03YP S4DY NU9C 4VER JER8 EJY1 JX9U"
	sequence_list = wallet_address.split()
	new_string_sushi = '%20'.join(map(str, sequence_list))
	sushi_pool_connect = 'https://api.sushipool.com/api/v1/stats/profile/'
	url_sushi = sushi_pool_connect+new_string_sushi
	return url_sushi

def WalletStatus():
	url_wallet = json_address_for_sushi()
	nimiq_core = requests.get(url_wallet).json()
	wallet_state = nimiq_core['wallet_balance']
	balance_formatted = format(wallet_state/100000,'.2f')
	return balance_formatted
def sort_by_name(d):
	return d['name']
def SimpleMonitor():
	status = 'online'
	json_address = json_address_for_sushi()
	data = None
	while data is None:
		try:
			data = requests.get(json_address).json()
		except:
			 pass
	devices = data['devices']
	devices=sorted(devices,key=sort_by_name)
	open('offline.txt', 'w').close()
	open('online.txt', 'w').close()
	for device in devices:
		miner_name = device['name']
		miner_status = device['device_status']
		
		if miner_status != status:
			open('offline.txt', 'a').write(miner_name+"\n")
		else:
			open('online.txt', 'a').write(miner_name+"\n")

def send_mess(text):
	url = "https://api.telegram.org/bot751128068:AAG4FraAKZ_es9ymZxy5dlhg3sJGtJpgKdw/"
	params = {'chat_id':"531864213", 'text': text}
	response = requests.post(url + 'sendMessage', data=params)
	return response

def main():	
		SimpleMonitor()
		Compare('offline.txt','online.txt','temp.txt')
		Compare('temp.txt','online.txt','accountsrerun.txt')
		f = open("accountsrerun.txt", "rt")
		SenRequestKillMiner(f,KillMiner,40)
		send_mess("List offline: "+str(f.readlines()))
		send_mess("Offline :"+str(len(open('accountsrerun.txt',"rt").readlines())))
		send_mess("Online :"+str(len(open('online.txt',"rt").readlines())))
		send_mess("Wallet Balance: "+str(WalletStatus()))

schedule.every(10).minutes.do(main)
while 1:
    schedule.run_pending()
    time.sleep(1)
