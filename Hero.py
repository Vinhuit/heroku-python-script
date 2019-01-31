from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time, sys ,os ,threading, shutil
import requests, schedule, subprocess, pyautogui
from requests.exceptions import ConnectionError
import grequests
import re
from shutil import copyfile
from subprocess import Popen, PIPE, STDOUT

devicename ="zpoon"
def KillMiner(mtpool):
	mtpool=mtpool.rstrip()
	print("Get Url Kill "+mtpool)
	reqRm = 'http://'+mtpool+'.herokuapp.com/custom?link=pkill+bash%3Bpkill+miner%3Bpkill+run2.sh%3Bpkill+setup_nim.sh&key=&lach='
	return reqRm
def KillAll(mtpool):
	mtpool=mtpool.rstrip()
	print("Get Url Kill "+mtpool)
	reqRm = 'http://'+mtpool+'.herokuapp.com/custom?link=kill+%25%25%3Bpkill+bash%3Bpkill+miner%3Bpkill+run2.sh%3Bpkill+setup_nim.sh%3Bkill+%25%25&key=&lach='
	#custom?link=kill+%25%25%3Bpkill+miner%3Bpkill+run2.sh%3Bpkill+setup_nim.sh&key=&lach=
	return reqRm
def StartMiner(mtpool):
	mtpool=mtpool.rstrip()
	print("Get Url Devices "+mtpool)
	reqStart = 'http://'+mtpool+'.herokuapp.com/custom?link=mkdir+miner%3Bcd+miner%3Bwget+https%3A%2F%2Fraw.githubusercontent.com%2FVinhuit%2Fazurenimpool%2Fmaster%2Fazure_script%2Frun2.sh%3Bchmod+u%2Bx+run2.sh%3B+.%2Frun2.sh+'+mtpool+'&key=&lach='
	return reqStart
def my_exception_handler(request, exception):
	print(exception)
	print("a")
def SenRequestRerunMiner(file,callback,timeout=40):
	urls=[]
	for pool in file:
		pool=pool.rstrip()
		urls.append(callback(pool))	
	rs = (grequests.get(u,timeout=timeout) for u in urls)
	a=grequests.map(rs)
	print(a)
	
def MultiRequest(urls):
	threads = []
	for line in urls:
		process = Thread(target=RefreshAccount, args=(line.rstrip(),))
		process.start()
		threads.append(process)
		for process in threads:
   			process.join()
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
def UptimeroboSelenium(headless,mail):
	startNumber = input('Number start: ')
	chrome_options = Options()
	if(headless=='yes'):
		chrome_options.add_argument("--headless")

	driver = webdriver.Chrome("./chromedriver.exe",chrome_options=chrome_options)
	driver.implicitly_wait(10)
	driver.get("https://uptimerobot.com/login")

	elem = driver.find_element_by_xpath("//*[@id=\"userEmail\"]")
	elem.clear()
	elem.send_keys(mail)

	elem = driver.find_element_by_xpath("//*[@id=\"userPassword\"]")
	elem.send_keys("anhvinh12")
	elem.send_keys(Keys.RETURN)

	elem = driver.find_element_by_xpath("//*[@id=\"main-container\"]/div[1]/div/div[1]/div/div[1]/a")
	elem.click()
	num=int(startNumber)
	for i in range(0,50):
		try:
			time.sleep(1)
			elem = driver.find_element_by_xpath("//*[@id=\"s2id_newMonitorType\"]/a")
			time.sleep(1)
			elem.click()
			time.sleep(2)
			elem.send_keys(Keys.ARROW_DOWN)
			elem.send_keys(Keys.RETURN)
			time.sleep(1)
			elem = driver.find_element_by_xpath("//*[@id=\"newHTTPMonitorFriendlyName\"]")
			name=devicename+str((num+i))
			print(name)
			elem.send_keys(name)
			elem = driver.find_element_by_xpath("//*[@id=\"newHTTPMonitorURL\"]")
			url="http://"+name+".herokuapp.com"
			elem.clear()
			elem.send_keys(url)
			elem = driver.find_element_by_xpath("//*[@id=\"newMonitorForm\"]/div[2]/button[2]")
			elem.click()
			time.sleep(1)
			elem.click()
			open('accuptimerobo.txt', 'a').write("\n"+name)
			time.sleep(2)
		except:
			pass
			print("fail")
			num=num-1
			elem = driver.find_element_by_xpath("//*[@id=\"editMonitorForm\"]/div[2]/button[1]")
			elem.click()
			continue
	driver.close()
