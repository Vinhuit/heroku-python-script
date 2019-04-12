import time, sys ,os ,threading, re, datetime
import grequests,requests, schedule

n=0
listDev=[]
devicename="zpoon"
def KillAll(mtpool):
	mtpool=mtpool.rstrip()
	print("Get Url Kill "+mtpool)
	reqRm = 'http://'+mtpool+'.herokuapp.com/custom?link=kill+%25%25%3Bpkill+bash%3Bpkill+miner%3Bpkill+run2.sh%3Bpkill+setup_nim.sh%3Bkill+%25%25&key=&lach='
	return reqRm
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
def StartStream(key,link,device,num):
	url = 'http://'+device+'.herokuapp.com/stream?' + 'link='+link+'&key='+key+'&device='+device+'&num='+str(num)
	#params = {'key':key, 'link': 'rtmp://a.rtmp.youtube.com/live2/'+link,'device':device,'num':num}
	response = requests.get(url)
	return response
def RemoveOfilneApi(num):
	data= '[{"device": ""}]'
	headers = {'content-type': 'application/json'}
	url = 'http://myjsonserver-winiss.1d35.starter-us-east-1.openshiftapps.com/offline/'+str(num)
	response = requests.patch(url, data=data,headers=headers)
	return response
def get_offline():
	status = 'online'
	json_address_offline = 'http://myjsonserver-winiss.1d35.starter-us-east-1.openshiftapps.com/offline'
	json_address_online = 'http://myjsonserver-winiss.1d35.starter-us-east-1.openshiftapps.com/online'
	dataOffLine = None
	dataOnline = None
	statusCode = 503
	while dataOffLine is None:
		try:
			print("try get offline stream")
			dataOffLine = requests.get(json_address_offline).json()
			dataOnline = requests.get(json_address_online).json()
		except:
			 pass
	while dataOnline is None:
		try:
			print("try get online stream")
			dataOnline = requests.get(json_address_online).json()
		except:
			 pass
	
	#print dataOffLine
	#print dataOnline
        num=0
	if len(dataOffLine)>0:
                num=num+1
		for i in dataOffLine:
			deviceOff=i[0]["device"]
			if len(dataOnline)>0:
				for n in dataOnline:
					deviceOn=n[0]["device"]
					if deviceOff==deviceOn:
						device=n[0]["device"]
						link=n[0]["link"]
						key=n[0]["key"]
                                                if device !="":
            						print(StartStream(key,link,device,num))
	        					print ("Rerun "+device)
                                                time.sleep(1)
						break
	for i in range(1,len(dataOffLine)+1):
		#print i
		statusCode=RemoveOfilneApi(i).status_code
		statusCode=RemoveOfilneApi(i).status_code
		#time.sleep(1)
		#print statusCode
		while statusCode != requests.codes.ok or statusCode != 404:
			statusCode = RemoveOfilneApi(i).status_code
			statusCode = RemoveOfilneApi(i).status_code
			#print statusCode
			if statusCode == 404:
				break
			#time.sleep(1)
	print ("DoneRemoveDevice")
def Compare(f1,f2,f3):
	with open(f1, 'r') as file1:
		with open(f2, 'r') as file2:
			same = set(file1).difference(file2)

	same.discard('\n')
	list(set(same))
	with open(f3, 'w') as file_out:
		for line in sorted(same):
			if re.match(devicename,line):
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
	price = None
	while data is None:
		try:
			print("try get json device")
			data = requests.get(json_address).json()
		except:
			 pass
	while price is None:
		try:
			print("try get price ")
			price = requests.get('https://api.nimiqx.com/price/btc,usd?api_key=210b34d0df702dd157d31f118ae00420').json()
		except:
			 pass
	price = price['usd']
	devices = data['devices']
	hashrate =  format(data['total_hashrate']/(1000000),'.2f')
	wallet_state = data['wallet_balance']
	balance_formatted = format(wallet_state/100000*price,'.2f')
	devices=sorted(devices,key=sort_by_name)
	open('offline.txt', 'w').close()
	open('online.txt', 'w').close()
	send_mess("HashRate: "+hashrate)
	for device in devices:
		if 'device_status' not in device:
			continue
		miner_name = device['name']
		miner_status = device['device_status']
		
		if miner_status != status:
			open('offline.txt', 'a').write(miner_name+"\n")
		else:
			open('online.txt', 'a').write(miner_name+"\n")
	print("Done Get")
	return balance_formatted
