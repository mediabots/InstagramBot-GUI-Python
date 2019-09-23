''' 
Name :
	InstagramBot
Compatibility :
	Python 2.7.8,
	Python 3.4.0 &
	Python 3.5.0
Architecture : 
	x86/x64 (32bit/64bit)
Written by :
	https://github.com/mediabots
Contact :
	mediabots@mail.ru
GUI Package used in Python:
	PySide/PyQt4
Dependent Python modules:
	requests
License:
	CC/Open-source/Free
Version:
	1.0.2
Release Date:
	23-Aug-2019
'''	

########### Python Modules/Packages
try:
	from PySide.QtCore import *
	from PySide.QtGui import *
	from PySide import QtCore
except:
	from PyQt4.QtCore import *
	from PyQt4.QtGui import *
	from PyQt4 import QtCore
#
import os
import sys
import time

import json
import re
import string
import requests
import pickle
import random
try:
	from urllib.parse import unquote,quote # For python 3
except:
	from urllib import unquote,quote # for Python 2
import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import threading
from threading import Thread
from queue import Queue
import copy
##import psutil # may require in future implementation 

import InstagramBot_ui

# ---------------------

gui_queue = Queue()
os_user_directory = os.path.expanduser("~")
app_version = "1.0.2"
directory_chnaged = False
documents = "Documents"

# Only for Multiple account feature (beta version)
if os.path.exists(os.path.join(os_user_directory,documents,"MediaBOTS","InstagramBOT","multi_enabled.txt")):
	os_user_directory = os.path.abspath(os.curdir)
	directory_chnaged = True
	documents = ""

try:
	if not os.path.exists(os.path.join(os_user_directory,documents,"MediaBOTS")):
		os.mkdir(os.path.join(os_user_directory,documents,"MediaBOTS"))
	if not os.path.exists(os.path.join(os_user_directory,documents,"MediaBOTS","InstagramBOT")):
		os.mkdir(os.path.join(os_user_directory,documents,"MediaBOTS","InstagramBOT"))
	if not os.path.exists(os.path.join(os_user_directory,documents,"MediaBOTS","InstagramBOT","users")):
		os.mkdir(os.path.join(os_user_directory,documents,"MediaBOTS","InstagramBOT","users"))
	if not os.path.exists(os.path.join(os_user_directory,documents,"MediaBOTS","InstagramBOT","others")):
		os.mkdir(os.path.join(os_user_directory,documents,"MediaBOTS","InstagramBOT","others"))
	if not os.path.exists(os.path.join(os_user_directory,documents,"MediaBOTS","InstagramBOT","hashes")):
		os.mkdir(os.path.join(os_user_directory,documents,"MediaBOTS","InstagramBOT","hashes"))
	if not os.path.exists(os.path.join(os_user_directory,documents,"MediaBOTS","InstagramBOT","userid to username.txt")):
		with open(os.path.join(os_user_directory,documents,"MediaBOTS","InstagramBOT","userid to username.txt"),"w") as f:
			f.write("")
	if not os.path.exists(os.path.join(os_user_directory,documents,"MediaBOTS","InstagramBOT","user does not exist.txt")):
		with open(os.path.join(os_user_directory,documents,"MediaBOTS","InstagramBOT","user does not exist.txt"),"w") as f:
			f.write("")
	if not os.path.exists(os.path.join(os_user_directory,documents,"MediaBOTS","InstagramBOT","Logs")):
		os.mkdir(os.path.join(os_user_directory,documents,"MediaBOTS","InstagramBOT","Logs"))
	log_path = os.path.join(os_user_directory,documents,"MediaBOTS","InstagramBOT","Logs",datetime.datetime.now().strftime("%d-%m-%Y")+".txt")
except:
	gui_queue.put("[Error] You don't have write permission under '{}' Folder!!\r\nExiting......".format(os.path.join(os_user_directory,documents)))
	time.sleep(30)
	sys.exit()

#initializing global variables
path_app_directory = os.path.join(os_user_directory,documents,"MediaBOTS","InstagramBOT")

id_to_user = dict()
user_to_id =  dict()

if os.path.exists(os.path.join(path_app_directory,"userid to username.txt")):
	path = os.path.join(path_app_directory,"userid to username.txt")
	f = open(path,"r").read().strip()
	if f:
		for each in f.split("\n"):
			if each:
				id_to_user[each.split(":")[0]]=each.split(":")[1]
				user_to_id[each.split(":")[1]]=each.split(":")[0]

url_follow = "https://www.instagram.com/web/friendships/%s/follow/"
url_unfollow = "https://www.instagram.com/web/friendships/%s/unfollow/"
url_home = "https://www.instagram.com/"
url_login = "https://www.instagram.com/accounts/login/ajax/"
url_user_detail = "https://www.instagram.com/%s/"
url_graphql = "https://www.instagram.com/graphql/query/"
#
list_of_ua = ['Mozilla/5.0 (BB10; Touch) AppleWebKit/537.10+ (KHTML, like Gecko) Version/10.0.9.2372 Mobile Safari/537.10+', 'Mozilla/5.0 (PlayBook; U; RIM Tablet OS 2.1.0; en-US) AppleWebKit/536.2+ (KHTML like Gecko) Version/7.2.1.0 Safari/536.2+', 'Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30', 'Mozilla/5.0 (Linux; U; Android 4.1; en-us; GT-N7100 Build/JRO03C) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30', 'Mozilla/5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30', 'Mozilla/5.0 (Linux; U; en-us; KFAPWI Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Silk/3.13 Safari/535.19 Silk-Accelerated=true', 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; LGMS323 Build/KOT49I.MS32310c) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3329.0 Mobile Safari/537.36', 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 550) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/14.14263', 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 950) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/14.14263', 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 10 Build/MOB31T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3329.0 Safari/537.36', 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3329.0 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3329.0 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 7.1.1; Nexus 6 Build/N6F26U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3329.0 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 8.0.0; Nexus 5X Build/OPR4.170623.006) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3329.0 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 8.0.0; Nexus 6P Build/OPP3.170518.006) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3329.0 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 7 Build/MOB30X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3329.0 Safari/537.36', 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 10 Build/MOB31T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3329.0 Safari/537.36', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.0; Trident/6.0; IEMobile/10.0; ARM; Touch; NOKIA; Lumia 520)', 'Mozilla/5.0 (MeeGo; NokiaN9) AppleWebKit/534.13 (KHTML, like Gecko) NokiaBrowser/8.5.0 Mobile Safari/534.13', 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1', 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53', 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3329.0 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3329.0 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3329.0 Mobile Safari/537.36', 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1', 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1', 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1', 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1', 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1', 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1']
accept_language = "en-US,en;q=0.5"
	
session_temp = requests.Session()
proxies = {}
timeout = 30
shared_resource_lock = threading.Lock()	

my_followers = []
my_following = []
my_following_app = []
bad_usernames = []
exclude_usernames = []

if os.path.exists(os.path.join(path_app_directory,"user does not exist.txt")):
	path = os.path.join(path_app_directory,"user does not exist.txt")
	bad_usernames = open(path,"r").read().strip().split("\n")

####### FUNTIONS #######

def app_exit(): # to exit 
	#Do other jobs before terminating the App 
	sys.exit()
#End of the Function app_exit()

log_counter = 0
def write_me_log(*argv): # LOG text; <imp> shared_resource_lock may cause freezing whole app
	global log_counter,log_path # global access for 'log_path' is not necessary though
	text = ' '.join(str(arg) for arg in argv)
	with threading.Lock():
		with open(log_path,"a+") as log:
			if log_counter in [0,1]:
				log.write("****************** ( Time - {} ) ******************\n".format(datetime.datetime.now().strftime("%H:%M:%S")))
				log_counter+=2
			log.write("{}\n".format(text))
	put_on_queue(text)
	
def put_on_queue(text):
	##global gui_queue
	gui_queue.put(text)
#End of the Function write_me_log()
		
def save_cookies(session, filename): # to save session
    if not os.path.isdir(os.path.dirname(filename)):
        return False
    with open(filename, 'wb+') as f:
        f.truncate()
        pickle.dump(session.cookies._cookies, f,protocol=0) # pass protocol parameter and set it to 0. For Python 2 default value is 0 and for Python 3 value is 3 
#End of the Function save_cookies()	

def load_cookies(session, filename): # to load session 
    if not os.path.isfile(filename):
        return False
    with open(filename,'rb') as f:
        cookies = pickle.load(f)
        if cookies:
            jar = requests.cookies.RequestsCookieJar()
            jar._cookies = cookies
            session.cookies = jar
        else:
            return False
#End of the Function load_cookies()

def get_username_by_user_id_via_api(self,user_id,login=True): #  
	##global id_to_user
	user_id = str(user_id)
	user_name = "";ret = ()
	# API needs different Host value for its headers
	api_headers_1 = self.session_main.headers.copy()
	api_headers_1.update({"Host":"i.instagram.com"})
	if user_id in id_to_user and not login: # if user_name already fetched in previous session Or login=False 
		return (id_to_user[user_id],ret) #   if username already fetched in the current & previous sessions
	try:
		_url_info = "https://i.instagram.com/api/v1/users/%s/info/" % (user_id)
		if login:
			resp,excep = session_func(self.session_main,_url_info,headers=api_headers_1,redirects=False,wait=0) # <Doc> for API host must changed to 'i.instagram.com'
		else:
			resp,excep = session_func(session_temp,_url_info,redirects=False,wait=0) 
		if not excep:
			if resp and resp.status_code == 200:
				if "login" in resp.url: # if resp.url is 'https://www.instagram.com/accounts/login/' . Only could happen, if login=False
					write_me_log("{} ,redirecting to login page".format(len(resp.content)))
					return (user_name,ret)
				elif not resp.content or resp.text == '{}': # if resp is Blank/None 
					write_me_log("[Err] User details not Found!")
					return (user_name,ret)
				else:
					user = resp.json()["user"] # this may lead an exception 
					user_name = user["username"]
					if login:
						ret = (user["follower_count"],user["following_count"],user["is_private"],user["is_verified"],user["is_business"],user['full_name'],user["media_count"])
					id_to_user[user_id] = user_name #   stored in dictionary, in case it need to be fetched again
					shared_resource_lock.acquire()
					with open(os.path.join(path_app_directory,"userid to username.txt"),"a+") as f:
						f.write("{}:{}\n".format(user_id,user_name))
					shared_resource_lock.release()
			elif resp.status_code == 404:
				write_me_log("[Err] No User Found!")
			else:
				write_me_log("[Err] {} Page not responding properly! \r\nStatus Code: {}".format(resp.url,resp.status_code))
		else:
			write_me_log("[Exception(Exception)] ")
			app_exit()	
	except Exception as err:
		write_me_log("[Exception] exception error <during : get_username_by_user_id_via_api() >>> {}".format(err))
		app_exit()
	return (user_name,ret)
		
def get_username_by_user_id(self,user_id): # no login required  # better use get_username_by_user_id_via_api() 
	##global id_to_user
	user_id = str(user_id)
	user_name = ""
	if user_id in id_to_user:
		return id_to_user[user_id] #   if username already fetched in the current & previous sessions
	try:	
		params = {'query_hash':'7c16654f22c819fb63d1183034a5162f','variables':'{"include_highlight_reels":false,"include_reel":true,"user_id":'+user_id+',"include_chaining":false,"include_suggested_users":false,"include_logged_out_extras":false}'}		
		_url_info = "https://www.instagram.com/graphql/query"
		resp,excep = session_func(session_temp,_url_info,redirects=False,params=params)
		if not excep:
			if (not resp.content or resp.text == '{}') or "login" in resp.url: # if resp is Blank/None Or resp.url is 'https://www.instagram.com/accounts/login/'
				write_me_log("{} ,redirecting to login page".format(len(resp.content)))
				resp,excep = session_func(self.session_main,_url_info,redirects=False,params=params,proxies=proxies) # try to reopen the web with logged in session 
		else:
			write_me_log("[Exception(Exception-I)] ")
			app_exit()
		if not excep:
			if resp and resp.status_code == 200:
				if (not resp.content or resp.text == '{}'):
					write_me_log("[Err] User details not Found!")
					return False
				user_name = resp.json()["data"]["user"]["reel"]["owner"]["username"] # this may lead an exception 
				id_to_user[user_id] = user_name #   stored in dictionary, in case it need to be fetched again
				shared_resource_lock.acquire()
				with open(os.path.join(path_app_directory,"userid to username.txt"),"a+") as f:
					f.write("{}:{}\n".format(user_id,user_name))
				shared_resource_lock.release()
			elif resp.status_code == 404:
				write_me_log("[Err] No User Found!")
			else:
				write_me_log("[Err] {} Page not responding properly! \r\nStatus Code: {}".format(resp.url,resp.status_code))
		else:
			write_me_log("[Exception(Exception-II)] ")
			app_exit()
	except Exception as err:
		write_me_log("[Exception] exception error <during : get_username_by_user_id() >>> {}".format(err))
		app_exit()
	#write_me_log("Wait") #=> disabled, since get_username_by_user_id called session_func and session_func has its own wait
	#time.sleep(random.randrange(5,10)) # wait
	return user_name
	#except (requests.exceptions.ConnectionError,requests.exceptions.RequestException,requests.exceptions.Timeout,requests.exceptions.TooManyRedirects) as err:
	#write_me_log (err)
#End of the Function get_username_by_user_id()

