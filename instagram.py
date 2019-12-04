import autoit #https://pypi.org/project/PyAutoIt/
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import os


chrome_options = Options()
chrome_options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')
driver = webdriver.Chrome(chrome_options=chrome_options)

userid = "sohom004@gmail.com"
passwd = "ig12345678"
image_file_path = r"c:\python34\file.jpg"

driver.get('https://www.instagram.com/accounts/login/?hl=en')


driver.get('https://instagram.com')
#driver.maximize_window()
#driver.minimize_window()

driver.find_element_by_xpath("//button[text()='Log In']").click()

driver.find_elements_by_css_selector('form input')[0].send_keys(userid)
driver.find_elements_by_css_selector('form input')[1].send_keys(passwd)
driver.find_element_by_xpath("//button[@type='submit']").submit()

try:
	driver.find_element_by_xpath("//button[text()='Cancel']").click()
except:
	pass
try:
	driver.find_element_by_xpath("//button[text()='Not Now']").click()
except:
	pass


# Creating a post by uploading picture 
ActionChains(driver).move_to_element(driver.find_element_by_xpath("//div[@class='q02Nz _0TPg']//span[@aria-label='New Post']")).click().perform()
handle = "[CLASS:#32770; TITLE:Open]"
autoit.win_wait(handle, 60)
autoit.control_set_text(handle, "Edit1", image_file_path)
autoit.control_click(handle, "Button1")
ActionChains(driver).move_to_element(driver.find_element_by_xpath("//button[@class='UP43G']")).click().perform()
ActionChains(driver).move_to_element(driver.find_element_by_xpath("//button[@class='UP43G']")).click().perform()

# Changing user profile picture
driver.get('https://instagram.com')
type_file_length = len(driver.find_elements_by_xpath("//input[@type='file']"))
driver.find_elements_by_xpath("//input[@type='file']")[type_file_length-3].send_keys(r"c:\python34\profile.png")
#driver.find_elements_by_xpath("//input[@type='file']")[1].send_keys(r"c:\python34\profile.png")
#driver.find_elements_by_xpath("//input[@class='tb_sK']")[2].send_keys(r"c:\python34\profile.png")
ActionChains(driver).move_to_element(driver.find_element_by_xpath("//button[@class='UP43G']")).click().perform()

# Create story
ActionChains(driver).move_to_element(driver.find_element_by_xpath("//button[@class='JdY43']")).click().perform()
handle = "[CLASS:#32770; TITLE:Open]"
autoit.win_wait(handle, 60)
autoit.control_set_text(handle, "Edit1", image_file_path)
autoit.control_click(handle, "Button1")
# device rotation required
#ActionChains(driver).move_to_element(driver.find_element_by_xpath("//button[@class='UP43G']")).click().perform()
#ActionChains(driver).move_to_element(driver.find_element_by_xpath("//button[@class='UP43G']")).click().perform()

driver.quit()

##
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

mobile_emulation = { 
			#"deviceName": "Apple iPhone 3GS"
			#"deviceName": "Apple iPhone 4"
			#"deviceName": "Apple iPhone 5"
			#"deviceName": "Apple iPhone 6"
			#"deviceName": "Apple iPhone 6 Plus"
			#"deviceName": "BlackBerry Z10"
			#"deviceName": "BlackBerry Z30"
			#"deviceName": "Nexus 4"
			"deviceName": "Nexus 5"
			#"deviceName": "Nexus S"
			#"deviceName": "HTC Evo, Touch HD, Desire HD, Desire"
			#"deviceName": "HTC One X, EVO LTE"
			#"deviceName": "HTC Sensation, Evo 3D"
			#"deviceName": "LG Optimus 2X, Optimus 3D, Optimus Black"
			#"deviceName": "LG Optimus G"
			#"deviceName": "LG Optimus LTE, Optimus 4X HD" 
			#"deviceName": "LG Optimus One"
			#"deviceName": "Motorola Defy, Droid, Droid X, Milestone"
			#"deviceName": "Motorola Droid 3, Droid 4, Droid Razr, Atrix 4G, Atrix 2"
			#"deviceName": "Motorola Droid Razr HD"
			#"deviceName": "Nokia C5, C6, C7, N97, N8, X7"
			#"deviceName": "Nokia Lumia 7X0, Lumia 8XX, Lumia 900, N800, N810, N900"
			#"deviceName": "Samsung Galaxy Note 3"
			#"deviceName": "Samsung Galaxy Note II"
			#"deviceName": "Samsung Galaxy Note"
			#"deviceName": "Samsung Galaxy S III, Galaxy Nexus"
			#"deviceName": "Samsung Galaxy S, S II, W"
			#"deviceName": "Samsung Galaxy S4"
			#"deviceName": "Sony Xperia S, Ion"
			#"deviceName": "Sony Xperia Sola, U"
			#"deviceName": "Sony Xperia Z, Z1"
			#"deviceName": "Amazon Kindle Fire HDX 7?"
			#"deviceName": "Amazon Kindle Fire HDX 8.9?"
			#"deviceName": "Amazon Kindle Fire (First Generation)"
			#"deviceName": "Apple iPad 1 / 2 / iPad Mini"
			#"deviceName": "Apple iPad 3 / 4"
			#"deviceName": "BlackBerry PlayBook"
			#"deviceName": "Nexus 10"
			#"deviceName": "Nexus 7 2"
			#"deviceName": "Nexus 7"
			#"deviceName": "Motorola Xoom, Xyboard"
			#"deviceName": "Samsung Galaxy Tab 7.7, 8.9, 10.1"
			#"deviceName": "Samsung Galaxy Tab"
			#"deviceName": "Notebook with touch"
			
			# Or specify a specific build using the following two arguments
			#"deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
		    #"userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }
		}

#chrome_options = webdriver.ChromeOptions()
chrome_options = Options()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
#chrome_options.add_argument("window-size=1039,859")
driver = webdriver.Chrome(chrome_options=chrome_options,executable_path=r'c:\python34\chromedriver.exe')


######################################################################################
import json
import os
import re
import requests
import random
from urllib.parse import unquote,quote
from datetime import datetime
import time
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

try:
	if not os.path.exists(os.path.join(os.path.expanduser("~"),"Documents","MediaBOTS")):
		os.mkdir(os.path.join(os.path.expanduser("~"),"Documents","MediaBOTS"))
		if not os.path.exists(os.path.join(os.path.expanduser("~"),"Documents","MediaBOTS","InstagramBOT")):
			os.mkdir(os.path.join(os.path.expanduser("~"),"Documents","MediaBOTS","InstagramBOT"))
			if not os.path.exists(os.path.join(os.path.expanduser("~"),"Documents","MediaBOTS","InstagramBOT","users")):
				os.mkdir(os.path.join(os.path.expanduser("~"),"Documents","MediaBOTS","InstagramBOT","users"))