def CreatePool():
	subprocess.call([r'CreatePool.cmd'])
def CreatePoolLinux(pool):
	print()
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
	time.sleep(1)
	for device in devices:
		miner_name = device['name']
		miner_status = device['device_status']
		
		if miner_status != status:
			open('offline.txt', 'rt').close()
			open('offline.txt', 'a').write(miner_name+"\n")
		else:
			open('offline.txt', 'rt').close()
			open('online.txt', 'a').write(miner_name+"\n")
	return balance_formatted
def CreateHeroku():
	while(1):
		chrome_options = Options()
		chrome_options.add_argument("--incognito")
		num=4
		driver = webdriver.Chrome("./chromedriver.exe",chrome_options=chrome_options)
		driver.implicitly_wait(10)
		driver.get("https://signup.heroku.com/")
		elem = driver.find_element_by_xpath("//*[@id=\"first_name\"]")
		time.sleep(2)
		elem.send_keys("trung")
		elem = driver.find_element_by_xpath("//*[@id=\"last_name\"]")
		elem.send_keys("tran")
		time.sleep(2)
		mail= "hoangha" + str(num) + "@4petstores.online"
		num=num+1
		elem = driver.find_element_by_xpath("//*[@id=\"email\"]")
		time.sleep(2)
		elem.send_keys(mail)
		elem = driver.find_element_by_xpath("//*[@id=\"company\"]")
		time.sleep(2)
		elem.send_keys("ctz")
		elem = driver.find_element_by_xpath("//*[@id=\"role\"]")
		elem.click()
		time.sleep(2)
		elem.send_keys(Keys.ARROW_DOWN)
		elem.send_keys(Keys.RETURN)
		elem = driver.find_element_by_xpath("//*[@id=\"main_programming_language\"]")
		elem.click()
		time.sleep(2)
		elem.send_keys(Keys.ARROW_DOWN)
		elem.send_keys(Keys.ARROW_DOWN)
		elem.send_keys(Keys.ARROW_DOWN)
		elem.send_keys(Keys.ARROW_DOWN)
		elem.send_keys(Keys.RETURN)
		elem = driver.find_element_by_xpath("//*[@id=\"recaptcha-anchor\"]")
		time.sleep(2)
		elem.click()
		time.sleep(30)
def send_mess(text):
	url = "https://api.telegram.org/bot751128068:AAG4FraAKZ_es9ymZxy5dlhg3sJGtJpgKdw/"
	params = {'chat_id':"531864213", 'text': text}
	response = requests.post(url + 'sendMessage', data=params)
	return response

def HerokuDelete(num):
	for i in range(0,num):
		with open('accRerun.txt', 'rt') as f:
			lines = f.read().splitlines()
			numpool = lines[-2]
			pool=lines[-1]
		pool=int(pool)+1
		
		numpool=int(numpool)+5
		try:
			listdirs = os.listdir('.')
			for names in listdirs:
				if re.match(devicename,names):
					shutil.rmtree(names)
		except:
			pass
		mail="trungtuan2"+"@4petstores.online\n"
		# child = winpexpect.winspawn('herokulogin.cmd')
		# child.expect('Email*')
		# child.sendline(mail)
		# child.expect('Password:')
		# child.sendline('Anhvinh12@#')
		p=subprocess.Popen(["python","herokulogin.py"])
		time.sleep(4)
		pyautogui.typewrite(str(mail))
		pyautogui.typewrite('Anhvinh12@#\n')
		pyautogui.typewrite('\n')

		p.wait()
		mtpool=devicename
		base=mtpool+str(numpool)
		print(base)
		check=os.system("heroku git:remote -a "+ base)
		if check == 1:
			break
		os.system("heroku git:clone -a "+ base)
		os.chdir(base)
		os.system("git commit --allow-empty -m "+"\"Trigger\"")
		print(os.system("git push heroku master"))
		#print(os.system("dir"))
		
		open('../accounts.txt', 'w').close()
		open('../accounts.txt', 'a').write(base+"\n")
		open('../listaccount.txt', 'a').write(base+"\n")
		
		print(os.system("heroku plugins:install heroku-fork"))

		for i in range(1,5):
			count=numpool+i
			print(count)
			name=mtpool+str(count)
			os.system("heroku apps:delete --app "+ name+" --confirm " +name)
			open('../accounts.txt', 'a').write(name+"\n")
			open('../listaccount.txt', 'a').write(base+"\n")
			os.system("heroku fork --from " +base +" --to " +name)
		print(os.system("heroku logout"))
		f = open("../accounts.txt", "rt")
		SenRequestRerunMiner(f,StartMiner,40)
		open('../accRerun.txt', 'a').write("\n"+str(numpool)+str(pool))
		os.chdir('..')
	
