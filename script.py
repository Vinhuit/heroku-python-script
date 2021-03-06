import time, sys ,os ,threading, re, datetime
import grequests,requests, schedule, json

n=0
listDev=[]
devicename="zpoon"
jsonserver='http://jsonserver01.herokuapp.com/'
def CheckDevice(num):
	if num == 1:
		url = "https://icemining.ca/site/wallet_miners_results?address=NQ56JVMC03YPS4DYNU9C4VERJER8EJY1JX9U"
	else:
		url = "https://icemining.ca/site/wallet_miners_results?address=NQ95X5CYLT5HLR5YAPME6FT8PGA0SE7TTNXH"
	html = requests.get(url)
	#print (html.content)
	result = re.findall(b'argon2d</b></td><td align="right">(\d+)',html.content)
	return (int(result[0]))
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
	data= '{"device": ""}'
	headers = {'content-type': 'application/json'}
	url = jsonserver+'offline/'+str(num)
	response = requests.put(url, data=data,headers=headers)
	return response
def AddDeviceApi(num,email,name):
	data1= {"device": email.rstrip(),"name":name,"isStart":"False","startAdHoc":"True"}
	data = json.dumps(data1)
	headers = {'content-type': 'application/json'}
	if int(num)>499:
		url=jsonserver+"rerunaccount/"+str(num)
	else:
		url=jsonserver+"temp/"+str(num)
	#url = 'http://xjsonserver01.herokuapp.com/temp/'+str(num)
	response = requests.put(url, data=data,headers=headers)
	return response
def AddDataApi(num,datas):
	data= json.dumps(datas)
	headers = {'content-type': 'application/json'}
	if int(num)>499:
		url=jsonserver+"rerunaccount/"+str(num)
	else:
		url=jsonserver+"temp/"+str(num)
	#url = 'http://xjsonserver01.herokuapp.com/temp/'+str(num)
	print(url)
	response = requests.put(url, data=data,headers=headers)
	return response