except:
	print("[Error] You don't have write permission under '{}' Folder!!\r\nExiting.....".format(os.path.join(os.path.expanduser("~"),"Documents")))
	time.sleep(30)
	sys.exit()
	
url_follow = "https://www.instagram.com/web/friendships/%s/follow/"
url_unfollow = "https://www.instagram.com/web/friendships/%s/unfollow/"
url_home = "https://www.instagram.com/"
url_login = "https://www.instagram.com/accounts/login/ajax/"
url_user_detail = "https://www.instagram.com/%s/"


list_of_ua = ['Mozilla/5.0 (BB10; Touch) AppleWebKit/537.10+ (KHTML, like Gecko) Version/10.0.9.2372 Mobile Safari/537.10+', 'Mozilla/5.0 (PlayBook; U; RIM Tablet OS 2.1.0; en-US) AppleWebKit/536.2+ (KHTML like Gecko) Version/7.2.1.0 Safari/536.2+', 'Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30', 'Mozilla/5.0 (Linux; U; Android 4.1; en-us; GT-N7100 Build/JRO03C) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30', 'Mozilla/5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30', 'Mozilla/5.0 (Linux; U; en-us; KFAPWI Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Silk/3.13 Safari/535.19 Silk-Accelerated=true', 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; LGMS323 Build/KOT49I.MS32310c) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3329.0 Mobile Safari/537.36', 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 550) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/14.14263', 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 950) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/14.14263', 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 10 Build/MOB31T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3329.0 Safari/537.36', 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3329.0 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3329.0 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 7.1.1; Nexus 6 Build/N6F26U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3329.0 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 8.0.0; Nexus 5X Build/OPR4.170623.006) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3329.0 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 8.0.0; Nexus 6P Build/OPP3.170518.006) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3329.0 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 7 Build/MOB30X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3329.0 Safari/537.36', 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 10 Build/MOB31T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3329.0 Safari/537.36', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.0; Trident/6.0; IEMobile/10.0; ARM; Touch; NOKIA; Lumia 520)', 'Mozilla/5.0 (MeeGo; NokiaN9) AppleWebKit/534.13 (KHTML, like Gecko) NokiaBrowser/8.5.0 Mobile Safari/534.13', 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1', 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53', 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3329.0 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3329.0 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3329.0 Mobile Safari/537.36', 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1', 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1', 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1', 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1', 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1', 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1']
'''
list_of_ua = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FSL 7.0.6.01001)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FSL 7.0.7.01001)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FSL 7.0.5.01003)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0",
        "Mozilla/5.0 (X11; U; Linux x86_64; de; rv:1.9.2.8) Gecko/20100723 Ubuntu/10.04 (lucid) Firefox/3.6.8",
        "Mozilla/5.0 (Windows NT 5.1; rv:13.0) Gecko/20100101 Firefox/13.0.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:11.0) Gecko/20100101 Firefox/11.0",
        "Mozilla/5.0 (X11; U; Linux x86_64; de; rv:1.9.2.8) Gecko/20100723 Ubuntu/10.04 (lucid) Firefox/3.6.8",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 1.0.3705)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)",
        "Opera/9.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.01",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows NT 5.1; rv:5.0.1) Gecko/20100101 Firefox/5.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv:5.0) Gecko/20100101 Firefox/5.02",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.112 Safari/535.1",
        "Mozilla/4.0 (compatible; MSIE 6.0; MSIE 5.5; Windows NT 5.0) Opera 7.02 Bork-edition [en]",
]
'''
##user_agent = "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.112 Safari/535.1"
accept_language = "en-US,en;q=0.5"

session = requests.Session()

class Instagram(object):
	def __init__(self): # constructor
		#@temp
		self.userid = ""
		self.username = "coderskey_com"
		self.password = "ig12345678"
		self.proxy = ""
		self.user_agent = random.sample(list_of_ua, 1)[0]
		
		self.s = requests.Session()
		self.c = requests.Session()
		self.s.headers.update(
		{
		"Accept": "*/*",
		"Accept-Language": "en-US,en;q=0.5",
		"Accept-Encoding": "gzip, deflate, br",
		"Connection": "keep-alive",
		"Host": "www.instagram.com",
		"Origin": "https://www.instagram.com",
		"Referer": "https://www.instagram.com/",
		"User-Agent": user_agent,
		"X-Instagram-AJAX": "1",
		"Content-Type": "application/x-www-form-urlencoded",
		"X-Requested-With": "XMLHttpRequest",
		}
		)
		
		self.successful_login = False
		self.after_challenge = False
	def login(self):
		login_post = {"username": self.username,"password": self.password}
		try:
			r = self.s.get(url_home,verify=False)
			if r.status_code == 200:
				csrf_token = r.cookies['csrftoken'] #OR >>> csrf_token = re.search('(?<="csrf_token":")\w+', r.text).group(0)
				self.s.headers.update({"X-CSRFToken": csrf_token})
				time.sleep(5 * random.random())
				try:
					login = self.s.post(url_login, data=login_post, allow_redirects=True,verify=False)
					if login.status_code == 200:
						loginResponse = login.json()
						print (loginResponse) #>>> {'authenticated': True, 'oneTapPrompt': False, 'userId': '1449233XXXX', 'user': True, 'status': 'ok', 'fr': 'ASCuL-zoly1k7LnRY_sv9h8ZXtb_JgyQMV40LK-x0MUANeG3kbjzf0z6f-WMl9jsmJ9qndc7FLaZ2VJx26joGQqFDJ9Glj1KBnzGcNGQUzHOH0fu7vd0YfEUE108U-xxxxxxxxx'}
						if loginResponse.get("authenticated") is True:
							self.userid = loginResponse.get('userId')
							self.s.headers.update({"X-CSRFToken": login.cookies["csrftoken"]})
							rollout_hash = re.search('(?<="rollout_hash":")\w+', r.text).group(0)
							self.s.headers.update({"X-Instagram-AJAX": rollout_hash})
							self.successful_login = True
							self.s.cookies["ig_vw"] = "1536"
							self.s.cookies["ig_pr"] = "1.25"
							self.s.cookies["ig_vh"] = "772"
							self.s.cookies["ig_or"] = "landscape-primary"
							try:
								r2 = self.s.get(url_home,verify=False)
								if self.username in r2.text:
									print ("Logged in successfully!")
								else:
									print ("[Error] Login Failed!")
									app_exit()
							except:
								print ("[Error] Instagram login() EXCEPTION (level-3)")
								app_exit()
						else:
							print ("[Error] Account login filed! \r\n(json : {})".format(loginResponse))
							app_exit()
					elif login.status_code == 400 and login.json()['message'] == 'checkpoint_required':
						if not self.after_challenge:
							self.after_challenge = True
							print("[Interrupted] To login, you required to verify your IG account")
							print("would you like to verify your account through? \nOptions:-\n1)Email Code\n2)SMS Code")
							verify_choice = input("Enter 1 or 2 : ")
							verify_options = {"1":"Email","2":"Mobile"}
							if verify_choice not in ["1","2"]: 
								verify_choice = "1"
							try:
								login2 = self.s.post(url_home[:-1]+login.json()["checkpoint_url"], data={'choice':verify_choice}, allow_redirects=True,verify=False)
								if login2.status_code == 200 and login2.json()['status'] == "ok":
									security_code =  input("Check your {} Enter the CODE : ".format(verify_options[verify_choice]))
									try:
										login3 = self.s.post(login2.url, data={'security_code':security_code}, allow_redirects=True,verify=False)
										if login3.status_code == 200 and login3.json()['status'] == "ok":
											print("Processing IG Login Challenge.....")
											self.login()
										else:
											print("[Error] IG Login Challenge Not working at (stage-2)")
											app_exit()
									except:
										print ("[Error] Instagram login() EXCEPTION (level-4)")
										app_exit()
								else:
									print("[Error] IG Login Challenge Not working at (stage-1)")
									app_exit()
							except:
								print ("[Error] Instagram login() EXCEPTION (level-3)")
								app_exit()
						else:
							print("[Error] IG Login Challenge Failed!!")
							app_exit()
					else:
						print ("[Error] Instagram POST request not made! \r\n(status_code : {})".format(login.status_code))
						app_exit()
				except:
					print ("[Error] Instagram login() EXCEPTION (level-2)")
					app_exit()
			else:
				print ("[Error] Instagram page not connecting! \r\n(status_code : {})".format(r.status_code))
				app_exit()
		except:
			print ("[Error] Instagram login() EXCEPTION (level-1)")
			app_exit()


	