def herokuFork(num):
	for i in range(0,num):
		with open('acc.txt', 'rt') as f:
			lines = f.read().splitlines()
			numpool = lines[-2]
			pool=lines[-1]
		pool=int(pool)+1
		
		numpool=int(numpool)+5
		try:
			listdirs = os.listdir('.')
			for names in listdirs:
				if re.match(devicename,names):
					shutil.rmtree(names)
		except:
			pass
		mail="trungtuan"+str(pool)+"@4petstores.online\n"
		# child = winpexpect.winspawn('herokulogin.cmd')
		# child.expect('Email*')
		# child.sendline(mail)
		# child.expect('Password:')
		# child.sendline('Anhvinh12@#')
		p=subprocess.Popen(["herokulogin.cmd",str(numpool)])
		time.sleep(3)
		pyautogui.typewrite(str(mail))
		pyautogui.typewrite('Anhvinh12@#\n')
		pyautogui.typewrite('\n')

		p.wait()
		mtpool=devicename
		base=mtpool+str(numpool)
		print(base)
		os.mkdir(base)
		print(os.system("xcopy /s /H youtube-live "+base))
		os.chdir(base)
		#print(os.system("dir"))
		check=os.system("heroku create "+ base)
		if check == 1:
			break
		open('../accounts.txt', 'w').close()
		open('../accounts.txt', 'a').write(base+"\n")
		open('../listaccount.txt', 'a').write(base+"\n")

		print(os.system("git push heroku master"))
		print(os.system("heroku plugins:install heroku-fork"))

		for i in range(1,5):
			count=numpool+i
			print(count)
			name=mtpool+str(count)
			open('../accounts.txt', 'a').write(name+"\n")
			open('../listaccount.txt', 'a').write(base+"\n")
			os.system("heroku fork --from " +base +" --to " +name)
		print(os.system("heroku logout"))
		f = open("../accounts.txt", "rt")
		SenRequestRerunMiner(f,StartMiner,40)
		open('../acc.txt', 'a').write("\n"+str(numpool)+str(pool))
		os.chdir('..')

def TypeText(num):
	for i in range(0,num):
		with open('acc.txt', 'rt') as f:
			lines = f.read().splitlines()
			numpool = lines[-2]
			num=lines[-1]
		num=int(num)+1
		
		numpool=int(numpool)+5
		try:
			listdirs = os.listdir('.')
			for names in listdirs:
				if re.match(devicename,names):
					shutil.rmtree(names)
		except:
			pass
		p=subprocess.Popen(["CreatePool.cmd",str(numpool)])
		time.sleep(5)
		
		#pyautogui.typewrite(str(mail))
		#pyautogui.typewrite('Anhvinh12@#\n')
		#pyautogui.typewrite('\n')
		time.sleep(1)
		p.wait()
		f = open("accounts.txt", "rt")
		SenRequestRerunMiner(f,StartMiner,40)
		open('acc.txt', 'a').write(str(num)+"\n")

