#coding=utf-8
import sys
import json
import urllib2

'''
author: c0ny1
github: https://github.com/c0ny1/WorkScripts/tree/master/get-subdomain-from-baidu
date: 2018-10-16 23:00
description: 基于百度云观测接口获取子域名
'''

def get_domain_json_from_baidu(domain):
	url = 'http://ce.baidu.com/index/getRelatedSites?site_address=%s' % domain
	req = urllib2.Request(url)
	res = urllib2.urlopen(req)
	res = res.read()
	return res

def dump_domain_to_text(domain_json,filename):
	f = open(filename,'w')
	obj_json = json.loads(domain_json)
	domain_list = obj_json.get("data")
	print '[+] Number of subdomains: %d' % len(domain_list)
	for d in domain_list:
		f.write(d.get('domain'))
		f.write('\n')
	f.close()
	print '[+] Successfully exported to %s' % filename

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print 'Usag: python getSubdomainFromBaidu.py xxx.com'
		exit()
	
	target_domain = sys.argv[1]
	domain_json = get_domain_json_from_baidu(target_domain)
	dump_domain_to_text(domain_json,'subdoamin.txt')
