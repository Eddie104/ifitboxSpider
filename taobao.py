#!/usr/bin/env python
# -*- coding: utf-8 -*-
import helper
import re, os, json

if __name__ == '__main__':
	for page in xrange(2, 10):
		pq = helper.get('https://yopride.taobao.com/i/asynSearch.htm?_ksTS=1500985131600_277&callback=jsonp278&mid=w-14910079178-0&wid=14910079178&path=/category.htm&spm=a1z10.3-c-s.w4002-14910079178.98.39295bb0lvLjMM&search=y&qq-pf-to=pcqq.c2c&pageNo=%d' % page)
		# print(pq('.J_TGoldData'))
		print(pq.html())
		break