def get_user_id_by_username(user_name):  # no login required
	id_user = "";is_private = False
	url_info = url_user_detail % (user_name)
	resp,excep = session_func(c,url_info+"?__a=1")
	if not exception:
		if resp and resp.status_code == 200:
			id_user = resp.json()["graphql"]["user"]["id"]
			is_private = bool(resp.json()["graphql"]["user"]["is_private"])
			resp.json()["graphql"]["user"]["is_verified"]
			resp.json()["graphql"]["user"]["is_business_account"]
			resp.json()["graphql"]["user"]["edge_follow"]["count"]
			resp.json()["graphql"]["user"]["edge_followed_by"]["count"]
			resp.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["count"]
			resp.json()["graphql"]["user"]["is_joined_recently"]
		elif resp.status_code == 404:
			print("[Error] No User Found!")
		else:
			print("[Error] {} Page not responding properly! \r\nStatus Code: {}".format(resp.url,resp.status_code))
	else:
		print("[Exception(Exception)] ")
	return id_user,is_private
	
def get_user_id_by_username_(user_name):
	id_user = "";is_private = False
	url_info = url_user_detail % (user_name)
	try:
		info = s.get(url_info+"?__a=1",verify=False)
		if info.status_code == 200:
			id_user = info.json()["graphql"]["user"]["id"]
			is_private = bool(info.json()["graphql"]["user"]["is_private"])
			info.json()["graphql"]["user"]["is_verified"]
			info.json()["graphql"]["user"]["is_business_account"]
			info.json()["graphql"]["user"]["edge_follow"]["count"]
			info.json()["graphql"]["user"]["edge_followed_by"]["count"]
			info.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["count"]
			info.json()["graphql"]["user"]["is_joined_recently"]
		elif info.status_code == 404:
			print("[Error] No User Found!")
		else:
			print("[Error] Page not responding properly!")
	except:
		print("[Error] Exception!")
	return id_user,is_private

target_user_id = "290023231"
url_follow_ = url_follow % (target_user_id)
#target_username = "realmadrid"
follow = s.post(url_follow_,verify=False)
follow.url
follow.json()
{'status': 'ok', 'result': 'following'}

url_unfollow_ = url_unfollow % (target_user_id)

unfollow = s.post(url_unfollow_,verify=False)
unfollow.json()
follow_hash = s.post('https://www.instagram.com/web/tags/follow/coding/',verify=False)
follow_hash.json()
unfollow_hash = s.post('https://www.instagram.com/web/tags/unfollow/ok/',verify=False)
follow_hash.json()

##
delete = s.post("https://www.instagram.com/create/2072513329842374187/delete/",allow_redirects=True,verify=False)
##

url_expolre = 'https://www.instagram.com/graphql/query/?query_hash=ecd67af449fb6edab7c69a205413bfa7&variables={"first":"24","after":"1"}'
print(quote(url_expolre))
print(urllib.quote(url_expolre)) # for python 2.xx

r = s.get(url_expolre,verify=False)
print(unquote(r.url))
print(urllib.unquote(r.url)) # for python 2.xx
data=r.json()
dict_ = dict()
list_ =  list()
data["data"]["user"]["id"]
data["data"]["user"]["profile_pic_url"]
data["data"]["user"]["username"]
int(data["data"]["user"]["edge_web_discover_media"]["page_info"]["end_cursor"])
bool(data["data"]["user"]["edge_web_discover_media"]["page_info"]["has_next_page"])
	
counter=0
for count,i in enumerate(data.get("data").get("user").get("edge_web_discover_media").get("edges")):
	img_urls = []
	print(count)
	print(i["node"]["owner"]["id"])
	print(i["node"]["shortcode"])
	if i["node"]["__typename"] == "GraphSidecar":
		for j in i['node']['edge_sidecar_to_children']['edges']:
			print(j['node']['display_url'])
			img_urls.append(j['node']['display_url'])
	else:
		print(i["node"]["display_url"])
		img_urls.append(i["node"]["display_url"])
	#dict_["id"] = i["node"]["shortcode"]
	#list_.append(i["node"]["shortcode"])
	try:
		print(i["node"]["accessibility_caption"])
	except:
		pass
	print(i["node"]["edge_media_to_comment"]["count"])
	print(i["node"]["edge_liked_by"]["count"])
	#print(i["node"]["edge_media_preview_like"]["count"])
	print(i["node"]["dimensions"])
	print(datetime.utcfromtimestamp(i["node"]["taken_at_timestamp"]).strftime('%Y-%m-%d %H:%M:%S'))
	#t1=datetime.utcfromtimestamp(1565819791).replace(microsecond=0)
	#t2=datetime.now().replace(microsecond=0)
	#print("taken {} days ago".format((t2-t1).days))
	#print(i["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"].encode("utf-8"))
	print(i["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"].encode("ascii",errors="ignore"))
	print(i["node"]["thumbnail_src"])
	print(i["node"]["__typename"])
	print(i["node"]["is_video"])
	print(i["node"]["comments_disabled"])
	#hashtags list -> [_each for _each in post["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"].strip().split("\n")[-1].split(" ") if _each.startswith("#")]
	
	#Download media image
	s2=requests.Session()
	for img_url in img_urls:
		with open("image{}.{}".format(counter,img_url.split("?")[0].split(".")[len(img_url.split("?")[0].split("."))-1]),"wb") as f:
			f.write(s2.get(img_url,verify=False).content)
		counter+=1
	s2.close()
	print("-")
	