def get_user_id_by_username(self,user_name):  # no login required
	##global user_to_id
	user_id = "";is_private = False
	url_info = url_user_detail % (user_name)
	_url_info = url_info+"?__a=1"
	if user_name in user_to_id:
		return user_to_id[user_name],is_private #   if user_id already fetched in the current session
	try:
		resp,excep = session_func(session_temp,_url_info)
		if not excep:
			if (not resp.content or resp.text == '{}') or resp.url != _url_info: # if resp is Blank/None Or resp.url is 'https://www.instagram.com/accounts/login/'
				write_me_log("{} ,redirecting to login page".format(len(resp.content)))
				resp,excep = session_func(self.session_main,_url_info,proxies=proxies) # try to reopen the web with logged in session 
		else:
			write_me_log("[Exception(Exception-I)] ")
			app_exit()
		if not excep:
			if resp and resp.status_code == 200:
				if (not resp.content or resp.text == '{}'):
					write_me_log("[Err] User details not Found!")
					return False
				user = resp.json()["graphql"]["user"] # this may lead an exception 
				user_id = user["id"] 
				is_private = user["is_private"]
				is_verified = user["is_verified"]
				is_business_account = user["is_business_account"]
				following_count = user["edge_follow"]["count"]
				followers_count = user["edge_followed_by"]["count"]
				post_count = user["edge_owner_to_timeline_media"]["count"]
				is_joined_recently = user["is_joined_recently"]
				user_to_id[user_name] = user_id #   stored in dictionary, in case it need to be fetched again
				id_to_user[user_id] = user_name #   stored in dictionary, in case it need to be fetched again
				shared_resource_lock.acquire()
				with open(os.path.join(path_app_directory,"userid to username.txt"),"a+") as f:
					f.write("{}:{}\n".format(user_id,user_name))
				shared_resource_lock.release()
			elif resp.status_code == 404:
				write_me_log("[Err] No User Found!")
			else:
				write_me_log("[Err] {} Page not responding properly! \r\nStatus Code: {}".format(resp.url,resp.status_code))
		else:
			write_me_log("[Exception(Exception-II)] ")
			app_exit()
	except Exception as err:
		write_me_log("[Exception] exception error <during : get_user_id_by_username() >>> {}".format(err))
		app_exit()
	return user_id,is_private
#End of the Function get_user_id_by_username()

def get_user_details(self,user_name,login=False): # no login required
	url_info = url_user_detail % (user_name)
	_url_info = url_info+"?__a=1"
	try:
		if login:
			resp,excep = session_func(self.session_main,_url_info,proxies=proxies)
		else:
			resp,excep = session_func(session_temp,_url_info)
			if not excep:
				if (not resp.content or resp.text == '{}') or resp.url != _url_info: # if resp is Blank/None Or resp.url is 'https://www.instagram.com/accounts/login/'
					write_me_log("{} ,redirecting to login page".format(len(resp.content)))
					resp,excep = session_func(self.session_main,_url_info,proxies=proxies) # try to reopen the web with logged in session 
			else:
				write_me_log("[Exception(Exception-I)] ")
				app_exit()
		if not excep:
			if resp and resp.status_code == 200:
				if (not resp.content or resp.text == '{}'):
					write_me_log("[Err] User details not Found!")
					return False
				data = resp.json() # resp.json() may return {} or something else # this may also lead an exception 
				user = data["graphql"]["user"]
				if login:
					return (user["followed_by_viewer"],user["follows_viewer"],user["requested_by_viewer"],user["id"])
				else:
					return (user["edge_followed_by"]["count"],user["edge_follow"]["count"],user["is_private"],user["is_verified"],user["is_business_account"],user['full_name'],user["edge_owner_to_timeline_media"]["count"])
			elif resp.status_code == 404:
				write_me_log("[Err] No User Found!!")
			else:
				write_me_log("[Err] {} Page not responding properly! \r\nStatus Code: {}".format(resp.url,resp.status_code))
		else:
			write_me_log("[Exception(Exception-II)] ")
			app_exit()
	except Exception as err:
		write_me_log("[Exception] exception error <during : get_user_details() >>> {}".format(err))
		app_exit()
	return False
#End of the Function get_user_details()

def session_func(s,url,headers={},redirects=True,params=None,data=None,proxies=None,method="get",wait=random.randrange(5,10)):
	'''try:
		headers = argv[0]
	except:
		headers = {}'''
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
			write_me_log ("[{}] Visiting {}".format(tried,url))
			if method == "get":
				if headers: # for API headers need to be different
					response = s.get(url,headers=headers,allow_redirects=redirects,params=params,verify=False, timeout=timeout,proxies=proxies)
				else:
					response = s.get(url,allow_redirects=redirects,params=params,verify=False, timeout=timeout,proxies=proxies)
			elif method == "post":
				response = s.post(url,verify=False, timeout=timeout,proxies=proxies)
			if response.status_code == 200:
				get = True
			else:
				time.sleep(5*tried) # or 30*tried
		except requests.ConnectionError as err:
			write_me_log("Your Internet Connection has some issue >>> {}".format(err))
			time.sleep(30*tried)
			exception = True
		except Exception as err:
			write_me_log("Exception occurred in session_func >>> {}".format(err))
			time.sleep(30*tried)
			exception = True
		tried+=1
	if not session_passed:
		s.close()
	#write_me_log("Wait in session_func")
	time.sleep(wait) #wait
	return response,exception
#End of the Function session_func()

def get_post_details(shortcode,about,type): # no login required
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
		write_me_log(">>> .scanning posts: {} to {}".format(((page_num-1)*first)+1,(page_num*first-1)+1))
		if not after:
			params = {'query_hash':hash,'variables':'{"first":'+str(first)+',"shortcode":"'+shortcode+'"}'}
		else:
			params = {'query_hash':hash,'variables':'{"first":'+str(first)+',"shortcode":"'+shortcode+'","after":"'+str(after)+'"}'}
		if about == "likes":
			params.update({'variables':params["variables"][:-1]+',"include_reel":true}'})
		try:
			resp,excep = session_func(session_temp,url_graphql,redirects=False,params=params)
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
					page_num+=1
				else:
					write_me_log("[Err] {} Page not responding properly! \r\nStatus Code: {}".format(resp.url,resp.status_code))
			else:
				write_me_log("[Exception] Exception! <during : get_post_details()>")
				app_exit()
			write_me_log("Wait")
			time.sleep(random.randrange(5,10)) # wait
		except Exception as err:
			write_me_log("[Exception] exception error <during : get_post_details() >>> {}".format(err))
			app_exit()
	return list(set(list_username)) # returning unique list
#End of the Function get_post_details()
def create_or_get_follow_text_file(directory_path,file_names,follow_lists):
	_my_follow = list()
	for idx,file_name in enumerate(file_names):
		if not os.path.exists(os.path.join(directory_path,file_name)) or (follow_lists and follow_lists[idx]) : # <Trick> After creating the text file on second run, (follow_lists and follow_lists[idx]) would return False if follow_list = [[]] passed as parameter in create_or_get_follow_text_file()
			shared_resource_lock.acquire()
			with open(os.path.join(directory_path,file_name),"w+") as f:
				if not follow_lists[idx]:
					write_me_log("blank create") # for DEBUG purpose only
					f.write("")
					_my_follow.append([])
				else:
					write_me_log("create")  # for DEBUG purpose only
					f.write(',\n'.join(str(each) for each in follow_lists[idx])+',\n')
					_my_follow.append(follow_lists[idx])
			shared_resource_lock.release()
		else:
			write_me_log("read")  # for DEBUG purpose only
			shared_resource_lock.acquire()
			if open(os.path.join(directory_path,file_name),"r").read().strip():
				_my_follow.append([each for each in open(os.path.join(directory_path,file_name),"r").read().strip(" ").split(",\n") if each]) # <trick> should't use strip(), cause it will remove \n from the end
			else:
				_my_follow.append([])
			shared_resource_lock.release()
	return _my_follow
#End of the Function create_or_get_follow_text_file()

def update_follow_text_file(directory_path,file_names,my_follow,username_to_follow_or_unfollow,append=True):
	write_me_log("Accessing update_follow_text_file()") # For DEBUG
	# if append is True, append user to the list & add user to the file. If append is False, remove user from the list & remove it from the file 
	for idx,file_name in enumerate(file_names):
		shared_resource_lock.acquire()
		if isinstance(my_follow[idx],list): # if sublist is a instance of a list
			if append:
				my_follow[idx].append(username_to_follow_or_unfollow)
			else:
				if username_to_follow_or_unfollow in my_follow[idx]:
					my_follow[idx].remove(username_to_follow_or_unfollow)
		if append:
			with open(os.path.join(directory_path,file_name),"a+") as f:
				f.write(username_to_follow_or_unfollow+",\n")
		else:
			file_content = open(os.path.join(directory_path,file_name)).read()
			file_content = file_content.replace(username_to_follow_or_unfollow+",\n","")
			with open(os.path.join(directory_path,file_name),"w+") as f:
				f.write(file_content)
		shared_resource_lock.release()
#End of the Function update_follow_text_file()		

def id_generator_alnum(size, chars=string.digits+string.ascii_lowercase+string.ascii_uppercase):
	return ''.join(random.choice(chars) for _ in range(size))
#End of id_generator_alnum()

def user_does_not_exist(user_name):
	bad_usernames.append(user_name)
	with open(os.path.join(path_app_directory,"user does not exist.txt"),"a+") as f:
		f.write("{}\n".format(user_name))
# End of user_does_not_exist()
# End of Functions		

####### CLASSES #######