def btmore():
	chrome_options = Options()
	#chrome_options.add_argument("--incognito")
	num=4
	driver = webdriver.Chrome("./chromedriver.exe",chrome_options=chrome_options)
	driver.implicitly_wait(10)
	driver.get("https://www.btmore.com/login")
	driver.implicitly_wait(10)
	time.sleep(4)
	elem = driver.find_element_by_xpath("//*[@id=\"app\"]/div/div[2]/div/div[1]/div[2]/div/div/div[2]/div/div/form/div[4]/a/span")
	elem.click()
	time.sleep(2)
	elem = driver.find_element_by_xpath("//*[@id=\"app\"]/div/div[2]/div/div[1]/div[2]/div/div/div[2]/div/div/form/div[3]/button[1]/span")
	elem = driver.find_element_by_xpath("//*[@id=\"app\"]/div/div[2]/div/div[1]/div[2]/div/div/div[1]/div/div/div[2]/form/div[5]/input")
	elem = driver.find_element_by_tag_name('body').send_keys.send_keys(Keys.CONTROL + 't')
	driver.get("https://dropmail.me/en/")
	elem = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/h2/span[1]")
	mail = elem.text
	print(mail)
	elem.send_keys(mail)
	elem = driver.find_element_by_xpath("html/body/div[2]/div[5]/ul/li/div[1]/div[1]/pre")
	print(elem.text)
	elem = driver.find_element_by_xpath("//*[@id=\"last_name\"]")
	elem.send_keys("tran")
	time.sleep(2)
	mail= "hoangha" + str(num) + "@4petstores.online"
	num=num+1
	elem = driver.find_element_by_xpath("//*[@id=\"email\"]")
	time.sleep(2)
	elem.send_keys(mail)
	elem = driver.find_element_by_xpath("//*[@id=\"company\"]")
	time.sleep(2)
	elem.send_keys("ctz")
	elem = driver.find_element_by_xpath("//*[@id=\"role\"]")
	elem.click()
	time.sleep(2)
	elem.send_keys(Keys.ARROW_DOWN)
	elem.send_keys(Keys.RETURN)
	elem = driver.find_element_by_xpath("//*[@id=\"main_programming_language\"]")
	elem.click()
	time.sleep(2)
	elem.send_keys(Keys.ARROW_DOWN)
	elem.send_keys(Keys.ARROW_DOWN)
	elem.send_keys(Keys.ARROW_DOWN)
	elem.send_keys(Keys.ARROW_DOWN)
	elem.send_keys(Keys.RETURN)
	elem = driver.find_element_by_xpath("//*[@id=\"recaptcha-anchor\"]")
	time.sleep(2)
	elem.click()
	time.sleep(30)
	
def main():
	print("""
0 - Kill and Start Miner Device
1 - Kill Miner Device
2 - Start Add Ping Uptimerobo Selenium
3 - Start Create Device Heroku
4 - Start Create Account Heroku
5 - Get Status Device
6 - Schedule Rerun Device 30 minute
"""
)
	n = int(input('Please enter the number: '))
	if n==1:
		os.system("notepad accountsrerun.txt")
		f = open("accountsrerun.txt", "rt")
		SenRequestRerunMiner(f,KillMiner)
		#print(pool_outputs)
		#MultiRequest(f)
		#RefreshAccount(f)
	elif n==0:
		xx = int(input('Run new account: '))
		if xx == 1:
			os.system("notepad accounts.txt")
			f = open("accounts.txt", "rt")
		else:
			os.system("notepad accountsrerun.txt")
			f = open("accountsrerun.txt", "rt")
			
		#SenRequestRerunMiner(f,KillMiner,40)
		SenRequestRerunMiner(f,StartMiner,40)
	elif n==9:

		os.system("notepad accountsrerun.txt")
		f = open("accountsrerun.txt", "rt")
		SenRequestRerunMiner(f,KillAll,40)
	elif n==2:
			print("Start Add Ping Heroku")
			UptimeroboSelenium(sys.argv[1],sys.argv[2])
	elif n==3:
		print("Start Create Pool Heroku")
		CreatePool()
		#os.system("notepad accounts.txt")
		f = open("accounts.txt", "rt")
		SenRequestRerunMiner(f,StartMiner)
	elif n==4:
		print("Start Create Account Heroku")
		CreateHeroku()
	elif n==5:
		balance=SimpleMonitor()
		Compare('offline.txt','online.txt','temp.txt')
		Compare('temp.txt','online.txt','accountsrerun.txt')
		
		print("Offline :"+str(len(open('accountsrerun.txt',"rt").readlines())))
		print("Online :"+str(len(open('online.txt',"rt").readlines())))
		print("Wallet Balance: "+str(balance))
		#os.system("notepad accountsrerun.txt")	
	elif n==6:
		schedule.every(30).minutes.do(main)
		while 1:
			schedule.run_pending()
			time.sleep(1)
	elif n==8:
		btmore()
	elif n ==7:
		try:
			xx = int(input('Input loop: '))
			herokuFork(xx)
		except KeyboardInterrupt:
			pass	
	else:
		try:
			xx = int(input('Input loop: '))
			HerokuDelete(xx)
		except KeyboardInterrupt:
			pass	
main()