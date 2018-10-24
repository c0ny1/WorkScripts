#coding=utf-8
import os
import argparse
import json
import urllib2
import shutil

'''
author: c0ny1
github: https://github.com/c0ny1/WorkScripts/tree/master/get-subdomain-from-baidu
date: 2018-10-25 0:38
description: https://github.com/odboy/shadowProxy项目从https://github.com/fate0/proxylist项目更新代理ip列表辅助脚本
'''

def downloadProxyList(download_save_file):
	'''
	从https://github.com/fate0/proxylist项目下载proxy.list文件
	'''
	url = 'https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list'
	print('[+] Start downloading proxy.list...')
	try:
		req = urllib2.Request(url)
		res = urllib2.urlopen(req)
		res = res.read()
		f = open(download_save_file,'w')
		f.write(res)
		print('[+] Download %s file successfully!' % download_save_file)
	except:
		print('[!] Please go to the following address manually to download proxy.list, and use -f proxy.list to update the proxy IP list.')
		print('[!] Link: https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list')
		exit()

def updateProxyURL(download_save_file,proxy_list_tmp_file):
	'''
	从下载的proxy.list文件中提取代理ip
	'''
	f = open(download_save_file)
	w = open(proxy_list_tmp_file,'w')
	print('[+] Get the proxy IP from the %s file...' % download_save_file)
	for l in f.readlines():
		proxy_josn_str = l.strip()
		proxy = json.loads(proxy_josn_str)
		proxy_type = proxy.get('type')
		proxy_ip = proxy.get('host')
		proxy_port = proxy.get('port')
		proxy_url = '%s://%s:%s' % (proxy_type,proxy_ip,proxy_port)
		if proxy_type == 'http':
			target = 'http://' + proxy_ip + ':' + str(proxy_port)
		elif proxy_type == 'https':
			target == 'https://' + proxy_ip + ':' + str(proxy_port)
		else:
			continue
		# print '[+]' + target
		w.write(target)
		w.write('\n')
	print('[+] Write the obtained IP to the %s file' % proxy_list_tmp_file)
	f.close()
	w.close()

def uniqifer(readFile,writeFile):
	'''
	IP代理列表去重
	'''
	a=0
	lines_seen = set()
	outfile = open(writeFile, "w")
	f = open(readFile, "r")
	print('[+] Begin to remove duplication.')
	for line in f:
		if line not in lines_seen:
			a+=1
			outfile.write(line)
			lines_seen.add(line)
	outfile.close()
	print('[+] Remove repeat success')
	
if __name__ == '__main__':
	download_save_file = 'proxy.list'
	proxy_list_tmp_file = 'proxylist.tmp'
	proxy_list_file = 'proxylist.txt'
	
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", "--file", dest = "file",metavar="FILE",help="Proxy list file path")
	args = parser.parse_args()
	if args.file:
		updateProxyURL(args.file,proxy_list_tmp_file)
	else:
		downloadProxyList(download_save_file)
		updateProxyURL(download_save_file,proxy_list_tmp_file)
	uniqifer(proxy_list_tmp_file,proxy_list_file)
	os.remove(proxy_list_tmp_file)