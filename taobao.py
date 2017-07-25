#!/usr/bin/env python
# -*- coding: utf-8 -*-
import helper
import re, os, json

COOKIE = {
	'miid': '1012835004480615841',
	'UM_distinctid': '15bfefbdc301b9-081eba29c52bcb-4931126d-130980-15bfefbdc313cb',
	'l': 'AsXFNNtxpqlIzjYL5WooNboIVRv/M3kU',
	'hng': 'CN%7Czh-CN%7CCNY%7C156',
	'thw': 'cn',
	'v': '0',
	'_uab_collina': '150098956744172848501565',
	'swfstore': '112947',
	'_tb_token_': '3771e3e38be6e',
	'x': 'e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0',
	'uc1': 'cookie14=UoTcDzt1e6lSpQ%3D%3D&lng=zh_CN&cookie16=U%2BGCWk%2F74Mx5tgzv3dWpnhjPaQ%3D%3D&existShop=true&cookie21=VT5L2FSpdet1FS8C2gIFaQ%3D%3D&tag=10&cookie15=Vq8l%2BKCLz3%2F65A%3D%3D&pas=0',
	'uc3': 'sg2=AiLbR8MnOloN4DqaYZor%2FU%2FQRYN0VmktZzHVSKsrKp8%3D&nk2=q6SA3Iz%2Fguzwz4GT&id2=UoH8VPQiyyo66w%3D%3D&vt3=F8dBzWOacJBKXveImIw%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D',
	'existShop': 'MTUwMDk4OTQ4NQ%3D%3D',
	'uss': 'VFRzDaRpnr5rnHi9ZT%2BZP3SAatjqC9xrdLLwkwahAjTOeTVuS8JSKaLcyA%3D%3D',
	'lgc': '%5Cu4E09%5Cu8272%5Cu5807010101',
	'tracknick': '%5Cu4E09%5Cu8272%5Cu5807010101',
	'cookie2': '1c2e8d7892e544cd84e63fd7d3463f77',
	'sg': '170',
	'mt': 'np=&ci=20_1',
	'cookie1': 'UojXLgEisSdUZ37qn0%2F9aH7jXQ9W6jYnCSKL0AmVu50%3D',
	'unb': '1039688687',
	'skt': '813a6ac93aeee615',
	't': 'fd63f6c9a2f763cf17bd42c3a2707105',
	'_cc_': 'V32FPkk%2Fhw%3D%3D',
	'tg': '0',
	'_l_g_': 'Ug%3D%3D',
	'_nk_': '%5Cu4E09%5Cu8272%5Cu5807010101',
	'cookie17': 'UoH8VPQiyyo66w%3D%3D',
	'isg': 'AqioB2HkZTzWi0gVaqmInUu7aZZ6eRP6GTwTMWLZ9CMWvUgnCeHcaz69x2q3',
	'pnm_cku822': '197UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5Ockp3Sn5Lf0R4Q3xDdiA%3D%7CU2xMHDJ3DmMYcV9%2FUWhTfV1zL04oRCNdJwlfCQ%3D%3D%7CVGhXd1llXWBdaVxoU29Ua1RhVmtJck5zR31JdE51SX1AeEB%2BR2k%2F%7CVWldfS0QMAU7BCQYIgIsCCNlAl87UghDPFESORkmBjkXQRc%3D%7CVmhIGCUFOBgiGyQEOwA6GiYYIxY2Aj4BIR0jGC0NOAI9az0%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D',
	'cna': 'xIEREWv0hF0CAWriR2jEIPhM',
	'_umdata': 'E2AE90FA4E0E42DE07C65CA6476B1D7090873A58613CD5D4DB51B93F447C5D686961A3707E0D6438CD43AD3E795C914C404316D6839ED8FA398CE7C4C77E8FB0'
}

if __name__ == '__main__':
	csv = 'name,price,selledTotal\n'

	namePattern = re.compile('\s[\w\s\-/\*\.]*</a>\s+<div class=\\\\"attribute')
	pricePattern = re.compile('class=\\\\"c-price\\\\">\d+\.\d{2}\s*</span>')
	selledPattern = re.compile('class=\\\\"sale-num\\\\">\d+</span>')
	for page in range(1, 10):
		html = helper.get('https://yopride.taobao.com/i/asynSearch.htm?_ksTS=1500985131600_277&callback=jsonp278&mid=w-14910079178-0&wid=14910079178&path=/category.htm&spm=a1z10.3-c-s.w4002-14910079178.98.39295bb0lvLjMM&search=y&qq-pf-to=pcqq.c2c&pageNo=%d' % page, cookies = COOKIE, sleep = 5, returnType = 1)
		# # print(pq.html())
		nameArr = namePattern.findall(html)
		# # print(len(nameArr))
		# # print(nameArr)
		nameArr = [name.split('</a>')[0].strip() for name in nameArr]
		# print(nameArr)
		# break
		priceArr = pricePattern.findall(html)
		# 'class=\\"c-price\\">96.00</span>'
		priceArr = [p.split('>')[1].split('<')[0].strip() for p in priceArr]
		# print(priceArr)
		selledArr = selledPattern.findall(html)
		selledArr = [s.split('>')[1].split('<')[0] for s in selledArr]

		print(len(nameArr))
		for i in range(0, len(nameArr)):
			csv += '%s,%s,%s\n' % (nameArr[i], priceArr[i], selledArr[i])
			# print(csv)
	f = open('result.csv', 'wb')
	f.write(csv.encode('utf-8'))
	f.close()