class InstagramBot(QMainWindow,InstagramBot_ui.Ui_InstagramBot):
	# accessing global variables
	global url_follow,url_unfollow,url_home,url_login,url_user_detail,url_graphql,list_of_ua,accept_language,queue,path_app_directory,id_to_user,user_to_id,proxies,timeout\
	,shared_resource_lock,my_followers,my_following,my_following_app,bad_usernames,exclude_usernames,app_version
	
	def __init__(self):
		QMainWindow.__init__(self)
		self.setFixedSize(QSize(840, 583))
		self.resize(840, 583)
		self.setMinimumSize(QSize(840, 583))
		self.setMaximumSize(QSize(840, 583))
		self.setCursor(Qt.PointingHandCursor)
		self.setupUi(self)
		
		# Setup System tray 
		systray_icon = QIcon()
		systray_icon.addPixmap(QPixmap(":/Main Icon/InstagramBot_systray.png"), QIcon.Normal, QIcon.Off)
		systray = QSystemTrayIcon(systray_icon,self)

		self.menu = QMenu()
		self.hideit = QAction("hide",self)
		self.showit = QAction("show",self)
		self.closeit = QAction("close",self)
		self.menu.addActions([self.hideit,self.closeit])

		systray.setContextMenu(self.menu)
		systray.show()

		self.closeit.triggered.connect(self.close)
		self.hideit.triggered.connect(self.hide)
		self.showit.triggered.connect(self.show)

		systray.showMessage("InstagramBOT","App is Running successfully!",QSystemTrayIcon.Information,2000)  # Information could be replaced by Warning, Critical, NoIcon
		
		# Status bar
		self.statusBar().showMessage("[ Powered by MediaBOTS ]")
		
		# For Thread Only
		##self.thread = ThreadClass()
		##self.thread.start()
		##self.thread.checkSignal.connect(self.update_label)
		##self.progress_bar.hide() # -> progress_bar need to be added by designer.exe before availabling this command 
		
		self.thread_check_update = ThreadCheckUpdate()
		self.thread_check_update.start()
		self.thread_check_update.signalCheckUpdate.connect(self.check_app_update)
		
		self.thread_check_status = ThreadCheckStatus()
		self.thread_check_status.start()
		self.thread_check_status.signalCheckStatus.connect(self.check_app_status)
		
		# Gui Thread
		self.gui_thread_2 = MyGuiThreadTwo('gui branch-thread 2') 
		self.gui_thread_2.start()
		
		#initialize class variables
		self.userid = ""
		self.username = ""
		self.password = ""
		self.proxy = ""
		#
		self.successful_login = False
		self.after_challenge = False
		#
		self.user_agent = random.sample(list_of_ua, 1)[0]
		# creating session variables from requests module 
		self.session_main = requests.Session()
		self.session_main.headers.update(
		{
		"Accept": "*/*",
		"Accept-Language": accept_language,
		"Accept-Encoding": "gzip, deflate, br",
		"Connection": "keep-alive",
		"Host": "www.instagram.com",
		"Origin": "https://www.instagram.com",
		"Referer": "https://www.instagram.com/",
		"User-Agent": self.user_agent,
		"X-Instagram-AJAX": "1",
		"Content-Type": "application/x-www-form-urlencoded",
		"X-Requested-With": "XMLHttpRequest",
		}
		)
		#
		self.counter_path = ""
		self.count_dict = {}
		self.tracker_path = ""
		self.track_dict = {}
		#
		self.path_users_directory = os.path.join(os_user_directory,documents,"MediaBOTS","InstagramBOT","users") # get path of the users directory 
		if os.listdir(self.path_users_directory):
			user_folders = [file_ for file_ in os.listdir(self.path_users_directory) if os.path.isdir(os.path.join(self.path_users_directory,file_))]
			##user_files = [file_ for file_ in os.listdir(self.path_users_directory) if os.path.isfile(os.path.join(self.path_users_directory,file_)) and file_.endswith(".txt")]
			if user_folders : 
				user_folder = user_folders[0]
				if os.path.exists(os.path.join(self.path_users_directory,user_folder,user_folder+".txt")):
					user_file_content = open(os.path.join(self.path_users_directory,user_folder,user_folder+".txt"),"r").read().strip().split("\n")[0]
					if user_file_content and len(user_file_content.split(","))==3:
						self.username,self.password,self.proxy=user_file_content.split(",")
						#write_me_log(self.proxy) # for DEBUG
						
		
		# set tab to index 0 & select 1st item of the list
		self.listwidget.item(0).setSelected(True)
		self.tabWidget.setCurrentIndex(0)
		
		self.listwidget.itemClicked.connect(self.Clicked)
		self.tabWidget.currentChanged.connect(self.Changed)
		##self.actionQueue.triggered.connect(self.newwindow) !disabled temporarily
		
		if self.username:
			self.line_find_users.setText(self.username)
			self.line_download_type.setText(self.username)
		else:
			self.line_find_users.setText("[At first, add an Instagram account]")
			self.line_download_type.setText("[At first, add an Instagram account]")
		self.line_find_users.setReadOnly(True)
		self.line_download_type.setReadOnly(True)
		
		# Account Settings
		self.logintable.setColumnCount(0)
		self.logintable.setRowCount(0)
		##self.logintable.insertRow(0)
		self.logintable.insertColumn(0)
		self.logintable.insertColumn(1)
		self.logintable.insertColumn(2)
		self.logintable.setHorizontalHeaderLabels(["Username","Password","Proxy Address"])
		self.logintable.setColumnWidth(0,121)
		self.logintable.setColumnWidth(1,121)
		self.logintable.setColumnWidth(2,121)
		#
		self.add.clicked.connect(self.addAccount)
		self.remove.clicked.connect(self.removeAccount)
		#
		# setting data to tableWidget
		if self.username:
			username  = QTableWidgetItem(self.username)
			username.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled) # set flags so item is uneditable
			##password  = QTableWidgetItem(self.password))
			password  = QTableWidgetItem(len(self.password)*'*') # set flags so item is uneditable
			password.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
			# preparing tableWidget for next row insert
			self.logintable.insertRow(self.logintable.rowCount())
			self.logintable.setItem(self.logintable.rowCount()-1, 0, username)
			self.logintable.setItem(self.logintable.rowCount()-1, 1, password) 
			self.logintable.setItem(self.logintable.rowCount()-1, 2, QTableWidgetItem(self.proxy))
		# 
		self.logintable.itemChanged.connect(self.login_data_changed)
		#
		#Multi Account
		self.button_enable_multi_account.clicked.connect(self.enable_multi_account)
		self.label_enable_multi_users_2.hide()
		if directory_chnaged:
			self.label_enable_multi_users_1.hide()
			self.label_enable_multi_users_2.show()
			self.button_enable_multi_account.setEnabled(False)
			self.button_enable_multi_account.setText("Multiple Account Support Enabled")
		
		# Find Following & Followers
		self.browse_find_following_followers.clicked.connect(self.browse_following_followers)
		self.button_find_following_followers_task.clicked.connect(self.add_find_following_followers_task)
		
		
		# Follow/Unfollow
		self.combo_follow_users.currentIndexChanged.connect(self.select_follow_users)
		#
		self.combo_unfollow_users.currentIndexChanged.connect(self.select_unfollow_users)
		#
		self.check_unfollow_users.hide()
		self.followback_day_limit.hide()
		#
		self.check_unfollow_users.setChecked(False)
		#
		##self.check_unfollow_users.setEnabled(False)
		#
		self.check_is_private_2.hide()
		self.check_is_verified_2.hide()
		self.check_is_celebrity_2.hide()
		#
		self.label_exclude.hide()
		#
		self.check_is_private_2.setChecked(False)
		self.check_is_verified_2.setChecked(False)
		self.check_is_celebrity_2.setChecked(False)
		#
		self.button_follow_task.clicked.connect(self.add_follow_task)
		#
		self.button_unfollow_task.clicked.connect(self.add_unfollow_task)
		#
		#Download Posts
		self.button_download_post_task.clicked.connect(self.add_download_post_task)
		##self.button_follow_users.clicked.connect(self.browse_follow_users) #disabled
		##self.button_unfollow_users.clicked.connect(self.browse_unfollow_users) #disabled
		#
		if self.username:
			self.path_follow_users.setText(QDir.toNativeSeparators(os.path.join(self.path_users_directory,self.username,"myList","follow.txt")))
			self.path_unfollow_users.setText(QDir.toNativeSeparators(os.path.join(self.path_users_directory,self.username,"myList","unfollow.txt")))
			self.button_follow_users.setEnabled(False) #
			self.button_unfollow_users.setEnabled(False) #
		else:
			self.path_follow_users.setReadOnly(True)
			self.path_unfollow_users.setReadOnly(True)
			self.button_follow_users.setEnabled(False)
			self.button_unfollow_users.setEnabled(False)
		
		# Like/Unlike
		self.combo_like_posts.currentIndexChanged.connect(self.browse_like_posts)
		self.check_like_posts.hide()
		self.radio_like_posts1.setChecked(True)
		self.radio_like_posts1.setEnabled(False)
		self.radio_like_posts2.setEnabled(False)
		
		# Find suitable users
		self.combo_find_users.currentIndexChanged.connect(self.select_find_users)
		#
		self.button_find_users_task.clicked.connect(self.add_find_users_task)
		
		# Download Posts
		self.combo_download_type.currentIndexChanged.connect(self.select_download_type)
		#
		self.radio_download_type_all.setChecked(True)
		self.radio_download_post_age_today.setChecked(True)
		#
		self.line_download_post_excel_location.setEnabled(False)
		
		#QActions
		self.actionEmail_Us.triggered.connect(self.open_email)
		self.actionOpen_User_Folder.triggered.connect(self.open_users_folder)
		self.actionGithub_Project_URL.triggered.connect(self.open_github_project)
		self.actionMediaBOTS.triggered.connect(self.open_home_page)
		self.actionOpen_an_Issue.triggered.connect(self.open_github_issue_page)
		self.actionBTC_Donation.triggered.connect(self.open_btc_donation_page)
		self.actionLogs.triggered.connect(self.open_logs)
		self.actionExit.triggered.connect(self.close) # self.close is a default function 
	# Thread's
	'''def update_label(self,value1 ,value2):
		self.label.setText(value1)
		##self.progress_bar.setValue(value2) # -> progress_bar need to be added by designer.exe before availabling this command '''
	def check_app_update(self): 
		write_me_log("App Update choice")
		should_download = QMessageBox.question(self,"Application Update","A newer version of the InstagramBOT is available, would you like to Download the latest version?",
											QMessageBox.Yes, QMessageBox.No)
		if should_download == QMessageBox.Yes:
			write_me_log("Downloading...")  # For DEBUG only
			url = QUrl('https://github.com/mediabots/InstagramBot-GUI-Python')
			if not QDesktopServices.openUrl(url):
				QMessageBox.warning(self, 'Application Update', 'Could not open url : https://github.com/mediabots/InstagramBot-GUI-Python')
		else:
			write_me_log("Continuing with the old version of InstagramBOT")  # For DEBUG only
			pass
	def check_app_status(self,message): 
		self.statusBar().showMessage(message)
		##self.statusBar().setStyleSheet("color: brown");
	# ------------ TOOLBAR ------------
	def open_email(self):
		url = QUrl('mailto:mediabots@mail.ru')
		if not QDesktopServices.openUrl(url):
			QMessageBox.warning(self, 'Email', 'Could not open your Defualt mail client to contact: mediabots@mail.ru')
	def open_users_folder(self):
		url = QUrl(path_app_directory)
		if not QDesktopServices.openUrl(url):
			QMessageBox.warning(self, 'Folder', 'Could not open Folder : {}'.format(path_app_directory))
	def open_github_project(self):
		#import webbrowser
		#webbrowser.open("http://www.google.com")
		url = QUrl('https://github.com/mediabots/InstagramBot-GUI-Python')   
		if not QDesktopServices.openUrl(url):
			QMessageBox.warning(self, 'Github Page', 'Could not open url: https://github.com/mediabots/InstagramBot-GUI-Python')
	def open_home_page(self):
		url = QUrl('https://github.com/mediaBOTS')
		if not QDesktopServices.openUrl(url):
			QMessageBox.warning(self, 'Home Page', 'Could not open url: https://github.com/mediaBOTS')
	def open_github_issue_page(self):
		url = QUrl('https://github.com/mediabots/InstagramBot-GUI-Python/issues/new')
		if not QDesktopServices.openUrl(url):
			QMessageBox.warning(self, 'Home Page', 'Could not open url: https://github.com/mediabots/InstagramBot-GUI-Python/issues/new')
	def open_btc_donation_page(self):
		url = QUrl('https://www.blockchain.com/btc/address/3Qdt3Cm19TUgFsqpfKnnms9ALxmgqLabou')
		if not QDesktopServices.openUrl(url):
			QMessageBox.warning(self, 'BTC Donation', 'Could not open url: https://www.blockchain.com/btc/address/3Qdt3Cm19TUgFsqpfKnnms9ALxmgqLabou')
	def open_logs(self):
		url = QUrl(log_path)  
		if not QDesktopServices.openUrl(url):
			QMessageBox.warning(self, 'Logs', 'Could not open file/folder : ')
	# ----------------------------------
	# Default Event Handler
	def hideEvent(self, event): 
		self.hide() 
		self.menu.removeAction(self.hideit)
		self.menu.removeAction(self.closeit)
		self.menu.addActions([self.showit,self.closeit])
		#if event.type() == QEvent.Type.Hide:
			#write_me_log (1)
		#if event.type() == QEvent.Type.Show:
			#write_me_log (2)

	def showEvent(self, event):  
		self.show() 		
		self.menu.removeAction(self.showit)
		self.menu.removeAction(self.closeit)
		self.menu.addActions([self.hideit,self.closeit])
		#if event.type() == QEvent.Type.Hide:
			#write_me_log (1)
		#if event.type() == QEvent.Type.Show:
			#write_me_log (2)
	
	def closeEvent(self, event): 
		write_me_log("Closing window") # for Debug
		should_close = QMessageBox.question(
		self,"Quit","Do you want to close the Application?",
		QMessageBox.Yes, QMessageBox.No
		)
		if should_close == QMessageBox.Yes:
			event.accept()
			os._exit(1)
			##sys.exit()
			##exit()
		else:
			event.ignore()
	# ----------------------------------
	# Login
	def login(self):
		# set default path for login user
		self.counter_path = os.path.join(self.path_users_directory,self.username,"etc","counter",datetime.datetime.utcnow().strftime("%d-%m-%Y")+".txt") #or use today() instead of utcnow()
		self.tracker_path = os.path.join(self.path_users_directory,self.username,"etc","tracker",datetime.datetime.utcnow().strftime("%d-%m-%Y")+".txt") #or use today() instead of utcnow()
		# setting proxies
		if self.proxy:
			proxies = {'http': 'http://'+self.proxy,'https': 'https://'+self.proxy}
		login_post = {"username": self.username,"password": self.password}
		#loading saved user agent
		if not os.path.exists(os.path.join(self.path_users_directory,self.username,"browser_agent.txt")):
			with open(os.path.join(self.path_users_directory,self.username,"browser_agent.txt"),"w+") as f:
				f.write(self.user_agent)
		else:
			self.session_main.headers["User-Agent"] = open(os.path.join(self.path_users_directory,self.username,"browser_agent.txt"),"r").read().strip()
		# loading cookies/session
		if os.path.exists(os.path.join(self.path_users_directory,self.username,"cookie.txt")):
			write_me_log ("Login via Cookies")
			load_cookies(self.session_main,os.path.join(self.path_users_directory,self.username,"cookie.txt"))
			r = self.session_main.get(url_home,verify=False,timeout=timeout)
			if self.username in r.text:
				self.successful_login = True
				#update cookies
				csrf_token = r.cookies['csrftoken'] #OR >>> csrf_token = re.search('(?<="csrf_token":")\w+', r.text).group(0)
				self.session_main.headers.update({"X-CSRFToken": csrf_token})
				rollout_hash = re.search('(?<="rollout_hash":")\w+', r.text).group(0)
				self.session_main.headers.update({"X-Instagram-AJAX": rollout_hash})
				write_me_log ("Logged in via Cookies successfully!")
				self.userid = re.search('(?<="user":{"id":")\w+', r.text).group(0)
				return
		else:
			write_me_log ("Logging in")
		try:
			time.sleep(5 * random.random())
			r = self.session_main.get(url_home,verify=False,timeout=timeout)
			if r.status_code == 200:
				csrf_token = r.cookies['csrftoken'] if r.cookies else id_generator_alnum(32) #OR >>> csrf_token = re.search('(?<="csrf_token":")\w+', r.text).group(0)
				self.session_main.headers.update({"X-CSRFToken": csrf_token})
				try:
					login = self.session_main.post(url_login, data=login_post, allow_redirects=True,verify=False)
					if login.status_code == 200:
						loginResponse = login.json()
						write_me_log (loginResponse)
						if loginResponse.get("authenticated") is True:
							self.userid = loginResponse.get('userId')
							if not self.userid:
								self.userid = re.search('(?<="user":{"id":")\w+', r.text).group(0)
							self.session_main.headers.update({"X-CSRFToken": login.cookies["csrftoken"]})
							rollout_hash = re.search('(?<="rollout_hash":")\w+', r.text).group(0)
							self.session_main.headers.update({"X-Instagram-AJAX": rollout_hash})
							self.session_main.cookies["ig_vw"] = "1536"
							self.session_main.cookies["ig_pr"] = "1.25"
							self.session_main.cookies["ig_vh"] = "772"
							self.session_main.cookies["ig_or"] = "landscape-primary"
							try:
								time.sleep(5 * random.random())
								r2 = self.session_main.get(url_home,verify=False,timeout=timeout)
								if self.username in r2.text:
									self.successful_login = True
									write_me_log ("Logged in successfully!")
									# saving cookies/session
									save_cookies(self.session_main,os.path.join(self.path_users_directory,self.username,"cookie.txt"))
								else:
									write_me_log ("[Error] Login Failed!")
									app_exit()
							except Exception as err:
								write_me_log ("[Error] Instagram login() EXCEPTION (level-3) >>> {}".format(err))
								app_exit()
						else:
							write_me_log ("[Error] Account login failed! \r\n(json : {})".format(loginResponse))
							app_exit()
					elif login.status_code == 400 and login.json()['message'] == 'checkpoint_required':
						if not self.after_challenge:
							self.after_challenge = True
							write_me_log("[Interrupted] To login, you required to verify your IG account at first")
							#write_me_log("would you like to Verify your account through which of the following Options:-\n1)Email Code\n2)SMS Code")
							#verify_choice = input("Enter 1 or 2 : ")
							verify_options = {"1":"Email","2":"Mobile"}
							#if verify_choice not in ["1","2"]: 
							#	verify_choice = "1"
							verify_choice = "1"
							try:
								time.sleep(5 * random.random())
								login2 = self.session_main.post(url_home[:-1]+login.json()["checkpoint_url"], data={'choice':verify_choice}, allow_redirects=True,verify=False)
								if login2.status_code == 200 and ("Enter Security Code" in login2.text or login2.json()['status'] == "ok"):
									##security_code =  input("Check your {} and enter the CODE : ".format(verify_options[verify_choice]))
									security_code, ok = QInputDialog.getText(self, 'Enter Email Code', 'The Code(received via Email) :') # security_code will receive a string object
									if ok:
										write_me_log(security_code)
									else:
										app_exit()
									try:
										time.sleep(5 * random.random())
										login3 = self.session_main.post(login2.url, data={'security_code':security_code}, allow_redirects=True,verify=False)
										if login3.status_code == 200 and (self.username in login3.text or login3.json()['status'] == "ok"):
											write_me_log("Processing IG Login Challenge.....")
											# checking whether response content is in json or not
											try:
												login3.json()
												self.login()  # <Trick> if json, need to call login() again to set all session parameters
											except:
												if self.username in login3.text:
													self.successful_login = True
													#update cookies
													rollout_hash = re.search('(?<="rollout_hash":")\w+', login3.text).group(0)
													self.session_main.headers.update({"X-Instagram-AJAX": rollout_hash})
													write_me_log ("[.] Logged in successfully!")
													# saving cookies/session
													save_cookies(self.session_main,os.path.join(self.path_users_directory,self.username,"cookie.txt"))
										else:
											write_me_log("[Error] IG Login Challenge Not working at (stage-2)")
											app_exit()
									except Exception as err:
										write_me_log ("[Error] Instagram login() EXCEPTION (level-4) >>> {}".format(err))
										app_exit()
								else:
									write_me_log("[Error] IG Login Challenge Not working at (stage-1)")
									app_exit()
							except Exception as err:
								write_me_log ("[Error] Instagram login() EXCEPTION (level-3) >>> {}".format(err))
								app_exit()
						else:
							write_me_log("[Error] IG Login Challenge Failed!!")
							app_exit()
					else:
						write_me_log ("[Error] Instagram POST request not made! \r\n(status_code : {})".format(login.status_code))
						app_exit()
				except Exception as err:
					write_me_log ("[Error] Instagram login() EXCEPTION (level-2) >>> {}".format(err))
					app_exit()
			else:
				write_me_log ("[Error] Instagram page not connecting! \r\n(status_code : {})".format(r.status_code))
				app_exit()
		except Exception as err:
			write_me_log ("[Error] Instagram login() EXCEPTION (level-1) >>> {}".format(err))
			app_exit()	
	# Follow a user by its username
	def follow_user(self): 
		if self.combo_follow_users.currentText() == "Follow users from my List":
			self.follow_unfollow_list()
		elif self.combo_follow_users.currentText() == "Auto Followback my followers":
			self.followback()
	def followback(self):
		self.combo_find_following_followers.setCurrentIndex(0) # <Trick> set to followers
		##my_following = create_or_get_follow_text_file(os.path.join(self.path_users_directory,self.username,"myStatus"),["following.txt"],[[]])[0] # <Doc> get my_following list , which would be required on next step; ie, find_following_followers() 
		self.find_following_followers(own_account=True,account_file="follow.txt") # <Doc> to get updated my_followers + to get updated follow.txt file
		self.follow_unfollow_list(followback=True)
		# Unfollow a user by its username
	def unfollow_user(self): 
		if self.combo_unfollow_users.currentText() == "Unfollow users form my List":
			self.follow_unfollow_list(follow=False)
		elif self.combo_unfollow_users.currentText() == "Auto Unfollow users those did not followback":
			self.unfollow_if()
		elif self.combo_unfollow_users.currentText() == "Unfollow all":
			self.unfollow_all()
	def unfollow_if(self):
		self.combo_find_following_followers.setCurrentIndex(0) # <Trick> set to followers
		# pass account_file="", because account_file modification not required in ths case
		self.find_following_followers(own_account=True) # <Doc> to get updated my_followers. REMEMBER - on next step, follow_unfollow_list() would not read from follow.txt or unfollow.txt file ,so no modification required for any of them
		self.follow_unfollow_list(follow=False)
	def unfollow_all(self):
		#print(self.check_unfollow_users.isHidden(),self.check_unfollow_users.isChecked())
		#write_me_log(self.check_unfollow_users.isHidden(),self.check_unfollow_users.isChecked())
		self.combo_find_following_followers.setCurrentIndex(1) # <Trick> set to following
		# <Doc>  For unfollow, my_following list required to be empty to update "unfollow.txt" file in find_following_followers()
		self.find_following_followers(own_account=True,account_file="unfollow.txt",_my_following=[]) # <Doc> to get updated my_following + to get updated unfollow.txt file
		self.follow_unfollow_list(follow=False)
	def follow_unfollow_list(self,follow=True,followback=False):	 # login required
		global my_following_app,my_followers
		#login if user not already logged in 
		if not self.successful_login: 
			self.login()
		# loading counter data on a dict
		if not os.path.exists(self.counter_path):
			self.initialize_counter()
		else:
			if not self.count_dict:
				self.read_counter()
		# determining follow or unfollow
		if follow:
			text_file_path = self.path_follow_users.text()
			counter_type = "following"
			daily_follow_or_unfollow_limit = int(self.daily_follow_limit.text())
			url_follow_unfollow = url_follow 
		else:
			text_file_path = self.path_unfollow_users.text()
			counter_type = "unfollowing"
			daily_follow_or_unfollow_limit = int(self.daily_unfollow_limit.text())
			url_follow_unfollow = url_unfollow
		while True:
			# reading unfollow.txt file content
			if os.path.exists(os.path.join(self.path_users_directory,self.username,"myList","unfollow.txt")):
				shared_resource_lock.acquire()
				unfollow_file_content = open(os.path.join(self.path_users_directory,self.username,"myList","unfollow.txt")).read() # or read from self.path_unfollow_users.text()
				shared_resource_lock.release()
			else:
				write_me_log("[Error] unfollow.txt file does't exist!")
				app_exit()
			# loading follow.txt or unfollow.txt from myList
			if os.path.exists(text_file_path):
				shared_resource_lock.acquire()
				usernames_to_follow_or_unfollow = open(text_file_path,"r").read().strip(" ").split(",\n")
				usernames_to_follow_or_unfollow = [each for each in usernames_to_follow_or_unfollow if each] # removing '' from list, if it is exist
				shared_resource_lock.release()
			else:
				QMessageBox.warning(self,"Warning!","{} file does not exist!".format(text_file_path))
				app_exit()
			# only for the condition :- "unfollow iff the user did not followback within x days"
			if not follow and self.check_unfollow_users.isChecked():
				# get updated my_followers list
				my_followers = create_or_get_follow_text_file(os.path.join(self.path_users_directory,self.username,"myStatus"),["followers.txt"],[[]])[0] # <Doc> pass [[]] to read(iff exists) or create a blank
				# get updated my_following_app list
				my_following_app = create_or_get_follow_text_file(os.path.join(self.path_users_directory,self.username,"myStatus"),["following_via_app.txt"],[[]])[0] # <Doc> pass [[]] to read(iff exists) or create a blank
				usernames = []
				followback_day_limit = int(self.followback_day_limit.text())
				# loading todays paths & dicts for temporary
				'''today_counter_path = self.counter_path
				today_tracker_path = self.tracker_path
				today_count_dict = self.count_dict
				today_track_dict = self.track_dict'''
				dates = [(datetime.datetime.utcnow() - datetime.timedelta(days=day)).strftime("%d-%m-%Y") for day in range(followback_day_limit)]
				write_me_log(dates) # For Debug
				for idx,each_date in enumerate(dates):
					if os.path.exists(os.path.join(self.path_users_directory,self.username,"etc","tracker",each_date+".txt")):
						#self.counter_path = os.path.join(self.path_users_directory,self.username,"etc","counter",each_date+".txt")
						tracker_path = os.path.join(self.path_users_directory,self.username,"etc","tracker",each_date+".txt")
						##self.read_tracker() # avoid read_tracker tracker, since its not calling  read_counter() on its function body
						track_dict = self.read_tracker(tracker_path) 
						##shared_resource_lock.acquire()
						usernames += track_dict["following"] # this would return "following" usernames of each_date from read_tracker
						##shared_resource_lock.release()
				# restoring paths & dicts to todays
				'''self.counter_path = today_counter_path
				self.tracker_path = today_tracker_path
				self.count_dict = today_count_dict
				self.track_dict = today_track_dict'''
				# overwrite usernames_to_follow_or_unfollow list values
				usernames_to_follow_or_unfollow = list(set(my_following_app) - set(my_followers) - set(usernames))
				#write_me_log(usernames_to_follow_or_unfollow) # for Debug
			# get updated my_following list
			##shared_resource_lock.acquire() # <DOC> Lock should not be implemented here, otherwise, it will wait for Infinite time 
			my_following = create_or_get_follow_text_file(os.path.join(self.path_users_directory,self.username,"myStatus"),["following.txt"],[[]])[0] # <Doc> pass [[]] to read(iff exists) or create a blank
			##shared_resource_lock.release()
			#write_me_log("to follow/unfollow : {}".format(usernames_to_follow_or_unfollow)) # for Debug only
			#write_me_log("already following : {}".format(my_following)) # for Debug only
			if followback:
				# overwrite usernames_to_follow_or_unfollow
				usernames_to_follow_or_unfollow = my_followers
			#write_me_log(usernames_to_follow_or_unfollow) # for Debug purpose
			for username_to_follow_or_unfollow in usernames_to_follow_or_unfollow:
				if (follow and username_to_follow_or_unfollow not in my_following and username_to_follow_or_unfollow not in bad_usernames and \
				username_to_follow_or_unfollow+",\n" not in unfollow_file_content) or (not follow and username_to_follow_or_unfollow in my_following and \
				username_to_follow_or_unfollow not in bad_usernames and username_to_follow_or_unfollow not in exclude_usernames): # <Trick>
					# specially for unfollow
					if not follow:
						# IG user type Conditions
						ret = get_user_details(self,username_to_follow_or_unfollow)
						write_me_log("wait")
						time.sleep(random.randrange(5,10)) #wait # though default sleep/wait is present, but it might be continued,so sleep externally requires
						#write_me_log(ret) # for DEBUG only
						if ret:
							if self.check_is_private_2.isChecked() and ret[2]:
								write_me_log("is_private")  # For DEBUG
								exclude_usernames.append(username_to_follow_or_unfollow)
								continue
							if self.check_is_verified_2.isChecked() and ret[3]:
								write_me_log("is_verified")  # For DEBUG
								exclude_usernames.append(username_to_follow_or_unfollow)
								continue
							if self.check_is_celebrity_2.isChecked() and ret[4]:
								write_me_log("is_celebrity")  # For DEBUG
								exclude_usernames.append(username_to_follow_or_unfollow)
								continue
					# get latest following info of a particular user from IG itself
					_following = get_user_details(self,username_to_follow_or_unfollow,login=True)
					if _following:
						_following,target_user_id = (_following[0] or _following[2],_following[3]) # either followed or requested(for private account) 
						# if has to unfollow a user and that user already unfollowed OR if has to follow a user and user already followed  
						if (not follow and not _following) or (follow and _following):
							write_me_log("{} already {}".format(username_to_follow_or_unfollow,counter_type))
							# update following.txt file as well as update my_following variable
							update_follow_text_file(os.path.join(self.path_users_directory,self.username,"myStatus"),["following.txt","followers+following.txt"],[my_following,0],username_to_follow_or_unfollow,append=follow) # <Doc> 3rd parameter is list ,and its sublist is also a list unless its correspondence .txt file has variable
							# should not update counter, because that user was not followed/unfollowed on that day.
							##self.update_counter(counter_type,username_to_follow_or_unfollow) # <- BUG Spotted
							write_me_log("wait")
							time.sleep(random.randrange(5,10)) #wait # though default sleep/wait is present, but it might be continued,so sleep externally requires
							write_me_log("continued") # for DEBUG
							continue 
					else:
						user_does_not_exist(username_to_follow_or_unfollow)
						write_me_log("User does not exist")
						write_me_log("continued")
						continue 
					#write_me_log("00000000000000000000000000") # for DEBUG
					##target_user_id = get_user_id_by_username(self,username_to_follow_or_unfollow)[0] # target_user_id could be achieved at earlier get_user_details()
					# no sleep requires, since default sleep/wait is present 
					if target_user_id:
						_url_follow_or_unfollow = url_follow_unfollow % (target_user_id)
						#wait until next day, if daily follow limit exceeded
						if self.count_dict[counter_type] >= daily_follow_or_unfollow_limit:
							write_me_log("Daily {} limit({}) reached".format(counter_type,daily_follow_or_unfollow_limit))
							today = int(datetime.datetime.utcnow().strftime("%d"))
							tomorrow = today + 1
							while today != tomorrow:
								write_me_log("Sleeping on {} for {}".format(self.follow_unfollow_list.__name__,counter_type))  # for DEBUG purpose
								time.sleep(5*60) # recheck in every 5 mins
								today = int(datetime.datetime.utcnow().strftime("%d"))
								#in case, at later, user updated daily_follow_or_unfollow_limit variable
								daily_follow_or_unfollow_limit = int(self.daily_follow_limit.text()) if (follow and self.daily_follow_limit.text()) else int(self.daily_unfollow_limit.text())
								if self.count_dict[counter_type] < daily_follow_or_unfollow_limit:
									write_me_log("break")
									break # exit from while loop & start following
						try:
							resp,excep = session_func(self.session_main,_url_follow_or_unfollow,method="post",proxies=proxies)
							if not excep:
								if resp and resp.status_code == 200: # resp.json() -> {'status': 'ok', 'result': 'following'}
									write_me_log ("{} {}".format(resp.json().get('result'),username_to_follow_or_unfollow))
									if (follow and (resp.json().get('result') == counter_type) or resp.json().get('result') == "requested") or (not follow and resp.json().get('result') == None):
										# update following.txt file as well as update my_following variable
										update_follow_text_file(os.path.join(self.path_users_directory,self.username,"myStatus"),["following.txt","following_via_app.txt","followers+following.txt"],[my_following,my_following_app,0],username_to_follow_or_unfollow,append=follow) # <Doc> 3rd parameter is list ,and its sublist is also a list unless its correspondence .txt file has variable
										# <Note> "followers+following.txt" may contain duplicates
										self.update_counter(counter_type,username_to_follow_or_unfollow)
										min_time_interval,max_time_interval = (int(self.min_follow_interval.text()),int(self.max_follow_interval.text())) if follow \
										else (int(self.min_unfollow_interval.text()),int(self.max_unfollow_interval.text())) 
										# checking if max value is less than min value 
										if  max_time_interval > min_time_interval:
											sleep = random.randint(min_time_interval,max_time_interval)
										else:
											sleep = random.randint(max_time_interval,max_time_interval)
										write_me_log("Sleeping for {} mins".format(sleep))# for DEBUG
										time.sleep(sleep*60)
								else:
									write_me_log("[Err] {} Page not responding properly! \r\nStatus Code: {}".format(resp.url,resp.status_code))
							else:
								write_me_log("[Exception] Exception! <during : follow_unfollow_list()>")
								app_exit()
						except Exception as err:
							write_me_log("[Exception] exception error <during : follow_unfollow_list()>>> {}".format(err))
							app_exit()
					else:
						user_does_not_exist(username_to_follow_or_unfollow)
			time.sleep(60)				
			if followback or self.check_unfollow_users.isChecked(): # if only need to followback or unfollow_if, while loop should stop after 1st iteration
				break
	#dialog.counter_path = os.path.join(dialog.path_users_directory,dialog.username,"etc","counter",datetime.datetime.utcnow().strftime("%d-%m-%Y")+".txt") #or use today() instead of utcnow()
	#dialog.tracker_path = os.path.join(dialog.path_users_directory,dialog.username,"etc","tracker",datetime.datetime.utcnow().strftime("%d-%m-%Y")+".txt") #or use today() instead of utcnow()	
			
	def initialize_counter(self):
		shared_resource_lock.acquire()
		self.counter_path = os.path.join(self.path_users_directory,dialog.username,"etc","counter",datetime.datetime.utcnow().strftime("%d-%m-%Y")+".txt")
		self.tracker_path = os.path.join(self.path_users_directory,dialog.username,"etc","tracker",datetime.datetime.utcnow().strftime("%d-%m-%Y")+".txt")
		with open(self.counter_path,"w+") as f:
			f.write("following:0,unfollowing:0,like:0,unlike:0")
		self.count_dict = {"following":0,"unfollowing":0,"like":0,"unlike":0}
		shared_resource_lock.release()
		self.initialize_tracker()
	def initialize_tracker(self):
		shared_resource_lock.acquire()
		with open(self.tracker_path,"w+") as f:
			f.write("following:,unfollowing:,like:,unlike:")
		self.track_dict = {"following":[],"unfollowing":[],"like":[],"unlike":[]}
		shared_resource_lock.release()
	def read_counter(self):
		counter_path = os.path.join(self.path_users_directory,dialog.username,"etc","counter",datetime.datetime.utcnow().strftime("%d-%m-%Y")+".txt")
		if self.counter_path != counter_path: # if day expired
			self.initialize_counter()
		shared_resource_lock.acquire()
		_list = open(self.counter_path,"r").read().strip().split(",")
		self.count_dict = {each.split(":")[0] : int(each.split(":")[1]) for each in _list}
		shared_resource_lock.release()
		self.read_tracker()
	def read_tracker(self,tracker_path=""):
		if tracker_path:
			_list = open(tracker_path,"r").read().strip().split(",")
			track_dict = {each.split(":")[0] : list(filter(None,each.split(":")[1].split(";"))) for each in _list}
			return track_dict
		shared_resource_lock.acquire()
		_list = open(self.tracker_path,"r").read().strip().split(",")
		self.track_dict = {each.split(":")[0] : list(filter(None,each.split(":")[1].split(";"))) for each in _list} # <trick> use filter to remove '' from a list
		shared_resource_lock.release()
		if self.count_dict["following"] != self.track_dict["following"].__len__() or self.count_dict["unfollowing"] != self.track_dict["unfollowing"].__len__():
			write_me_log("\nBUZZ!!!!!!!!!!!!!!!!!!\n")
	def update_counter(self,key,value):
		write_me_log("Accessing update_counter()") # For DEBUG
		# In case date changed(in a new day), then it would have a new counter_path, so that implies a count_dict and text file(for counter_path) as well as track_dict & tracker_path
		self.counter_path = os.path.join(self.path_users_directory,dialog.username,"etc","counter",datetime.datetime.utcnow().strftime("%d-%m-%Y")+".txt")
		self.tracker_path = os.path.join(self.path_users_directory,dialog.username,"etc","tracker",datetime.datetime.utcnow().strftime("%d-%m-%Y")+".txt")
		if not os.path.exists(self.counter_path): # if day is a new day
			self.initialize_counter()
		shared_resource_lock.acquire()
		self.count_dict[key]+=1 # or self.count_dict.update({key:self.count_dict.get(key)+1})
		with open(self.counter_path,"w+") as f:
			f.write(','.join("{}:{}".format(each[0],each[1]) for each in list(self.count_dict.items())))
		shared_resource_lock.release()
		self.update_tracker(key,value)  ## counter_path  , tracker_path | count_dict , track_dict
	def update_tracker(self,key,value):
		shared_resource_lock.acquire()
		self.track_dict[key].append(value)
		with open(self.tracker_path,"w+") as f:
			f.write(','.join("{}:{}".format(each[0],';'.join(each[1])) for each in list(self.track_dict.items())))
		shared_resource_lock.release()
	# Find/Search suitable users from user own explore, other users comments & likes
	def find_suitable_users(self): # Partial Login required
		# variables
		page_num = 1
		has_next_page = True
		user_id = ""
		hashtag = ""
		data_type = "user"
		after = ""
		
		# choices
		if self.combo_find_users.currentText() == "Explore":
			#login if user not already logged in 
			if not self.successful_login: 
				self.login()
			hash = "ecd67af449fb6edab7c69a205413bfa7" #for explore, hash is private
			edge__by = "edge_web_discover_media"
			first = 24
			_type = "explore"
			after = 0
		elif (self.combo_find_users.currentText() == "Comments List from a User post feed" or self.combo_find_users.currentText() == "Likes List from a User post feed"):
			hash = "f2405b236d85e8296cf30347c9f08c2a" #hash is public
			edge__by = "edge_owner_to_timeline_media"
			first = 12
			_type = "post feed"
			user_name = self.line_find_users.text()
			if user_name:
				user_id = get_user_id_by_username(self,user_name)[0]
				# no sleep/wait gap required , since it only called for once
			if not user_id:
				user_does_not_exist(user_name)
				write_me_log("returned") # For Debug
				return # since it is unable to fetch user_id , no need to continue
				
		elif (self.combo_find_users.currentText() == "Comments List from a Hashtag" or self.combo_find_users.currentText() == "Likes List from a Hashtag"):
			hash = "f12c9ec5e46a3173b2969c712ad84744" #for ...
			edge__by = "edge_hashtag_to_media"
			first = 9
			_type = "hashtag feed"
			hashtag = str(self.line_find_users.text()).lower().replace("#","").strip() # wrapped str() to support python 2.7
			data_type = "hashtag"
		
		write_me_log(_type) 
		#print(self.min_followers.text(),self.max_followers.text(),self.follow_ratio.text()) # for Debug
		write_me_log(self.min_followers.text(),self.max_followers.text(),self.follow_ratio.text()) # for Debug
		
		while has_next_page:
			write_me_log(">>> Scanning {}: {} to {}".format(_type,((page_num-1)*first)+1,(page_num*first-1)+1))
			if not after:
				params = {'query_hash':hash,'variables':'{"first":'+str(first)+'}'}
			else:
				params = {'query_hash':hash,'variables':'{"first":'+str(first)+',"after":"'+str(after)+'"}'}
			if user_id: # only applicable for "Comments List from a User post feed" or "Likes List from a User post feed"
				params.update({'variables':params["variables"][:-1]+',"id":"'+user_id+'"}'})
			elif hashtag:
				params.update({'variables':params["variables"][:-1]+',"tag_name":"'+hashtag+'"}'})
			try:
				if _type == "explore":
					resp,excep = session_func(self.session_main,url_graphql,redirects=False,params=params,proxies=proxies)
				else:
					resp,excep = session_func(session_temp,url_graphql,redirects=False,params=params)
				if not excep:
					if resp and resp.status_code == 200:
						data = resp.json()
						has_next_page = bool(data["data"][data_type][edge__by]["page_info"]["has_next_page"])
						if has_next_page:
							if isinstance(after,int):
								after += 1
							else:
								after = data["data"][data_type][edge__by]["page_info"]["end_cursor"]
						post_lists = data["data"][data_type][edge__by]["edges"]
						#write_me_log(len(post_lists)) # For DEBUG purpose only
						for post in post_lists:
							if _type == "post feed" or _type == "hashtag feed":
								shortcode = post["node"]["shortcode"]
								write_me_log(shortcode) # For DEBUG
								res = None
								if self.combo_find_users.currentText() in ["Comments List from a User post feed","Comments List from a Hashtag"] and post["node"]["edge_media_to_comment"]["count"] > 0:
									write_me_log(post["node"]["edge_media_to_comment"]["count"]) # for DEBUG purpose
									res = get_post_details(shortcode,"comments","list") # return list of username's those who commented
								elif self.combo_find_users.currentText() in ["Likes List from a User post feed","Likes List from a Hashtag"] and post["node"]["edge_media_preview_like"]["count"] > 0:
									write_me_log(post["node"]["edge_media_preview_like"]["count"]) # for DEBUG purpose
									res = get_post_details(shortcode,"likes","list") # return list of username's those who liked
								if res:
									write_me_log(res) # For DEBUG
									for each_user_name in res:
										self.find_suitable_users_conditions(each_user_name)
								continue # its work is done here
							# For explore choice
							user_id  = post["node"]["owner"]["id"]
							user_name,ret = get_username_by_user_id_via_api(self,user_id)
							if not user_name:
								user_name = get_username_by_user_id(self,user_id)
							if user_name:
								self.find_suitable_users_conditions(user_name,ret)	
						page_num+=1
					else:
						write_me_log("[Err] {} Page not responding properly! \r\nStatus Code: {}".format(resp.url,resp.status_code))
				else:
					write_me_log("[Exception] Exception! <during : find_suitable_users()>")
					app_exit()
			except Exception as err:
				write_me_log("[Exception] exception error <during : find_suitable_users() >>> {}".format(err))
				app_exit()
			time.sleep(random.randrange(5,10)) 
		# End of while loop
		
	def find_suitable_users_conditions(self,user_name,ret=()):
		# Load scrapped list
		shared_resource_lock.acquire()
		my_list_follow = list(set(open(os.path.join(self.path_users_directory,self.username,"myList","follow.txt"),"r").read().strip(" ").split(",\n")))[:-1]
		shared_resource_lock.release()
		
		if user_name not in my_list_follow:
			if not ret:
				ret = get_user_details(self,user_name)
			#write_me_log(ret) # for DEBUG only
			if ret:
				followers = 1 if not ret[0] else ret[0] # <Trick> taken care, otherwise 'div by zero' exception would occur 
				if self.check_is_private.isChecked() and ret[2] :
					write_me_log("is_private")  # For DEBUG
					return
				if self.check_is_verified.isChecked() and ret[3]:
					write_me_log("is_verified")  # For DEBUG
					return
				if self.check_is_celebrity.isChecked() and  ret[4]:
					write_me_log("is_celebrity")  # For DEBUG
					return
				if (ret[0] >= int(self.min_followers.text()) and ret[0] <= int(self.max_followers.text()) and ret[1]/followers >= float(self.follow_ratio.text())):
					# set this suitable user to myList
					write_me_log(user_name)  # For DEBUG
					my_list_follow.append(user_name)
					shared_resource_lock.acquire()
					with open(os.path.join(self.path_users_directory,self.username,"myList","follow.txt"),"a+") as f:
						f.write("{},\n".format(user_name))
					shared_resource_lock.release()
			#write_me_log("wait")
			#time.sleep(random.randrange(5,10)) # wait #=> disabled, since get_user_details called session_func and session_func has its own wait
	# Find Following & Followers by username's
	def find_following_followers(self,own_account=False,account_file="",_my_following=[""]):
		global my_followers,my_following
		#login if user not already logged in 
		if not self.successful_login: 
			self.login()
		#vars
		user_names = []
		splitter = " "
		following_list = []
		followers_list = []
		if not own_account:
			if self.line_find_following_followers.text().strip():
				user_names = [each.strip().lower() for each in self.line_find_following_followers.text().strip().split(",") if each]
			elif self.textEdit_find_following_followers.toPlainText().strip():
				user_names+=[os.path.basename(each[:-1]).strip().lower() for each in self.textEdit_find_following_followers.toPlainText().strip().split("\n") if each and each.endswith("/")]
				user_names+=[os.path.basename(each).strip().lower() for each in self.textEdit_find_following_followers.toPlainText().strip().split("\n") if each and not each.endswith("/")]
			elif self.path_find_following_followers.text() and os.path.exists(self.path_find_following_followers.text()) and (self.path_find_following_followers.text().endswith(".txt") or self.path_find_following_followers.text().endswith(".csv")):
				file_content = open(self.path_find_following_followers.text(),"r").read().strip()
				if "," in file_content:
					splitter = ","
				elif ";" in file_content:
					splitter = ";"
				elif "\n" in file_content:
					splitter = "\n"
				elif " " in file_content:
					splitter = " "
				user_names = [each.strip().lower() for each in file_content.split(splitter) if each]
			else:
				QMessageBox.warning(self,"Warning!","Username field can't be blank")
		else:
			user_names = [self.username] # find followers of own account 
		write_me_log(user_names) # For Debug usage
		for user_name in user_names:
			target_user_id = get_user_id_by_username(self,user_name)[0]
			if target_user_id:
				# fetching directory information
				if self.username == user_name:
					_directory = os.path.join(self.path_users_directory,self.username,"myStatus")
				else:
					_directory = os.path.join(path_app_directory,"others",user_name)
				if not os.path.exists(_directory): # if user directory not present, create a one
					os.mkdir(_directory)
				#
				#write_me_log(_directory) # for DEBUG
				if (self.combo_find_following_followers.currentText() == "Followers"):
					followers_list = self.get_follow_list_of_a_username(target_user_id,"followers")
					create_or_get_follow_text_file(_directory,["followers.txt"],[followers_list]) # create
				elif (self.combo_find_following_followers.currentText() == "Following"):
					following_list = self.get_follow_list_of_a_username(target_user_id,"following")
					create_or_get_follow_text_file(_directory,["following.txt"],[following_list])  # create
				elif (self.combo_find_following_followers.currentText() == "Following+Followers" or self.combo_find_following_followers.currentText() == "Followback" or self.combo_find_following_followers.currentText() == "Fan"):
					followers_list = self.get_follow_list_of_a_username(target_user_id,"followers")
					following_list = self.get_follow_list_of_a_username(target_user_id,"following")
					following_and_followers_list = list(set(followers_list) | set(following_list))
					followback_list = list(set(followers_list) & set(following_list)) # intersection
					fan_list = list(set(followers_list) - set(followback_list))
					create_or_get_follow_text_file(_directory,["followers.txt","following.txt","followers+following.txt","followback.txt","fan.txt"],[followers_list,following_list,following_and_followers_list,followback_list,fan_list])  # create
				# in case user want to use auto followback feature, myList/follow.txt file need to be updated from followers_list
				# OR in case user want to use auto unfollow_all feature, myList/unfollow.txt file need to be updated from following_list
				if own_account:
					my_followers = followers_list if followers_list else my_followers # my_followers need to declare as global variable, because it is an assignment 
					my_following = following_list if following_list else my_following # my_following need to declare as global variable, because it is an assignment 
					if account_file:
						users_list = followers_list if followers_list else following_list
						shared_resource_lock.acquire()
						# get list of users to follow from myList/follow.txt Or myList/unfollow.txt 
						my_list_follow_or_unfollow = list(set(open(os.path.join(self.path_users_directory,self.username,"myList",account_file),"r").read().strip(" ").split(",\n")))[:-1]
						if _my_following:
							_my_following = my_following
						#update myList/follow.txt Or myList/unfollow.txt file
						with open(os.path.join(self.path_users_directory,self.username,"myList",account_file),"a+") as f:
							for each_user in users_list:
								if each_user not in _my_following and each_user not in my_list_follow_or_unfollow:
									f.write("{},\n".format(each_user))
						shared_resource_lock.release()
						# also need to update fan.txt & followback.txt files 
						#TO_DO_LIST()
			else:
				user_does_not_exist(user_name)
			write_me_log("wait")
			time.sleep(random.randrange(5,10)) # wait
	def get_follow_list_of_a_username(self,target_user_id,_type):
		# checking whether command is to scan followers list or following list
		if _type == "followers":
			private_hash = "c76146de99bb02f6415203be841dd25a" #for followers
			edge__by = "edge_followed_by"
		else:
			private_hash = "d04b0a864b4b54837c0d870b0e77e076" #for followings
			edge__by = "edge_follow"
		
		follow_list = []
		
		page_num = 1
		has_next_page = True
		after = ""
		first = 24
		write_me_log(_type) 
		
		while has_next_page:
			write_me_log(">>> Scanning {}: {} to {}".format(_type,((page_num-1)*first)+1,(page_num*first-1)+1))
			if not after:
				params = {'query_hash':private_hash,'variables':'{"include_highlight_reels":false,"include_reel":true,"id":'+target_user_id+',"fetch_mutual":true,"first":'+str(first)+'}'}
			else:
				params = {'query_hash':private_hash,'variables':'{"include_highlight_reels":false,"include_reel":true,"id":'+target_user_id+',"fetch_mutual":true,"first":'+str(first)+',"after":"'+after+'"}'}
			#try
			resp,excep = session_func(self.session_main,url_graphql,params=params,redirects=False,proxies=proxies)
			if not excep:
				if resp and resp.status_code == 200:
					data = resp.json()
					has_next_page = bool(data["data"]["user"][edge__by]["page_info"]["has_next_page"])
					if has_next_page:
						after = data["data"]["user"][edge__by]["page_info"]["end_cursor"]
					user_lists = data["data"]["user"][edge__by]["edges"]	
					for user in user_lists:
						id_to_user[user["node"]["id"]] = user["node"]["username"]
						follow_list.append(user["node"]["username"])
					page_num+=1
				else:
					write_me_log("[Err] {} Page not responding properly! \r\nStatus Code: {}".format(resp.url,resp.status_code))
			else:
				write_me_log("[Exception] Exception! <during : get_follow_list_of_a_username()>")
				app_exit()
			#except Exception as err:
			#write_me_log("[Exception] exception error <during : get_follow_list_of_a_username() >>> {}".format(err))
			#app_exit()
			time.sleep(random.randrange(5,10))
		# End of while loop
		
		return follow_list
	# Download posts
	def downloading(self): # Partial Login required
		# variables
		page_num = 1
		has_next_page = True
		user_id = ""
		hashtag = ""
		data_type = "user"
		after = ""
		
		# choices
		if self.combo_download_type.currentText() == "Explore":
			#login if user not already logged in 
			if not self.successful_login: 
				self.login()
			hash = "ecd67af449fb6edab7c69a205413bfa7" #for explore, hash is private
			edge__by = "edge_web_discover_media"
			first = 24
			_type = "explore"
			after = 0
		elif (self.combo_download_type.currentText() == "Username"):
			hash = "f2405b236d85e8296cf30347c9f08c2a" #hash is public
			edge__by = "edge_owner_to_timeline_media"
			first = 12
			_type = "post feed"
			user_name = self.line_download_type.text()
			if user_name:
				user_id = get_user_id_by_username(self,user_name)[0]
				# no sleep/wait gap required , since it only called for once
			if not user_id:
				user_does_not_exist(user_name)
				write_me_log("returned") # For Debug
				return # since it is unable to fetch user_id , no need to continue	
		elif (self.combo_download_type.currentText() == "Hashtag"):
			hash = "f12c9ec5e46a3173b2969c712ad84744" #for ...
			edge__by = "edge_hashtag_to_media"
			first = 9
			_type = "hashtag feed"
			hashtag = str(self.line_download_type.text()).lower().replace("#","").strip() # wrapped str() to support python 2.7
			data_type = "hashtag"
		
		write_me_log(_type) 
		
		while has_next_page:
			write_me_log(">>> Scanning {}: {} to {}".format(_type,((page_num-1)*first)+1,(page_num*first-1)+1))
			if not after:
				params = {'query_hash':hash,'variables':'{"first":'+str(first)+'}'}
			else:
				params = {'query_hash':hash,'variables':'{"first":'+str(first)+',"after":"'+str(after)+'"}'}
			if user_id: # only applicable for "post feed"
				params.update({'variables':params["variables"][:-1]+',"id":"'+user_id+'"}'})
			elif hashtag:
				params.update({'variables':params["variables"][:-1]+',"tag_name":"'+hashtag+'"}'})
			try:
				if _type == "explore":
					resp,excep = session_func(self.session_main,url_graphql,redirects=False,params=params,proxies=proxies)
				else:
					resp,excep = session_func(session_temp,url_graphql,redirects=False,params=params)
				if not excep:
					if resp and resp.status_code == 200:
						# print(resp.url) For GEBUG
						data = resp.json()
						has_next_page = bool(data["data"][data_type][edge__by]["page_info"]["has_next_page"])
						if has_next_page:
							if isinstance(after,int):
								after += 1
							else:
								after = data["data"][data_type][edge__by]["page_info"]["end_cursor"]
						post_lists = data["data"][data_type][edge__by]["edges"]
						self.download_posts(post_lists)
						page_num+=1
					else:
						write_me_log("[Err] {} Page not responding properly! \r\nStatus Code: {}".format(resp.url,resp.status_code))
				else:
					write_me_log("[Exception] Exception! <during : downloading()>")
					app_exit()
			except Exception as err:
				write_me_log("[Exception] exception error <during : downloading() >>> {}".format(err))
				app_exit()
			time.sleep(random.randrange(5,10)) 
		# End of while loop
	def download_posts(self,post_lists): # No Login required
		# vars
		get_post_age = 1 if self.radio_download_post_age_today.isChecked() else 7 if self.radio_download_post_age_week.isChecked() else 30 if self.radio_download_post_age_month.isChecked() else 999999
		get_post_type = 'GraphImage' if self.radio_download_type_image.isChecked() else 'GraphSidecar' if self.radio_download_type_slider.isChecked() else 'GraphVideo' if self.radio_download_type_video.isChecked() else 'All'
		write_me_log(get_post_age,get_post_type) # for DEBUG
		ret = ()
		
		# creating mandatory directory for posts
		if post_lists:
			if self.combo_download_type.currentText() == "Explore":
				_directory = os.path.join(self.path_users_directory,self.username,"explore")
			elif self.combo_download_type.currentText() == "Username":
				if self.username == self.line_download_type.text():
					_directory = os.path.join(self.path_users_directory,self.username,"myStatus","posted")
				else:
					_directory = os.path.join(path_app_directory,"others",self.line_download_type.text())
			else:
				_directory = os.path.join(path_app_directory,"hashes",self.line_download_type.text())
			if not os.path.exists(_directory): # if user directory not present, create a one
				os.mkdir(_directory)
		
		write_me_log(len(post_lists))
		for post in post_lists:
			try:
				urls = []
				string = ""
				video_view_count = ""
				# check if post type is All or specific
				if get_post_type == "All" or get_post_type == post["node"]["__typename"]:
					t1 = datetime.datetime.utcfromtimestamp(post["node"]["taken_at_timestamp"]).replace(microsecond=0)
					t2 = datetime.datetime.utcnow().replace(microsecond=0)
					post_age = (t2-t1).days
					# Checking if post age within set limit
					if post_age < get_post_age:
						# if post contains multiple images or slides
						if post["node"]["__typename"] == "GraphSidecar" and post.get('node').get('edge_sidecar_to_children'): # <Trick> always check if nearest attribute of the json could be reachable before direct accessing via [''] 
							for sub_post in post['node']['edge_sidecar_to_children']['edges']:
								write_me_log(sub_post['node']['display_url']) # for DEBUG
								urls.append(sub_post['node']['display_url'])
						#if post is a video
						elif post["node"]["__typename"] == "GraphVideo":
							##post_url = url_home+'p/'+post["node"]["shortcode"]
							post_url = url_home+'p/'+post["node"]["shortcode"]+"?__a=1"
							resp,excep = session_func(session_temp,post_url)
							if not excep:
								if resp and resp.status_code == 200:
									video_url = resp.json().get("graphql").get("shortcode_media").get("video_url")
									video_view_count = resp.json().get("graphql").get("shortcode_media").get("video_view_count")
									write_me_log(video_url) # for DEBUG
									##video_url = re.search('(?<="video_url":")[a-zA-Z0-9:/.=?_-]+', resp.text).group(0) # deprecated
									#video_view_count = re.search('(?<="video_view_count":)[0-9]+', resp.text).group(0)
									urls.append(video_url)
								else:
									write_me_log("[Err] {} Page not responding properly! \r\nStatus Code: {}".format(resp.url,resp.status_code))
							else:
								write_me_log("[Exception] Exception! <during : download_posts()>")
								app_exit()
						# if post contains single image
						else:
							write_me_log(post["node"]["display_url"]) # for DEBUG
							urls.append(post["node"]["display_url"])
						# Creating folder for the post
						if not os.path.exists(os.path.join(_directory,post["node"]["shortcode"])):
							os.mkdir(os.path.join(_directory,post["node"]["shortcode"]))
						# Downloading & Saving files to directory
						for idx,each_url in enumerate(urls):
							resp,excep = session_func(session_temp,each_url)
							if not excep:
								if resp and resp.status_code == 200:
									if len(urls) > 1:
										name = "{}-{}.{}".format(post["node"]["shortcode"],idx+1,each_url.split("?")[0].split(".")[-1])
									else:
										name = "{}.{}".format(post["node"]["shortcode"],each_url.split("?")[0].split(".")[-1])
									with open(os.path.join(_directory,post["node"]["shortcode"],name),"wb+") as f:
										f.write(resp.content)
								else:
									write_me_log("[Err] {} Page not responding properly!! \r\nStatus Code: {}".format(resp.url,resp.status_code))
							else:
								write_me_log("[Exception] Exception!! <during : download_posts()>")
								app_exit()
						# preparing STAT file
						if not ret or self.combo_download_type.currentText() != "Username":
							user_name,ret = get_username_by_user_id_via_api(self,post["node"]["owner"]["id"],login=False)
							if not ret:
								user_name = get_username_by_user_id(self,post["node"]["owner"]["id"])
								if user_name:
									ret = get_user_details(self,user_name)
						if ret:
							string += "Full Name : {}\n Posts Count : {}\n Followers : {}\n Following : {}\n Private Account? : {}\n Verified Account? : {}\n Business Account? : {}\n".format(ret[5],ret[6],ret[0],ret[1],ret[2],ret[3],ret[4])
						string += " Post type : {}\n".format(post["node"]["__typename"].replace("Graph",""))
						string += " Comments : {}\n".format(post["node"]["edge_media_to_comment"]["count"])
						#print(post["node"]["edge_media_to_comment"]["count"])
						if self.combo_download_type.currentText() == "Explore":
							string += " Likes : {}\n".format(post["node"]["edge_liked_by"]["count"])
						else:
							string += " Likes : {}\n".format(post["node"]["edge_media_preview_like"]["count"]) 
						if video_view_count:
							string += " Views : {}\n".format(video_view_count)
						#print(post["node"]["edge_liked_by"]["count"])
						##print(post["node"]["dimensions"]["height"])
						##print(post["node"]["dimensions"]["width"])
						string += " Post Created at : {}\n".format(datetime.datetime.utcfromtimestamp(post["node"]["taken_at_timestamp"]).strftime('%Y-%m-%d %H:%M:%S'))
						#print(datetime.datetime.utcfromtimestamp(post["node"]["taken_at_timestamp"]).strftime('%Y-%m-%d %H:%M:%S'))
						try:
							string += " Image may contain : {}\n".format(post["node"]["accessibility_caption"])
							#print(post["node"]["accessibility_caption"])
						except:
							pass
						if len(post["node"]["edge_media_to_caption"]["edges"]):
							content_text = post["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]
							string += " Text : {}\n".format(content_text)
							##print(content_text.encode("utf-8"))
							#print(content_text.encode("ascii",errors="ignore"))
							if content_text.strip():
								hashes = [_each for _each in content_text.strip().replace("\n"," ").replace("#"," #").strip().split("\n")[-1].split(" ") if _each.startswith("#")] # <Trick> replace # with [SPACE]#, so if hashes exist without any space, it will create a space(which is splitting value here) between them in the text.
								string += " Hashes : {}\n".format(' '.join(hashes))
								string += " Number of Hashes : {}\n".format(len(hashes))
						# Saving STAT file
						with open(os.path.join(_directory,post["node"]["shortcode"],"statistic.txt"),"wb+") as f:
							f.write(string.encode("utf-8")) # <class 'bytes'>
			except Exception as err:
				write_me_log("[Exception] exception error <during : download_posts() >>> {}".format(err))
				app_exit()

	# ------- SLOTS -------
	# Find suitable users
	def add_find_users_task(self):
		#checking whether user added an IG account or not 
		if not self.username:
			QMessageBox.warning(self,"Warning!","To search suitable users, at first you have to add a user account in 'Accounts Settings' Panel")
		else:
			queue.put(self.find_suitable_users)
	# Find Following & Followers
	def add_find_following_followers_task(self):
		if not self.username:
			QMessageBox.warning(self,"Warning!","To find following/followers of a IG user, at first you have to add a user account in 'Accounts Settings' Panel")
		else:
			queue.put(self.find_following_followers)
	# Follow/Unfollow
	def add_unfollow_task(self):
		if not self.username:
			QMessageBox.warning(self,"Warning!","To unfollow others, at first you have to add a user account in 'Accounts Settings' Panel")
		else:
			queue.put(self.unfollow_user)
	def add_follow_task(self):
		if not self.username:
			QMessageBox.warning(self,"Warning!","To follow others, at first you have to add a user account in 'Accounts Settings' Panel")
		else:
			queue.put(self.follow_user)
			###queue.put(self.temp_to_do)
	# Download Posts
	def add_download_post_task(self):
		queue.put(self.downloading)	
	# @@@@@@@@@@@@@@@@@@@@@@@@
	# Download posts
	def select_download_type(self):
		if (self.combo_download_type.currentText() == "Explore"):
			if self.username:
				self.line_download_type.setText(self.username)
			else:
				self.line_download_type.setText("[At first, add an Instagram account]")
			self.line_download_type.setReadOnly(True)
		elif (self.combo_download_type.currentText() == "Username"):
			self.line_download_type.clear()
			self.line_download_type.setReadOnly(False)
			self.line_download_type.setPlaceholderText("Add a username (eg, ronaldo)")
		elif (self.combo_download_type.currentText() == "Hashtag"):
			self.line_download_type.clear()
			self.line_download_type.setReadOnly(False)
			self.line_download_type.setPlaceholderText("Add a hashtag (eg, #ok)")
	# Find suitable users
	def select_find_users(self):
		if (self.combo_find_users.currentText() == "Explore"):
			if self.username:
				self.line_find_users.setText(self.username)
			else:
				self.line_find_users.setText("[At first, add an Instagram account]")
			self.line_find_users.setReadOnly(True)
		elif (self.combo_find_users.currentText() == "Comments List from a User post feed" or self.combo_find_users.currentText() == "Likes List from a User post feed"):
			self.line_find_users.clear()
			self.line_find_users.setReadOnly(False)
			self.line_find_users.setPlaceholderText("Add a username (eg, ronaldo)")
		elif (self.combo_find_users.currentText() == "Comments List from a Hashtag" or self.combo_find_users.currentText() == "Likes List from a Hashtag"):
			self.line_find_users.clear()
			self.line_find_users.setReadOnly(False)
			self.line_find_users.setPlaceholderText("Add a hashtag (eg, #ok)")
	# Like/Unlike	
	def browse_like_posts(self):
		if (self.combo_like_posts.currentText() == "Like Posts from my List"):
			self.button_like_posts.show()
			self.check_like_posts.hide()
			self.radio_like_posts1.setChecked(True)
			self.radio_like_posts1.setEnabled(False)
			self.radio_like_posts2.setEnabled(False)
		else:
			self.button_like_posts.hide()
			self.check_like_posts.show()
			self.radio_like_posts2.setChecked(True)
			self.radio_like_posts1.setEnabled(True)
			self.radio_like_posts2.setEnabled(True)
			
		if (self.combo_like_posts.currentText() == "Like Posts from Hashtags"):
			self.path_like_posts.clear()
			self.path_like_posts.setPlaceholderText("Add a hashtag (eg, #ok)")
			self.path_like_posts.setReadOnly(False)
		elif (self.combo_like_posts.currentText() == "Like Posts from User post feeds"):
			self.path_like_posts.clear()
			self.path_like_posts.setPlaceholderText("Add a username (eg, ronaldo)")
			self.path_like_posts.setReadOnly(False)
		elif (self.combo_like_posts.currentText() == "Like Posts from Explore"):
			if self.username:
				self.path_like_posts.setText(self.username)
			else:
				self.path_like_posts.setText("[At first, add an Instagram account]")
			self.path_like_posts.setReadOnly(True)
		else:
			self.path_like_posts.clear()
			self.path_like_posts.setPlaceholderText("Text(.txt) file location")
			self.path_like_posts.setReadOnly(False)
	# Follow/Unfollow
	def select_follow_users(self):
		if (self.combo_follow_users.currentText() == "Follow users from my List"):
			self.path_follow_users.show()
			self.button_follow_users.show()
		else:
			self.path_follow_users.hide()
			self.button_follow_users.hide()
	
	def select_unfollow_users(self):
		if (self.combo_unfollow_users.currentText() == "Auto Unfollow users those did not followback"):
			self.check_unfollow_users.show()
			self.followback_day_limit.show()
			self.check_unfollow_users.setChecked(True)
		else:
			self.check_unfollow_users.hide()
			self.followback_day_limit.hide()
			self.check_unfollow_users.setChecked(False)
			
		if (self.combo_unfollow_users.currentText() == "Unfollow users form my List"):
			self.path_unfollow_users.show()
			self.button_unfollow_users.show()
			#
			self.check_is_private_2.hide()
			self.check_is_verified_2.hide()
			self.check_is_celebrity_2.hide()
			#
			self.label_exclude.hide()
			#
			self.check_is_private_2.setChecked(False)
			self.check_is_verified_2.setChecked(False)
			self.check_is_celebrity_2.setChecked(False)
			self.check_unfollow_users.setChecked(False)
		else:
			self.path_unfollow_users.hide()
			self.button_unfollow_users.hide()
			#
			self.label_exclude.show()
			#
			self.check_is_private_2.show()
			self.check_is_verified_2.show()
			self.check_is_celebrity_2.show()
			#
			self.check_is_private_2.setChecked(True)
			self.check_is_verified_2.setChecked(True)
			self.check_is_celebrity_2.setChecked(True)
			self.check_unfollow_users.setChecked(True)
			
		if (self.combo_unfollow_users.currentText() == "Unfollow all"):
			self.check_unfollow_users.setChecked(False)
			
	def browse_follow_users(self):
		file_location = QFileDialog.getOpenFileName(self,caption="Load Text file",directory=".",filter=".txt file (*.txt)")
		self.path_follow_users.setText(QDir.toNativeSeparators(file_location[0]))
	def browse_unfollow_users(self):
		file_location = QFileDialog.getOpenFileName(self,caption="Load Text file",directory=".",filter=".txt file (*.txt)")
		self.path_unfollow_users.setText(QDir.toNativeSeparators(file_location[0]))
		
	# Find Following & Followers
	def browse_following_followers(self):
		file_location = QFileDialog.getOpenFileName(self,caption="Load Text or CSV file",directory=".",filter=".txt or .csv file (*.txt *.csv)")
		self.path_find_following_followers.setText(QDir.toNativeSeparators(file_location[0]))
		
	# Account Settings
	
		
	def addAccount(self):
		_proxy = ""
		if not self.username: # if no user added previously
			if self.line_username.text() and self.line_password.text(): # if fields of username & password is not empty
				# fetching data from fields
				username = QTableWidgetItem(self.line_username.text())
				username.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled) # to make item non editable
				##password = QTableWidgetItem(self.line_password.text())
				password = QTableWidgetItem(len(self.line_password.text())*'*')
				password.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled) # to make item non editable
				if self.line_proxy_ip.text():
					if self.line_proxy_port.text():
						_proxy = self.line_proxy_ip.text()+":"+self.line_proxy_port.text()
					else:
						_proxy = self.line_proxy_ip.text()
					if self.line_proxy_user.text() and self.line_proxy_password.text():
						_proxy = self.line_proxy_user.text()+":"+self.line_proxy_password.text()+"@"+self.line_proxy_ip.text()+":"+self.line_proxy_port.text()
					proxy = QTableWidgetItem(_proxy)
				else:
					proxy = QTableWidgetItem(_proxy)
				# preparing tableWidget for next row insert
				self.logintable.insertRow(self.logintable.rowCount())
				# setting data to tableWidget
				self.logintable.setItem(self.logintable.rowCount()-1, 0, username)
				self.logintable.setItem(self.logintable.rowCount()-1, 1, password)  
				self.logintable.setItem(self.logintable.rowCount()-1, 2, proxy)
				# setting variables
				self.username,self.password,self.proxy = self.line_username.text(),self.line_password.text(),_proxy # dont assign from username or password or proxy variables, because they are of type: QTableWidgetItem
				write_me_log (self.proxy) # for debug
				# saving user data to a text file
				self.addAccoutToFile(self.line_username.text(),self.line_password.text(),_proxy)
				# clearing fields data
				self.line_username.clear()
				self.line_password.clear()
				self.line_proxy_ip.clear()
				self.line_proxy_port.clear()
				self.line_proxy_user.clear()
				self.line_proxy_password.clear()
				# set path for Follow users
				self.path_follow_users.setText(QDir.toNativeSeparators(os.path.join(self.path_users_directory,self.username,"myList","follow.txt")))
				self.path_unfollow_users.setText(QDir.toNativeSeparators(os.path.join(self.path_users_directory,self.username,"myList","unfollow.txt")))
				#self.button_follow_users.setEnabled(True) # browse button enabled
				#self.button_unfollow_users.setEnabled(True) # browse button enabled
				#set username in lineEdit fields
				self.path_like_posts.setText(self.username)
				self.line_find_users.setText(self.username)
				self.line_download_type.setText(self.username)
			else:
				QMessageBox.warning(self,"Warning!","username & password field can't be empty.")
		else:
			if directory_chnaged:
				QMessageBox.information(self,"Information","Watch My Video Tutorial, to see how you can use multiple accounts with multiple App instances.")
				url = QUrl('https://github.com/mediabots/InstagramBot-GUI-Python')
				QDesktopServices.openUrl(url)
			else:
				QMessageBox.information(self,"Information","A user is already exist.\nPlease check below location:\n {}".format(self.path_users_directory))
		
	def addAccoutToFile(self,username,password,proxy):
		if os.path.exists(self.path_users_directory):
			if not os.path.exists(os.path.join(self.path_users_directory,username)):
				os.mkdir(os.path.join(self.path_users_directory,username))
			with open(os.path.join(self.path_users_directory,username,username+".txt"),"w+") as f:
				f.write("{},{},{}\n".format(username,password,proxy))
			# create default directories for a user
			self.addOtherFiles()
		else:
			write_me_log("[Error] users Directory not present under {}\r\nExiting......".format(self.path_users_directory))
			app_exit()
	def addOtherFiles(self):
		if not os.path.exists(os.path.join(self.path_users_directory,self.username,"myList")):
			os.mkdir(os.path.join(self.path_users_directory,self.username,"myList"))
		if not os.path.exists(os.path.join(self.path_users_directory,self.username,"myList","follow.txt")):
			with open(os.path.join(self.path_users_directory,self.username,"myList","follow.txt"),"w+") as f:
				f.write("leomessi,\nshakira,\nronaldo,\nnature,\ntomhardy,\nmariasharapova,\n")
		if not os.path.exists(os.path.join(self.path_users_directory,self.username,"myList","unfollow.txt")):
			with open(os.path.join(self.path_users_directory,self.username,"myList","unfollow.txt"),"w+") as f:
				f.write("")
		if not os.path.exists(os.path.join(self.path_users_directory,self.username,"myStatus")):
			os.mkdir(os.path.join(self.path_users_directory,self.username,"myStatus"))
		if not os.path.exists(os.path.join(self.path_users_directory,self.username,"etc")):
			os.mkdir(os.path.join(self.path_users_directory,self.username,"etc"))
		if not os.path.exists(os.path.join(self.path_users_directory,self.username,"etc","counter")):
			os.mkdir(os.path.join(self.path_users_directory,self.username,"etc","counter"))
		if not os.path.exists(os.path.join(self.path_users_directory,self.username,"etc","tracker")):
			os.mkdir(os.path.join(self.path_users_directory,self.username,"etc","tracker"))
			
	def removeAccount(self):
		index_list = []
		user_ids = []
		for each_select in self.logintable.selectionModel().selectedRows():
			user_ids.append(each_select.data())
			index = QPersistentModelIndex(each_select)      
			index_list.append(index)
		for index in index_list:
			self.logintable.removeRow(index.row())
		self.removeAccountFromFile(user_ids) # remove user details from text file
		self.username = "" # reset self.username
		self.path_follow_users.clear() # clear slef.path_follow_users filed
		self.path_unfollow_users.clear() # clear slef.path_unfollow_users filed
		self.button_follow_users.setEnabled(False) # browse button disabled
		self.button_unfollow_users.setEnabled(False) # browse button disabled
		#unset username in lineEdit fields
		self.path_like_posts.setText("[At first, add an Instagram account]")
		self.line_find_users.setText("[At first, add an Instagram account]")
		self.line_download_type.setText("[At first, add an Instagram account]")
	def removeAccountFromFile(self,user_ids):
		for folder_ in os.listdir(self.path_users_directory):
				if os.path.isdir(os.path.join(self.path_users_directory,folder_)) and folder_ in user_ids:
					for file_ in os.listdir(os.path.join(self.path_users_directory,folder_)):
						if os.path.isfile(os.path.join(self.path_users_directory,folder_,file_)) and file_.endswith(".txt") and os.path.splitext(file_)[0] in user_ids: # splitext() to discard extension
							os.remove(os.path.join(self.path_users_directory,folder_,file_))
				
		
	def removeAccount_(self): # deprecated, not working properly
		selected = self.logintable.selectionModel().selectedRows()
		for each_ in selected:
			self.logintable.removeRow(each_.row())
			#write_me_log(each_.data())
			
	def login_data_changed(self):
		item = self.logintable.currentItem()
		try:
			proxy = item.text()
			username = self.logintable.item(item.row(),0).text() # <Doc> format item(row,column).text() ;where column -> 0, because username is in column 0
			self.updateAccountToFile(username,proxy)
		except:
			pass
		
	def updateAccountToFile(self,username,proxy):
		for folder_ in os.listdir(self.path_users_directory):
			if os.path.isdir(os.path.join(self.path_users_directory,folder_)) and folder_ == username:
				for file_ in os.listdir(os.path.join(self.path_users_directory,folder_)):
					if os.path.isfile(os.path.join(self.path_users_directory,folder_,file_)) and file_.endswith(".txt") and os.path.splitext(file_)[0] == username: # <trick> splitext() to discard extension
						file_path = os.path.join(self.path_users_directory,folder_,file_)
						file_content = open(file_path,"r").read()
						with open(file_path,"w+") as f:
							f.write("") # clear previous content (may be not required due to w+ mode)
							if file_content.split(",")[2].strip() == "" : #in case no proxy was not there
								f.write(file_content.replace(file_content.split(",")[2],proxy+"\n")) # update new proxy
							else:
								f.write(file_content.replace(file_content.split(",")[2].strip(),proxy)) # update new proxy
	def enable_multi_account(self):
		if thread_list.__len__():
			QMessageBox.warning(self,"Warning","Currently App is processing some task.\n To enable this feature, either wait for completion of the task or Restart the App")	
		else:
			with open(os.path.join(os_user_directory,documents,"MediaBOTS","InstagramBOT","multi_enabled.txt"),"w") as f:
				f.write(os.path.join(os_user_directory,documents,"MediaBOTS","InstagramBOT","multi_enabled.txt"))
			self.label_enable_multi_users_1.hide()
			self.label_enable_multi_users_2.show()
			self.button_enable_multi_account.setEnabled(False)
			self.button_enable_multi_account.setText("Multiple Account Support Enabled")
			QMessageBox.warning(self,"Warning","Multiple Account Support successfully Enabled.\n App is going to close within 5 seconds, to make this change effective.")
			time.sleep(5)
			app_exit()
	# etc
	def Clicked(self):
		for i in range(9):
			if self.listwidget.item(i).isSelected():
				self.tabWidget.setCurrentIndex(i)
			
	def Changed(self):
		for i in range(9):
			if self.tabWidget.currentIndex() == i:
				self.listwidget.item(i).setSelected(True)
				
	def newwindow(self):
		self.wid = QDialog()
		self.wid.setSizeGripEnabled(False)
		self.wid.setModal(True)
		self.wid.resize(250, 150)
		self.wid.setMinimumSize(QSize(250, 150))
		self.wid.setMaximumSize(QSize(250, 150))
		self.wid.setFixedSize(QSize(250, 150))
		self.wid.setWindowTitle('NewWindow')
		
		self.wid.layout = QVBoxLayout()
		self.wid.combobox = QComboBox()
		self.wid.combobox.addItems(["Item 1","Item 2","Item 3"])
		close = QPushButton("Close")
		
		self.wid.layout.addWidget(self.wid.combobox)
		self.wid.layout.addWidget(close)
		
		self.wid.setLayout(self.wid.layout)
		
		close.clicked.connect(self.wid.close)
		self.wid.combobox.currentIndexChanged.connect(self.change)
		
		self.wid.setFocus()
		
		self.wid.show()

	def change(self):
		text = self.wid.combobox.currentText()
		index = self.wid.combobox.currentIndex()
		write_me_log("text : {} at index {}".format(text,index))