#Download a Video
p=s.get('https://www.instagram.com/p/BzKB4G6FOlu/',verify=False)
video_url = re.search('(?<="video_url":")[a-zA-Z0-9:/.=?_-]+', p.text).group(0)
video_view_count = re.search('(?<="video_view_count":)[0-9]+', p.text).group(0)
s2=requests.Session()
with open("video{}.{}".format(1,video_url.split("?")[0].split(".")[len(video_url.split("?")[0].split("."))-1]),"wb") as f:
		f.write(s2.get(video_url,verify=False).content)
s2.close()

####
public = "f2405b236d85e8296cf30347c9f08c2a"
target_id = "524226044"
after = "QVFBZ0ZCMV9SOWJzRXAyTXJYT3hacFdKaENkWmFZVDB0SGpONUlITDFxSDNIanFMclVSaEpiTUJZajVDXzB2dWx2bVJnVDBLWHlvSWFJamViMXo4Z1hWNw=="
url_post = 'https://www.instagram.com/graphql/query/?query_hash='+public+'&variables={"id":"'+target_id+'","first":12,"after":"'+after+'"}'
print(quote(url_post))
print(urllib.quote(url_post)) # for python 2.xx

session = requests.Session()
request = session.get(url_post,verify=False)
print(unquote(request.url))
print(urllib.unquote(request.url)) # for python 2.xx
data=request.json()

bool(data["data"]["user"]['edge_owner_to_timeline_media']['page_info']['has_next_page'])
after = data["data"]["user"]['edge_owner_to_timeline_media']['page_info']['end_cursor']
	
counter=0
for count,i in enumerate(data.get("data").get("user").get("edge_owner_to_timeline_media").get("edges")):
	img_urls = list()
	print(count)
	print(i["node"]["shortcode"])
	print(i["node"]["__typename"])
	if i["node"]["__typename"] == "GraphSidecar":
		for j in i['node']['edge_sidecar_to_children']['edges']:
			print(j['node']['display_url'])
			img_urls.append(j['node']['display_url'])
	else:
		print(i["node"]["display_url"])
		img_urls.append(i["node"]["display_url"])
	try:
		print(i["node"]["accessibility_caption"])
	except:
		pass
	print(i["node"]["edge_media_to_comment"]["count"])
	print(i["node"]["edge_media_preview_like"]["count"])
	print(i["node"]["dimensions"])
	print(datetime.utcfromtimestamp(i["node"]["taken_at_timestamp"]).strftime('%Y-%m-%d %H:%M:%S'))
	if len(i["node"]["edge_media_to_caption"]["edges"]):
		#print(i["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"].encode("utf-8"))
		print(i["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"].encode("ascii",errors="ignore"))
	print(i["node"]["is_video"])
	print(i["node"]["comments_disabled"])
	print(i['node']['owner']['username']) #x
	print(i['node']['owner']['id'])
	print(i['node']['location']) #x
	
	#Download media image
	s2=requests.Session()
	for img_url in img_urls:
		with open("image{}.{}".format(counter,img_url.split("?")[0].split(".")[len(img_url.split("?")[0].split("."))-1]),"wb") as f:
			f.write(s2.get(img_url,verify=False).content)
		counter+=1
	s2.close()
	print("-")
	

##
https://www.instagram.com/explore/people/suggested/
##
	
####
private = "c76146de99bb02f6415203be841dd25a"
target_id = "524226044"
url_followers = 'https://www.instagram.com/graphql/query/?query_hash='+private+'&variables={"id":"'+target_id+'","include_reel":true,"fetch_mutual":true,"first":24}'
print(quote(url_post))
print(urllib.quote(url_post)) # for python 2.xx

r = s.get(url_followers,verify=False)
print(unquote(r.url))
print(urllib.unquote(r.url)) # for python 2.xx
data=r.json()

bool(data['data']['user']['edge_followed_by']['page_info']['has_next_page'])
after = data['data']['user']['edge_followed_by']['page_info']['end_cursor']
data['data']['user']['edge_followed_by']['count']
data['data']['user']['edge_mutual_followed_by']['count']

for count,i in enumerate(data.get("data").get("user").get("edge_followed_by").get("edges")):
	print(count)
	print(i['node']['username'])
	print(i['node']['id'])
	print(i['node']['is_verified'])
	print(i['node']['is_private'])
	print(i['node']['full_name'].encode("ascii",errors="ignore"))
	print(i['node']['followed_by_viewer'])
	print(i['node']['requested_by_viewer'])
	print(i['node']['reel']['owner']['__typename'])
	print("--")

url_followers = 'https://www.instagram.com/graphql/query/?query_hash='+private+'&variables={"id":"'+target_id+'","include_reel":true,"fetch_mutual":true,"first":24,"after":"'+after+'"}'

url_following = "https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables=%7B%22id%22%3A%225973102154%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Afalse%2C%22first%22%3A24%7D"
url_following = "https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables=%7B%22id%22%3A%225973102154%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Afalse%2C%22first%22%3A12%2C%22after%22%3A%22QVFBWklfNzY1WFZmRUlzUXdLX3JZdk5ZU0FRMXpwN3lQVDVBZlp5aEJ1d3VCNHZMLUh0TVo0Q1ZNZkZPdHhMTzBPOXlVTm5uVXl5dE1iUHNsd2JEbENhZQ%3D%3D%22%7D"

def app_exit():
	#Do other jobs before terminating the App 
	sys.exit()
	
