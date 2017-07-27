#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, requests, time, platform
from pyquery import PyQuery

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}

def now(): 
	return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

def today(): 
	return time.strftime('%Y-%m-%d', time.localtime(time.time()))

def timeStr():
	return time.strftime('%H:%M:%S', time.localtime(time.time()))

def mkDir(path):
	if not os.path.exists(path):
		os.makedirs(path)
	return path	

def writeFile(content, path):
	try:
		f = open(path, 'w')
		f.write(content)
		f.close()
		return True
	except Exception as e:
		print(e)
		return False

def readFile(path):
	try:
		f = open(path, 'r')
		r = f.read()
		f.close()
		return r
	except Exception as e:
		print(e)
		return None

# 开始下载图片
def downloadImg(url, imgPath):
	if url != None:
		if os.path.exists(imgPath):
			print('%s is exists, jump it!' % imgPath)
		else:
			print('download image: %s' % url)
			try:
				r = requests.get(url, stream = True)
			except Exception as e:
				print(e)
				return
			with open(imgPath, 'wb') as f:
				for chunk in r.iter_content(chunk_size = 1024): 
					if chunk:
						f.write(chunk)
						f.flush()

def get(url, cookies = {}, myHeaders = None, sleep = 0, returnType = 0):
	if sleep > 0:
		time.sleep(sleep)
	print('[%s] get url => %s' % (now(), url))
	global headers
	response = requests.get(url, headers = myHeaders or headers, cookies = cookies)
	if response.status_code == 200:
		return PyQuery(response.text) if returnType == 0 else response.text
	else:
		return None

def post(url):
	print('post url => ' + url)
	global headers
	response = requests.post(url, headers = headers, cookies = {}, data = {'imgContinue': 'Continue to image ... '})
	if response.status_code == 200:
		return PyQuery(response.text)
	else:
		return None

def optimizeImg(imgFile):
	system = platform.system()
	file = os.path.join(os.path.abspath("."), "pingo.exe")
	if (system == "Windows" and os.path.isfile(file)):
		os.system("{} -s5 {}".format(file, imgFile))