class MovieSplashScreen(QSplashScreen):
	def __init__(self, movie, parent = None):
		movie.jumpToFrame(0)
		pixmap = QPixmap(movie.frameRect().size())

		QSplashScreen.__init__(self, pixmap)
		self.movie = movie
		self.movie.frameChanged.connect(self.repaint)

	def showEvent(self, event):
		self.movie.start()

	def hideEvent(self, event):
		self.movie.stop()

	def paintEvent(self, event):
		painter = QPainter(self)
		pixmap = self.movie.currentPixmap()
		self.setMask(pixmap.mask())
		painter.drawPixmap(0, 0, pixmap)

	def sizeHint(self):
		return self.movie.scaledSize()
		
class MyThread(Thread):	
	def __init__(self,name):
		Thread.__init__(self)
		self.name = name
		self._stop = threading.Event() 
	def stop(self): 
		self._stop.set() 
	def stopped(self): 
		return self._stop.isSet() 
	def run(self):
		## global dialog,queue,thread_list
		global log_path,dialog # not so sure about dialog, may be it not required. 
		while True: # endless
			#write_me_log ("Starting " + self.name + "\n")
			time.sleep(1) # recheck in every 5 secs
			# updating path related to datetime/time 
			log_path = os.path.join(os_user_directory,documents,"MediaBOTS","InstagramBOT","Logs",datetime.datetime.now().strftime("%d-%m-%Y")+".txt")
			##dialog.counter_path = os.path.join(dialog.path_users_directory,dialog.username,"etc","counter",datetime.datetime.utcnow().strftime("%d-%m-%Y")+".txt") #or use today() instead of utcnow()
			##dialog.tracker_path = os.path.join(dialog.path_users_directory,dialog.username,"etc","tracker",datetime.datetime.utcnow().strftime("%d-%m-%Y")+".txt") #or use today() instead of utcnow()	
			#
			c=0
			len_thread_list = len(thread_list)
			while len_thread_list > c:
				for each in thread_list:
					if not each.isAlive() and each.ident: # if thread was started and stopped now
						thread_list.remove(each)
						if each.name == "find_suitable_users":
							dialog.button_find_users_task.setEnabled(True)
						elif each.name == "follow_user":
							dialog.button_follow_task.setEnabled(True)
						elif each.name == "unfollow_user":
							dialog.button_unfollow_task.setEnabled(True)
						elif each.name == "find_following_followers":
							dialog.button_find_following_followers_task.setEnabled(True)
						elif each.name == "downloading":
							dialog.button_download_post_task.setEnabled(True)
					c+=1
			if not queue.empty():
				item = queue.get()
				write_me_log ("name : "+item.__name__)
				self.process_queue(item)
			#write_me_log ("Exiting " + self.name + "\n")
	def process_queue(self,item):
		##global thread_list
		_class = item.__self__.__class__
		_class_name = item.__self__.__class__.__name__
		_instance = item.__self__
		if item.__name__ not in [each.name for each in thread_list]:
			shared_resource_lock.acquire()
			thread_list.append(Thread(name=item.__name__,target=item))
			thread_list[len(thread_list)-1].setDaemon(True)
			thread_list[len(thread_list)-1].start() # start a individual thread (sun threads)
			shared_resource_lock.release()
			if thread_list[len(thread_list)-1].name == "find_suitable_users":
				_instance.button_find_users_task.setEnabled(False)
			elif thread_list[len(thread_list)-1].name == "follow_user":
				_instance.button_follow_task.setEnabled(False)
			elif thread_list[len(thread_list)-1].name == "unfollow_user":
				_instance.button_unfollow_task.setEnabled(False)
			elif thread_list[len(thread_list)-1].name == "find_following_followers":
				_instance.button_find_following_followers_task.setEnabled(False)
			elif thread_list[len(thread_list)-1].name == "downloading":
				_instance.button_download_post_task.setEnabled(False)
			