def get_follow_list_of_a_username(self,target_user_id,type_):
	
	# checking whether command is to scan followers list or following list
	if type_ == "followers":
		private_hash = "c76146de99bb02f6415203be841dd25a" #for followers
		edge__by = "edge_followed_by"
	else:
		private_hash = "d04b0a864b4b54837c0d870b0e77e076" #for followings
		edge__by = "edge_follow"
	
	url = "https://www.instagram.com/graphql/query/"
	follow_list = []
	id_to_user = dict()
	
	page_num = 1
	has_next_page = True
	after = ""
	first = 24
	print(type_)
	
	while has_next_page:
		print("Scanning {} to {}".format(((page_num-1)*first)+1,(page_num*first-1)+1)
		if not after:
			params = {'query_hash':private_hash,'variables':'{"include_highlight_reels":false,"include_reel":true,"id":'+target_user_id+',"fetch_mutual":true,"first":'+str(first)+'}'}
		else:
			params = {'query_hash':private_hash,'variables':'{"include_highlight_reels":false,"include_reel":true,"id":'+target_user_id+',"fetch_mutual":true,"first":'+str(first)+',"after":"'+after+'"}'}
		time.sleep(random.randint(5,10))
		try:
			r = self.s.get(url,params=params,allow_redirects=False,verify=False)
			data = r.json()
			has_next_page = bool(data["data"]["user"][edge__by]["page_info"]["has_next_page"])
			if has_next_page:
				after = data["data"]["user"][edge__by]["page_info"]["end_cursor"]
			user_lists = data["data"]["user"][edge__by]["edges"]	
			for user in user_lists:
				id_to_user[user["node"]["id"]] = user["node"]["username"]
				follow_list.append(user["node"]["id"])
		except:
			print("[Error] error")
			app_exit()
		page_num+=1
	# End of while loop
	
	follow_usernames = [id_to_user[i] for i in follow_list]
	print ("[{}] {} users found".format( type_,len( follow_usernames ) ) )
	return follow_list,follow_usernames
			
def get_followback_list_of_a_username(self,target_user_id):

	url = "https://www.instagram.com/graphql/query/"
	
	follow_list = [[],[]]
	id_to_user = dict()
	private = ["c76146de99bb02f6415203be841dd25a","d04b0a864b4b54837c0d870b0e77e076"]
	
	for index,private_hash in enumerate(private):

		edge__by = ["edge_followed_by","edge_follow"][index]
		print ("{}".format(edge__by[5:]))
		
		page_num = 1
		has_next_page = True
		after = ""
		
		while has_next_page:
			print("Scanning {} to {}".format((page_num-1)*24,page_num*24-1))
			if not after:
				params = {'query_hash':private_hash,'variables':'{"include_highlight_reels":false,"include_reel":true,"id":'+target_user_id+',"fetch_mutual":true,"first":24}'}
			else:
				params = {'query_hash':private_hash,'variables':'{"include_highlight_reels":false,"include_reel":true,"id":'+target_user_id+',"fetch_mutual":true,"first":24,"after":"'+after+'"}'}
			time.sleep(random.randint(5,10))
			try:
				r = self.s.get(url,params=params,allow_redirects=False,verify=False)
				data = r.json()
				has_next_page = bool(data["data"]["user"][edge__by]["page_info"]["has_next_page"])
				if has_next_page:
					after = data["data"]["user"][edge__by]["page_info"]["end_cursor"]
				user_lists = data["data"]["user"][edge__by]["edges"]	
				for user in user_lists:
					#user["node"]["is_private"]
					if index == 0:
						id_to_user[user["node"]["id"]] = user["node"]["username"]
					follow_list[index].append(user["node"]["id"])
			except:
				print("[Error] error")
				app_exit()
			page_num+=1
		# End of while loop
	# End of for loop
	followback_userids = list(set(follow_list[0]) & set(follow_list[1]))
	followback_usernames = [id_to_user[i] for i in followback_userids]
	print ("[FollowBack] {} users found".format( len( followback_userids ) ) )
	return followback_userids,followback_usernames

url_comments = "https://www.instagram.com/graphql/query/?query_hash=97b41c52301f77ce508f55e66d17620e&variables=%7B%22shortcode%22%3A%22BzdGFwvFFwM%22%2C%22first%22:%2212%22%7D"
url_comments = "https://www.instagram.com/graphql/query/?query_hash=97b41c52301f77ce508f55e66d17620e&variables=%7B%22shortcode%22%3A%22BzdGFwvFFwM%22%2C%22first%22:%2212%22,%22after%22:%22{\%22cached_comments_cursor\%22:%20\%2217983731223256832\%22,%20\%22bifilter_token\%22:%20\%22KGEAgJcjbuRwPwBh-OpPJXY_AOLUwug_9j8ACfrTUFscQABr1X2udiBAAG2l9xbRO0AAsctNeMR3PwCzG3vp4yNAAJQvKuAaLEAANpmGUSYVQACa3PHnSoo_AN1w1a_UZz8AAA==\%22}%22%7D"

#edge_liked_by , edge_threaded_comments

url_liked = "https://www.instagram.com/graphql/query/?query_hash=d5d763b1e2acf209d62d22d184488e57&variables=%7B%22shortcode%22%3A%22Bzc_WMYgzoZ%22%2C%22include_reel%22%3Atrue%2C%22first%22%3A24%7D"
url_liked = "https://www.instagram.com/graphql/query/?query_hash=d5d763b1e2acf209d62d22d184488e57&variables=%7B%22shortcode%22%3A%22Bzc_WMYgzoZ%22%2C%22include_reel%22%3Atrue%2C%22first%22%3A24,%22after%22:%22QVFDVUp5TlZ2YTVuNzlrcXZwZndSZlMtTEo2QTcwUzI0MGhxWWptdjJTTnVsajIySVZySkE0OFVBN3FVVEdXQldjZExCWEl0dHNyWHctZFB6S2Y3bzlwRw==%22%7D"


url_graphql = "https://www.instagram.com/graphql/query/"

def get_post_details(shortcode,about,type):
	#variables
	page_num = 1
	has_next_page = True
	after = ""
	
	if about == "comments":
		hash = "97b41c52301f77ce508f55e66d17620e" #hash is public
		edge__by = "edge_media_to_parent_comment"
		first = 12
	elif about == "likes" :
		hash = "d5d763b1e2acf209d62d22d184488e57" #hash is public
		edge__by = "edge_liked_by"
		first = 24

	list_username = []
	while has_next_page:
		print("Scanning {} to {}".format(((page_num-1)*first)+1,(page_num*first-1)+1))
		if not after:
			params = {'query_hash':hash,'variables':'{"first":'+str(first)+',"shortcode":"'+shortcode+'"}'}
		else:
			params = {'query_hash':hash,'variables':'{"first":'+str(first)+',"shortcode":"'+shortcode+'","after":"'+str(after)+'"}'}
		if about == "likes":
			params.update({'variables':params["variables"][:-1]+',"include_reel":true}'})
		resp,excep = session_func("",url_graphql,redirects=False,params=params,data=None)
		if not excep:
			if resp and resp.status_code == 200:
				data = resp.json()
				if type == "stat":
					return data["data"]["shortcode_media"][edge__by]["count"]
				has_next_page = bool(data["data"]["shortcode_media"][edge__by]["page_info"]["has_next_page"])
				if has_next_page:
					after = data["data"]["shortcode_media"][edge__by]["page_info"]["end_cursor"]
				if about == "comments":
					list_username += list(each["node"]["owner"]["username"] for each in data["data"]["shortcode_media"][edge__by]["edges"])
				else:
					list_username += list(each["node"]["username"] for each in data["data"]["shortcode_media"][edge__by]["edges"])
			else:
				print("[Error] {} Page not responding properly! \r\nStatus Code: {}".format(resp.url,resp.status_code))
		else:
			print("[Exception] Exception! <during : find_suitable_users()>")
		
	return list_username
	
def get_instagram_url_from_media_id(media_id):
	shortened_id = ""
	media_id = int(media_id)
	alphabet = (
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
        )
	while media_id:
            media_id, idx = divmod(media_id, 64)
            shortened_id = alphabet[idx] + shortened_id
	return "https://instagram.com/p/{}/".format(shortened_id)

from base64 import b64decode, b64encode	
def shortcode_to_mediaid(code: str) -> int:
        if len(code) > 11:
            raise InvalidArgumentException("Wrong shortcode \"{0}\", unable to convert to mediaid.".format(code))
        code = 'A' * (12 - len(code)) + code
        return int.from_bytes(b64decode(code.encode(), b'-_'), 'big')
		
path_app_directory = os.path.join(os.path.expanduser("~"),"Documents","MediaBOTS","InstagramBOT")

id_to_user = dict()
if os.path.exists(os.path.join(path_app_directory,"userid to username.txt")):
	path = os.path.join(path_app_directory,"userid to username.txt")
	f = open(path,"r").read()
	if f:
		for each in f.split("\n"):
			if each:
				id_to_user[each.split(":")[0]]=each.split(":")[1]
	
def get_username_by_user_id(user_id): # no login required
	global id_to_user
	user_id = str(user_id)
	user_name = ""
	if user_id in id_to_user:
		return id_to_user[user_id] #   if username already fetched in the current session
	session = requests.Session()
	headers = {'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.8','Accept': '*/*', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36', 'Connection': 'keep-alive','X-Requested-With': 'XMLHttpRequest'}
	try:	
		params = {'query_hash':'7c16654f22c819fb63d1183034a5162f','variables':'{"include_highlight_reels":false,"include_reel":true,"user_id":'+user_id+',"include_chaining":false,"include_suggested_users":false,"include_logged_out_extras":false}'}		
		r = session.get("https://www.instagram.com/graphql/query",params=params,headers=headers,allow_redirects=False,verify=False)
		if r.status_code == 200 and r.json()["status"] == "ok":
			user_name = r.json()["data"]["user"]["reel"]["owner"]["username"]
			id_to_user[user_id] = user_name #   stored in dictionary, in case it need to be fetched again
			with open(os.path.join(path_app_directory,"userid to username.txt"),"a+") as f:
				f.write("{}:{}\n".format(user_id,user_name))
	except (requests.exceptions.ConnectionError,requests.exceptions.RequestException,requests.exceptions.Timeout,requests.exceptions.TooManyRedirects) as err:
		print (err)
	except:
		print("Exception occurred!")
	session.close()
	return user_name
	

###
from PIL import Image
import piexif
import datetime

def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()

print(get_exif(r"c:\python34\exif.jpg"))
image = Image.open(r"c:\python34\exif.jpg")
image = image.transpose(Image.FLIP_LEFT_RIGHT) 
image_clean = Image.new(image.mode, image.size)
image_clean.putdata(list(image.getdata()))
image_clean.save(r"c:\python34\exif_clean.jpg")
print(get_exif(r"c:\python34\exif_clean.jpg"))


def insert_tag(filename):
	##zeroth_ifd = {269: "test title"}
	##zeroth_ifd[270] = "test descript"
	##exif_bytes = piexif.dump({"0th":zeroth_ifd})
	##piexif.insert(exif_bytes,filename)
	im = Image.open(filename)
	try:
		#exif_dict = piexif.load(im.info["exif"])
		exif_dict = {}
		exif_dict["0th"] = {270: b'test title', 271: 'Apple' , 306 : str(datetime.datetime.now()), 315: 'Hola'} #https://www.exiv2.org/tags.html
		exif_bytes = piexif.dump(exif_dict)
		im.save(filename, "jpeg", exif=exif_bytes)
	except:
		print ("error")
	im.close()


insert_tag(r"c:\python34\exif.jpg")


tag_explore = "https://www.instagram.com/explore/tags/nature/?__a=1"


explore ="https://www.instagram.com/graphql/query/?query_hash=ecd67af449fb6edab7c69a205413bfa7&variables=%7B%22first%22%3A24%2C%22after%22%3A%223%22%7D"

# Find/Search suitable users from user own explore, other users comments & likes
def find_suitable_users(self,type_="explore"):
	if not self.successful_login: #if user not logged in yet
		self.login()
	
	if type_ == "explore":
		private_hash = "ecd67af449fb6edab7c69a205413bfa7" #for explore
		edge__by = "edge_web_discover_media"
	else:
		private_hash = "" #for ...
	
	url = "https://www.instagram.com/graphql/query/"
	
	page_num = 1
	has_next_page = True
	after = 0
	
	print(type_)
	
	while has_next_page:
		print("Scanning {} to {}".format(((page_num-1)*24)+1,(page_num*24-1)+1))
		if not after:
			params = {'query_hash':private_hash,'variables':'{"first":24}'}
		else:
			params = {'query_hash':private_hash,'variables':'{"first":24,"after":"'+after+'"}'}
		try:
			resp,excep = session_func(self.session_main,url,redirects=False,params=params,data=None)
			if not excep:
				if resp.status_code == 200:
					data = resp.json()
					has_next_page = bool(data["data"]["user"][edge__by]["page_info"]["has_next_page"])
					if has_next_page:
						after += 1
					post_lists = data["data"]["user"][edge__by]["edges"]	
					for post in post_lists:
						user_id  = post["node"]["owner"]["id"]
						user_name = get_username_by_user_id(user_id)
						if user_name:
							ret = get_user_details(user_name)
							if ret:
								if (self.check_is_private.isChecked() == ret[2]  and self.check_is_non_verified.isChecked() == ret[3] and self.check_is_celebrity.isChecked() == ret[4]):
									if (ret[0] >= int(self.min_followers.text()) and ret[1] <= int(self.max_followers.text()) and ret[0]/ret[1] >= float(self.follow_ratio.text())):
										##pass
										# set this suitable user to myList
										with open(os.path.join(self.path_users_directory,self.username,"myList","follow.txt"),"a+") as f:
											f.write("{},\n".format(user_name))
				else:
					print("[Error] {} Page not responding properly! \r\nStatus Code: {}".format(resp.url,resp.status_code))
			else:
				print("[Exception] Exception! <during : find_suitable_users()>")
		except:
			print("[Exception] error <during : find_suitable_users()")
			app_exit()
		page_num+=1
		time.sleep(random.randint(5,10))
	# End of while loop
	return
	
def get_user_details(user_name): # no login required
	resp,excep = session_func("",url_home+user_name+"?__a=1")
	if not excep:
		if resp.status_code == 200:
			data = resp.json()
			user = data["graphql"]["user"]
			return (user["edge_followed_by"]["count"],user["edge_follow"]["count"],user["is_private"],user["is_verified"],user["is_business_account"],user['full_name'])
		elif resp.status_code == 404:
			print("[Error] No User Found!")
		else:
			print("[Error] {} Page not responding properly! \r\nStatus Code: {}".format(resp.url,resp.status_code))
	else:
		print("[Exception] Exception!")
	return False
	
def session_func(s,url,redirects=True,params=None,data=None):
	session_passed = True
	response = None
	if not s:
		s = requests.Session()
		session_passed =  False
	get = False
	tried = 1
	while not get and tried <= 3:
		#status_code = 200
		exception = False
		try:
			print ("[{}] Visiting {}".format(tried,url))
			response = s.get(url,allow_redirects=redirects,params=params,verify=False)
			if response.status_code == 200:
				get = True
			else:
				pass
				#status_code = response.status_code
		except:
			exception = True
		time.sleep(1*tried)
		tried+=1
	if not session_passed:
		s.close()
	return response,exception
	
############# POST ing via Instagram App , need to take care of random guid,uuid,device id,OS etc 
import uuid
from requests_toolbelt import MultipartEncoder
import hashlib
import urllib
import hmac
from PIL import Image

def generateSignature(self, data, skip_quote=False):
	if not skip_quote:
		try:
			parsedData = urllib.parse.quote(data)
		except AttributeError:
			parsedData = urllib.quote(data)
	else:
		parsedData = data
	return 'ig_sig_key_version=' + self.SIG_KEY_VERSION + '&signed_body=' + hmac.new(self.IG_SIG_KEY.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest() + '.' + parsedData

def generateUUID(type):
	generated_uuid = str(uuid.uuid4())
	if (type):
		return generated_uuid
	else:
		return generated_uuid.replace('-', '')
	
def generateDeviceId(seed):
	volatile_seed = "12345"
	m = hashlib.md5()
	m.update(seed.encode('utf-8') + volatile_seed.encode('utf-8'))
	return 'android-' + m.hexdigest()[:16]

def id_generator_alnum(size, chars=string.digits+string.ascii_lowercase+string.ascii_uppercase,lower_case_only=False):
	if lower_case_only:
		chars=string.digits+string.ascii_lowercase
	return ''.join(random.choice(chars) for _ in range(size))
	
self.API_URL = 'https://i.instagram.com/api/v1/'
DEVICE_SETTINTS = {'manufacturer': 'Xiaomi',
'model': 'HM 1SW',
'android_version': 18,
'android_release': '4.3'}
self.DEVICE_SETTINTS = DEVICE_SETTINTS
self.USER_AGENT = 'Instagram 10.26.0 Android ({android_version}/{android_release}; 320dpi; 720x1280; {manufacturer}; {model}; armani; qcom; en_US)'.format(**DEVICE_SETTINTS)
#self.USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'

self.isLoggedIn = False
m = hashlib.md5()
m.update(self.username.encode('utf-8') + self.password.encode('utf-8'))


self.device_id = generateDeviceId(m.hexdigest())

upload_id = str(int(time.time() * 1000))
photo = r"pending_media_%s.jpg" %upload_id
os.path.exists(photo)
self.uuid = generateUUID(True)

csrf_token = id_generator_alnum(32)
self.token = csrf_token

#login
data = {'phone_id': generateUUID(True),
'_csrftoken': self.token,
'username': self.username,
'guid': self.uuid,
'device_id': self.device_id,
'password': self.password,
'login_attempt_count': '0'}

self.s = requests.Session()
self.s.headers.update({'Connection': 'close',
'Accept': '*/*',
'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
'Cookie2': '$Version=1',
'Accept-Language': 'en-US',
'User-Agent': self.USER_AGENT})

login = self.s.post(self.API_URL + 'accounts/login/', data=data, verify=False)
self.LastResponse = login
self.LastJson = json.loads(login.text)
if login.status_code == 200:
	self.isLoggedIn = True
	self.username_id = self.LastJson["logged_in_user"]["pk"]
	self.rank_token = "%s_%s" % (self.username_id, self.uuid)
	self.token = self.LastResponse.cookies["csrftoken"]
	print("Login success!\n")
#upload
data = {'upload_id': upload_id,
'_uuid': self.uuid,
'_csrftoken': self.token,
'image_compression': '{"lib_name":"jt","lib_version":"1.3.0","quality":"87"}',
'photo': ('pending_media_%s.jpg' % upload_id, open(photo, 'rb'), 'application/octet-stream', {'Content-Transfer-Encoding': 'binary'})}

m = MultipartEncoder(data, boundary=self.uuid)

self.s.headers.update({'X-IG-Capabilities': '3Q4=',
'X-IG-Connection-Type': 'WIFI',
'Cookie2': '$Version=1',
'Accept-Language': 'en-US',
'Accept-Encoding': 'gzip, deflate',
'Content-type': m.content_type,
'Connection': 'close',
'User-Agent': self.USER_AGENT})

upload = self.s.post(self.API_URL + "upload/photo/", data=m) # OR m.to_string()

caption = "write text"	
poster_ = Image.open(photo)
(w, h) = poster_.size
poster_.close()
	
#self.IG_SIG_KEY = '4f8732eb9ba7d1c8e8897a75d6474d4eb3f5279137431b2aafb71fafe2abe178'
self.IG_SIG_KEY = id_generator_alnum(64,lower_case_only=True)
self.SIG_KEY_VERSION = '4'			

self.s.headers.update({'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8'})
		
if upload.status_code == 200:
	data = {'_csrftoken': self.token,
	'media_folder': 'Instagram',
	'source_type': 4,
	'_uid': self.username_id,
	'_uuid': self.uuid,
	'caption': caption,
	'upload_id': upload_id,
	'device': DEVICE_SETTINTS,
	'edits': {
	   'crop_original_size': [w * 1.0, h * 1.0],
	   'crop_center': [0.0, 0.0],
	   'crop_zoom': 1.0
	},
	'extra': {
	   'source_width': w,
	   'source_height': h
	}}
	##configured = self.s.post(self.API_URL + 'media/configure/',data=data, verify=False)
	#configured = self.s.post(self.API_URL + 'media/configure/?', data=data, verify=False)
	#configured = self.s.post(self.API_URL + 'media/configure/?',params=urllib.parse.quote(json.dumps(data)), verify=False)
	configured = self.s.post(self.API_URL + 'media/configure/?',data=generateSignature(self,json.dumps(data)), verify=False)
	
	
	
	'''
	
	upload_id = str(int(time.time() * 1000))

upload_url = "https://www.instagram.com/rupload_igphoto/fb_uploader_%s"%upload_id
self.session_main.headers.update({"Accept-Language":"en-GB,en-US;q=0.9,en;q=0.8"})


self.session_main.cookies.pop("rur")
self.session_main.cookies["rur"] = "FRC"
self.session_main.cookies["ig_direct_region_hint"] = "PRN"


Cookie: 
mid=XJJ32QAEAAGzZjwy6XUTkfOqYyNj; 
shbid=19217; 
csrftoken=X2K5RYWo0gB0C9lLYAqjyxGpFTn7nyXS; 
ds_user_id=14492339811; 
sessionid=14492339811%3A6ihNUZVgK6VtCO%3A17; 
shbts=1569638322.6839757; 
ig_direct_region_hint=PRN; 
datr=JRKRXcLqbR8KJTnTbDhF8tdA; 
rur=FRC; 
urlgen="{\"117.203.144.14\": 9829}:1iEppq:Ic_9ZA-f0zulfKHNFpMluka1WO0"

self.session_main.headers["Sec-Fetch-Mode"] =  "cors"
self.session_main.headers["Sec-Fetch-Site"] = "same-origin"


curl "https://www.instagram.com/rupload_igphoto/fb_uploader_1569844631501" -H "sec-fetch-mode: cors" -H "origin: https://www.instagram.com" 
-H "x-ig-www-claim: hmac.AR1JeV2sV2A3xfqFYLQcGS_2QV_QF8DplquoJ0o8ltDOB2MA" -H "accept-language: en-GB,en-US;q=0.9,en;q=0.8" 
-H "x-csrftoken: X2K5RYWo0gB0C9lLYAqjyxGpFTn7nyXS" 
-H "user-agent: Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1" 
-H "x-requested-with: XMLHttpRequest" -H "cookie: mid=XJJ32QAEAAGzZjwy6XUTkfOqYyNj; shbid=19217; csrftoken=X2K5RYWo0gB0C9lLYAqjyxGpFTn7nyXS;
 ds_user_id=14492339811; sessionid=14492339811^%^3A6ihNUZVgK6VtCO^%^3A17; shbts=1569638322.6839757; ig_direct_region_hint=PRN; datr=JRKRXcLqbR8KJTnTbDhF8tdA; 
 rur=FRC;
 urlgen=^\^"^{^\^\^\^"117.203.144.14^\^\^\^": 9829^\^\054 ^\^\^\^"117.226.210.36^\^\^\^": 9829^\^\054 ^\^\^\^"45.248.177.88^\^\^\^": 9829^}:1iEuIf:
 VpgANKStyP1hc8qp5qLuDv7Qvoc^\^""
 -H "x-ig-app-id: 1217981644879628" -H "x-entity-name: fb_uploader_1569844631501" -H "offset: 0" -H "accept-encoding: gzip, deflate, br" 
 -H "x-instagram-ajax: 667362966597" -H "content-type: image/jpeg" -H "accept: */*" -H "referer: https://www.instagram.com/create/details/" 
 -H "authority: www.instagram.com" -H "x-instagram-rupload-params: 
 ^{^\^"media_type^\^":1,^\^"upload_id^\^":^\^"1569844631501^\^",^\^"upload_media_height^\^":1080,^\^"upload_media_width^\^":1080^}"
 -H "sec-fetch-site: same-origin" -H "x-entity-length: 34321" --data-binary ^"^ÿ^Ø^ÿ^à^

	'''
#### Post ing via Python (tracked by Fiddler)
import emojis

self = dialog
self.login()

upload_id = str(int(time.time() * 1000))

upload_url = "https://www.instagram.com/rupload_igphoto/fb_uploader_%s"%upload_id
self.session_main.headers.update({"Accept-Language":"en-GB,en-US;q=0.9,en;q=0.8"}) # x


self.session_main.cookies.pop("rur") # x
self.session_main.cookies["rur"] = "FRC" # x
self.session_main.cookies["ig_direct_region_hint"] = "PRN" # x
self.session_main.cookies["urlgen"] = "{\"45.248.177.88\": 9829}:1iEw5K:3abn7Bf3VvzfvJriC9wndgbC5oo" # not required
self.session_main.cookies["datr"] = "JRKRXcLqbR8KJTnTbDhF8tdA" # common , not required
self.session_main.cookies["ig_cb"] = "1" # common , not required

self.session_main.headers["Sec-Fetch-Mode"] =  "cors"
self.session_main.headers["Sec-Fetch-Site"] = "same-origin"
self.session_main.headers["Offset"] = "0"
self.session_main.headers["Referer"] = "https://www.instagram.com/create/details/" 
self.session_main.headers["X-IG-App-ID"] = "1217981644879628"  # common app id
self.session_main.headers["X-IG-WWW-Claim"] = "hmac.AR1JeV2sV2A3xfqFYLQcGS_2QV_QF8DplquoJ0o8ltDOB-Bn" # one of fetched from IG 
photo = r"c:\python34\pending_media_%s.jpg"%upload_id
self.session_main.headers["X-Entity-Length"] = str(len(open(photo,"rb").read()))
self.session_main.headers["X-Entity-Name"] = "fb_uploader_%s" %upload_id

from PIL import Image
im = Image.open(photo)
(w,h) = im.size
im.close()

self.session_main.headers["X-Instagram-Rupload-Params"] = json.dumps({"media_type":1,"upload_id":upload_id,"upload_media_height":h,"upload_media_width":w})
self.session_main.headers["Content-Type"]="image/jpeg"

#upload
r=self.session_main.post(upload_url,data=open(photo,"rb").read(),verify=False)
r.json()

# updating headers for configure
self.session_main.headers.pop("X-Instagram-Rupload-Params")
self.session_main.headers.pop("X-Entity-Name")
self.session_main.headers.pop("X-Entity-Length")
self.session_main.headers.pop("Offset")
self.session_main.headers["Content-Type"] = "application/x-www-form-urlencoded" # reset
self.session_main.headers["Referer"] = 'https://www.instagram.com/' # reset
# configure
caption = "new photo\n :ok: :okay: :smile: :cookie: :thumbsup: :smiley: :clap: :snake: :clapper: :morning: \r\n #ok #test #code #python \n @python @doesnotexist"
caption = emojis.encode(caption)
payload = {"upload_id":upload_id,"caption":caption,"usertags":"","custom_accessibility_caption":"","retry_timeout":""}
r2=self.session_main.post("https://www.instagram.com/create/configure/",data=payload,verify=False)

if r2.json()["status"] == "ok":
	r2.json()["media"]["pk"]
	r2.json()["media"]["code"]
	r2.json()["media"]["user"]["username"]
	r2.json()["media"]["taken_at"]