def get_device(num=2):
	datas =[]
	datasvinh =[]
	datasdanh =[]
	list50=[]
	list100=[]
	json_address_offline = jsonserver+"alldevices"
	urlDevice = jsonserver+"temp"
	urlDevice2 = jsonserver+"rerunaccount"
	dataOffLine = None
	dataDevice = None
	dataDevice2 = None
	statusCode = 503
	dataping=[]
	while dataOffLine is None:
		try:
			print("try get offline stream")
			dataOffLine = requests.get(json_address_offline).json()
		except:
			 pass
	if len(dataOffLine)>0:
		for i in dataOffLine:
			deviceOff=i["device"]
			if i["name"] == "Vinh":
				datasvinh.append(deviceOff)
			else:
				datasdanh.append(deviceOff)
			datas.append(deviceOff)
	if num == 1:
		while dataDevice is None:
			try:
				print("try get devices")
				dataDevice = requests.get(urlDevice).json()
			except:
				 pass
		while dataDevice2 is None:
			try:
				print("try get devices 2")
				dataDevice2 = requests.get(urlDevice2).json()
			except:
				 pass
	
	#print dataOffLine
	#print dataOnline
	
	
		if len(dataDevice)>0:
			for i in dataDevice:
				deviceOff=i["id"]
				try:
					if i["startAdHoc"] == "True":
						dataping.append("azure00"+str(deviceOff))
				except:
					pass
		if len(dataDevice2)>0:
			for i in dataDevice2:
				deviceOff=i["id"]
				try:
					if i["startAdHoc"] == "True":
						dataping.append("azure00"+str(deviceOff))
				except:
					pass
		list50=datas[len(datas)//2:]
		list100=datas[:len(datas)//2]
		#if len(sys.argv)>1:
		#	SenRequestRerunMiner(list50,PingDevice,60)
		#else:
			#SenRequestRerunMiner(datas,PingDevice,60)
		try:
			if CheckDevice(1) <100:
				print("Ping Vinh")
				send_mess("Start Vinh: "+str(datetime.datetime.now()))
				SenRequestRerunMiner(datasvinh,PingDevice,60)
			if CheckDevice(2) <100:
				print("Ping Danh")
				send_mess("Start Danh: "+str(datetime.datetime.now()))
				SenRequestRerunMiner(datasdanh,PingDevice,60)
			if len(dataping)>1:
				print("Ping AdHoc")
				SenRequestRerunMiner(dataping,PingDevice,60)
		except:
			send_mess("Shoud be start All")
			#SenRequestRerunMiner(datas,PingDevice,60)
	else:	
		send_mess("Start All: "+str(datetime.datetime.now()))
		SenRequestRerunMiner(datas,PingDevice,60)
		
	#schedule.every(3).minutes.do(get_device).tag('getdevice')
	#schedule.every(20).minutes.do(job_that_executes_once)
def get_device2():
	datas =[]
	json_address_offline = jsonserver+"other"
	dataOffLine = None
	statusCode = 503
	while dataOffLine is None:
		try:
			print("try get list device")
			dataOffLine = requests.get(json_address_offline).json()
		except:
			 pass
	
	#print dataOffLine
	#print dataOnline
	if len(dataOffLine)>0:
		num=1
		for i in dataOffLine:
			deviceOff=i["device"]
			if "name" in i:
				name=i["name"]
			else:
				name="Vinh"
			datas.append(deviceOff)
			AddDeviceApi(num,deviceOff,name)
			num=num+1
	#SenRequestRerunMiner(datas,PingDevice,60)
def AddFalseStart():
	datas =[]
	json_address_offline = jsonserver+"temp/"
	dataOffLine = None
	statusCode = 503
	temp_data = []
	while dataOffLine is None:
		try:
			print("try get list device")
			dataOffLine = requests.get(json_address_offline).json()
		except:
			 pass
	#print dataOffLine
	#print dataOnline
	#print(dataOffLine)

	if len(dataOffLine)>4:
		for i in dataOffLine:
			if "name" not in i:
				i.update({'name':'Vinh'})
			i.update({'isStart':'False'})
		for i in range(len(dataOffLine)):
			print(dataOffLine[i])
			print(AddDataApi(i+1,dataOffLine[i]))
def get_offline():
	status = 'online'
	json_address_offline = jsonserver+"offline"
	json_address_online = jsonserver+"online"
	dataOffLine = None
	dataOnline = None
	statusCode = 503
	while dataOffLine is None:
		try:
			print("try get offline stream")
			dataOffLine = requests.get(json_address_offline).json()
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
	if len(dataOffLine)>0:
		for i in dataOffLine:
			deviceOff=i["device"]
			if len(dataOnline)>0:
				for n in dataOnline:
					deviceOn=n["device"]
					if deviceOff==deviceOn:
						device=n["device"]
						link=n["link"]
						key=n["key"]
						num=n["id"]
						print(StartStream(key,link,device,num))
						print ("Rerun "+device)
						break
	#for i in range(1,len(dataOffLine)+1):
		#print i
		#statusCode=RemoveOfilneApi(i).status_code
		#time.sleep(1)
		#print statusCode
		#while statusCode != requests.codes.ok or statusCode != 404:
			#statusCode = RemoveOfilneApi(i).status_code
			#print statusCode
			#if statusCode == 404:
				#break
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
			price = requests.get('https://api.sushipool.com/api/v1/stats/network').json()
		except:
			 pass
	devices = data['devices']
	hashrate =  format(price['hashrate']/(1000000000),'.2f')
	price = price['price']['usd']
	wallet_state = data['wallet_balance']
	balance_formatted = format(wallet_state/100000*price,'.2f')
	devices=sorted(devices,key=sort_by_name)
	open('offline.txt', 'w').close()
	open('online.txt', 'w').close()
	send_mess("HashRate: "+hashrate + 'Gh/s')
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
def job_that_executes_once():
    schedule.clear('getdevice')
    return schedule.CancelJob	
def startmain():
	print('StartSchedule')
	get_device(1)
	#schedule.every(3).minutes.do(ping).tag('startping')
	#schedule.every(10).minutes.do(main).tag('startmain')
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
#get_offline()
#AddFalseStart()
print("Start Run")
#schedule.every(5).minutes.do(startmain)
if len(sys.argv)==2:
	time.sleep(200)
	get_device(2)
if len(sys.argv)==3:
	get_device2()
	get_device(2)
if len(sys.argv)==4:
	get_device(1)	
#schedule.every(120).minutes.do(main)
#schedule.every(1).minutes.do(get_offline)
#schedule.every(123).minutes.do(get_device)
print("Start Run")
#send_mess("Start At: "+str(datetime.datetime.now()))
#schedule.every().day.at("10:56").do(startmain).tag('main2')
#schedule.every().day.at("20:00").do(get_device2)
#schedule.every().day.at("14:00").do(cancelschedule).tag('cancelmain')
#while 1:
#	schedule.run_pending()
#	time.sleep(1)
	#print("Run...")
