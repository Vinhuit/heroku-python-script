import time, sys ,os ,threading, re, datetime
import grequests,requests, schedule

n=0
listDev=[]
def KillMiner(mtpool):
	mtpool=mtpool.rstrip()
	print("Get Url Kill "+mtpool)
	reqRm = 'http://'+mtpool+'.herokuapp.com/custom?link=pkill+bash%3Bpkill+miner%3Bpkill+run2.sh%3Bpkill+setup_nim.sh&key=&lach='
	return reqRm
def PingDevice(mtpool):
	mtpool=mtpool.rstrip()
	print("Ping Url "+mtpool)
	reqRm = 'http://'+mtpool+'.herokuapp.com/'
	return reqRm
def StartMiner(mtpool):
	mtpool=mtpool.rstrip()
	print("Get Url Devices "+mtpool)
	reqStart = 'http://'+mtpool+'.herokuapp.com/custom?link=mkdir+miner%3Bcd+miner%3Bwget+https%3A%2F%2Fraw.githubusercontent.com%2FVinhuit%2Fazurenimpool%2Fmaster%2Fazure_script%2Frun2.sh%3Bchmod+u%2Bx+run2.sh%3B+.%2Frun2.sh+'+mtpool+'&key=&lach='
	return reqStart
def SenRequestRerunMiner(file,callback,timeout=40):
	urls=[]
	for pool in file:
		pool=pool.rstrip()
		urls.append(callback(pool))	
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
			if re.match("mtpoon",line):
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
	nimiq_core = None
	while nimiq_core is None:
		try:
			nimiq_core = requests.get(url_wallet).json()
		except:
			 pass
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
			print("try get json device")
			data = requests.get(json_address).json()
		except:
			 pass
	devices = data['devices']
	wallet_state = data['wallet_balance']
	balance_formatted = format(wallet_state/100000,'.2f')
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
	return balance_formatted

def send_mess(text):
	url = "https://api.telegram.org/bot751128068:AAG4FraAKZ_es9ymZxy5dlhg3sJGtJpgKdw/"
	params = {'chat_id':"531864213", 'text': text}
	response = requests.post(url + 'sendMessage', data=params)
	return response
def file_lengthy(fname):
        with open(fname) as f:
                for i, l in enumerate(f):
                        pass
        return i + 1
def GetLines(fname):
	with open(fname) as f:
		contents = f.readlines()
	contents = [x.strip() for x in contents] 
	return contents
def ping():
	filenames = ['offline.txt', 'online.txt']
	with open('listacc.txt', 'w') as outfile:
		for fname in filenames:
			with open(fname) as infile:
				for line in infile:
					outfile.write(line)
	f = open("listacc.txt", "rt")
	f2=open('listaccs.txt', 'w')
	listacc=[]
	for line in set(f):
		if re.match("mtpoon",line):
			f2.write(line)
	time.sleep(2)
	f2=open('listaccs.txt', 'rt')
	SenRequestRerunMiner(f2,PingDevice,5)
	
def cancelschedule():
	schedule.clear('startmain')
	schedule.clear('startping')
def startmain():
	schedule.every(3).minutes.do(ping).tag('startping')
	schedule.every(10).minutes.do(main).tag('startmain')
def main():
		global n
		global listDev
		n=n+1;
		balance=SimpleMonitor()
		Compare('offline.txt','online.txt','temp.txt')
		Compare('temp.txt','online.txt','accountsrerun.txt')
		f=open('accountsrerun.txt', 'rt')
		listDev.append(file_lengthy('accountsrerun.txt'))
		if n==2:
			if(listDev[1] < listDev[0]):	
				send_mess("Start Kill")
				SenRequestRerunMiner(f,KillMiner,40)
				
			else:
				send_mess("Start Rerun")
				SenRequestRerunMiner(f,StartMiner,40)
			del listDev[:]
			n=0
		else:			
			send_mess("Start Kill")
			SenRequestRerunMiner(f,KillMiner)

		send_mess("List offline:")
		send_mess('\n'.join(GetLines('accountsrerun.txt')))
		send_mess("Offline :"+str(len(open('accountsrerun.txt',"rt").readlines())))
		send_mess("Online :"+str(len(open('online.txt',"rt").readlines())))
		send_mess("Wallet Balance: "+str(balance))
SimpleMonitor()
#schedule.every(3).minutes.do(main)
print(datetime.datetime.now())
schedule.every().day.at("21:00").do(startmain).tag('main')
schedule.every().day.at("16:00").do(cancelschedule).tag('cancelmain')

while 1:
	schedule.run_pending()
	time.sleep(1)