class MyGuiThreadTwo(QThread):
	##global gui_queue,dialog
	def __init__(self,name):
		QThread.__init__(self)
		self.name = name
	def __del__(self):
		self.wait()
	def run(self):
		while True:
			time.sleep(5) # recheck in every 5 secs
			if not gui_queue.empty():
				while not gui_queue.empty():
					with threading.Lock():
						dialog.label_status.setText(str(gui_queue.get()))
					time.sleep(1) # hold on for 1 secs
# subclass to check whether a new app version is available 

class ThreadCheckStatus(QThread):   
	##global dialog,thread_list
	try:
		signalCheckStatus = QtCore.Signal(str) 
	except:
		#Or pyqtSignal for PyQt4
		signalCheckStatus = QtCore.pyqtSignal(str)
	def __init__(self):
		QThread.__init__(self)
	def __del__(self):
		self.wait()
	def run(self):
		while True:
			time.sleep(5) # recheck in every 5 secs
			if thread_list:
				self.message = "Running.. {} task".format(len(thread_list))
			else:
				self.message = "Idle!!"
				 
			self.signalCheckStatus.emit(self.message)
			
class ThreadCheckUpdate(QThread):
	try:
		signalCheckUpdate = QtCore.Signal() 
	except:
		#Or pyqtSignal for PyQt4
		signalCheckUpdate = QtCore.pyqtSignal()
	def __init__(self,*args):
		super(ThreadCheckUpdate,self).__init__(*args)
		#QThread.__init__(self, *args)
		self.val = ""
	def run(self):
		while True:
			#print("..") # For DEBUG
			time.sleep(3)  # recheck in every 3 secs
			if not os.path.exists(log_path):
				try:
					#print("checking update") # For DEBUG only
					app_version_page = "https://raw.githubusercontent.com/mediabots/InstagramBot-GUI-Python/master/version-updates.txt"
					resp,excep = session_func(session_temp,app_version_page)
					if not excep:
						if resp and resp.status_code == 200:
							content = resp.text
							versions = content.strip().split("--------------------\n")
							latest_version = versions[-1]
							latest_version_number = latest_version.split("\n")[0].split("-")[1].strip().split(" ")[1]
							#print(latest_version_number)  # For DEBUG only
							if app_version != latest_version_number:
								self.val = "anything"
						else:
							#print("App version checker page not responding correctly")
							pass
					else:
						#print("No Network!")
						pass
				except:
					#print("No Network!!")
					pass
				if self.val:
					self.signalCheckUpdate.emit()
				break # exit from thread