def Compare2(f1,f2,f3):
	with open(f1, 'r') as file1:
		with open(f2, 'r') as file2:
			same = set(file1).difference(file2)

	same.discard('\n')
	list(set(same))
	with open(f3, 'w') as file_out:
		for line in sorted(same):
				file_out.write(line)
def send_mess(text):
	url = "https://api.telegram.org/bot751128068:AAG4FraAKZ_es9ymZxy5dlhg3sJGtJpgKdw/"
	params = {'chat_id':"531864213", 'text': text}
	response = requests.post(url + 'sendMessage', data=params)
	return response
def file_lengthy(fname):
        return sum(1 for line in fname)
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
		if re.match(devicename,line):
			f2.write(line)
	time.sleep(2)
	f2=open('listaccs.txt', 'rt')
	SenRequestRerunMiner(f2,PingDevice,5)
	
def cancelschedule():
	print('stopSchedule')
	schedule.clear('startmain')
	schedule.clear('startping')
	balance=SimpleMonitor()
	Compare('offline.txt','online.txt','temp.txt')
	Compare('temp.txt','online.txt','accountsrerun.txt')
	f=open('accountsrerun.txt', 'rt')
	SenRequestRerunMiner(f,KillAll,40)
	send_mess("Kill All Device:")
	send_mess("Offline :"+str(len(open('accountsrerun.txt',"rt").readlines())))
	send_mess("Online :"+str(len(open('online.txt',"rt").readlines())))
	send_mess("Wallet Balance: "+str(balance))
	
def startmain():
	print('StartSchedule')
	#schedule.every(3).minutes.do(ping).tag('startping')
	schedule.every(10).minutes.do(main).tag('startmain')
def main():
		global n
		global listDev
		n=n+1;
		balance=SimpleMonitor()
		Compare2('offline.txt','online.txt','accountsrerun.txt')
		#Compare('temp.txt','online.txt','accountsrerun.txt')
		f=open('accountsrerun.txt', 'rt')
		#listDev.append(file_lengthy('accountsrerun.txt'))
		#if n==2:
			#if(listDev[1] < listDev[0]):	
				#send_mess("Start Kill")
				#SenRequestRerunMiner(f,KillMiner,40)
				
			#else:
				#send_mess("Start Rerun")
				#SenRequestRerunMiner(f,StartMiner,40)
			#del listDev[:]
			#n=0
		#else:			
			#send_mess("Start Kill")
			#SenRequestRerunMiner(f,KillMiner)

		send_mess("List offline:")
		send_mess('\n'.join(GetLines('accountsrerun.txt')))
		send_mess("Offline :"+str(len(open('accountsrerun.txt',"rt").readlines())))
		send_mess("Online :"+str(len(open('online.txt',"rt").readlines())))
		send_mess("Wallet Balance: "+str(balance))

#schedule.every(3).minutes.do(main)
print(datetime.datetime.now())
#main()
get_offline()
schedule.every(120).minutes.do(main)
schedule.every(1).minutes.do(get_offline)
#schedule.every().day.at("10:56").do(startmain).tag('main2')
#schedule.every().day.at("21:00").do(startmain).tag('main')
#schedule.every().day.at("14:00").do(cancelschedule).tag('cancelmain')
while 1:
	schedule.run_pending()
	time.sleep(1)
