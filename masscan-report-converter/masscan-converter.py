#coding=utf-8
import os
import sys
import time
import argparse
import xml.dom.minidom
import xlsxwriter
from xlsxwriter import Workbook

'''
author: c0ny1
date: 2018-09-28 18:23
'''

def convert_masscan_report(xml_path,xls_path):
	workbook = xlsxwriter.Workbook(xls_path)
	worksheet = workbook.add_worksheet('Scan info')
	worksheet.autofilter("A1:H1")  #设置过滤
	worksheet.freeze_panes(1, 0)  #冻结窗格
	
	worksheet.lastrow = 0
	summary_header = ["addr", "port", "state", "protocol", "addrtype", "reason", "reason_ttl", "scan_endtime"]
	for idx, item in enumerate(summary_header):
		worksheet.write(0, idx, item,workbook.add_format({"bold": True}))
	worksheet.lastrow += 1
	
	DOMTree = xml.dom.minidom.parse(xml_path) 
	data = DOMTree.documentElement
	nodelist = data.getElementsByTagName('host')
	host_info = {}
	for node in nodelist:
		scan_endtime = node.getAttribute('endtime')
		scan_endtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(scan_endtime)))
		address_node = node.getElementsByTagName('address')
		addrtype = address_node[0].getAttribute('addrtype')
		addr = address_node[0].getAttribute('addr')
		port_node = node.getElementsByTagName('port')
		for port in port_node:
			protocol = port.getAttribute('protocol')
			portid = port.getAttribute('portid')
			state_element = port.getElementsByTagName('state')
			state = state_element[0].getAttribute('state')
			reason = state_element[0].getAttribute('reason')
			reason_ttl = state_element[0].getAttribute('reason_ttl')
			print '[+] | %s | %s | %s | %s | %s | %s | %s | %s |' % (addr,portid,state,protocol,addrtype,reason,reason_ttl,scan_endtime)
			scan_info = [addr,portid,state,protocol,addrtype,reason,reason_ttl,scan_endtime]
			for i in range(0,len(scan_info)):
				worksheet.write(worksheet.lastrow, i, scan_info[i])
			worksheet.lastrow += 1	
	workbook.close()

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input", metavar="XML", help="path to xml input")
	parser.add_argument("-o", "--output", metavar="XLS", help="path to xlsx output")
	
	if len(sys.argv) == 1:
		sys.argv.append('-h')
		
	args = parser.parse_args()
	
	if args.input:
		xml_path = args.input
	else :
		exit('[*] please use -i set xml path!')
	
	if os.path.lexists(xml_path) == False:
		exit('[*] %s does not exist!',xml_path)
		
	if args.output:
		xls_path = args.output
	else:
		xls_path = './masscan_report.xls'
		
	convert_masscan_report(xml_path,xls_path)
	
	