# Thread Example	
'''class ThreadClass(QThread): # may require in future implementation
	# For Thread Only
	try:
		checkSignal = QtCore.Signal(str,float) 
	except:
		#Or pyqtSignal for PyQt4
		checkSignal = QtCore.pyqtSignal(str,float)
	def __init__(self,*args):
		super(ThreadClass,self).__init__(*args)
		#QThread.__init__(self, *args)
	def run(self):
		while True:
			self.val_float = psutil.cpu_percent(interval=5)
			self.val = "String"
			self.checkSignal.emit(self.val,self.val_float)
			#print(val_float)	'''
# End of Classes			

queue = Queue()
thread_list = list()

if __name__=='__main__':
	app = QApplication(sys.argv)
	dialog = InstagramBot()
	# setup splash/intro screen
	movie = QMovie(":/Splash/MediaBots_animate.gif")
	splash = MovieSplashScreen(movie)
	splash.show()
	
	non_gui_main_thread = MyThread('non gui main-thread') 
	non_gui_main_thread.setDaemon(True)
	non_gui_main_thread.start() # start a endless thread (main thread)
	
	start = time.time()
	while movie.state() == QMovie.Running and time.time() < start + 8:
		app.processEvents()
	#time.sleep(8)
	
	dialog.show()
	splash.finish(dialog)
	
	sys.exit(app.exec_())
