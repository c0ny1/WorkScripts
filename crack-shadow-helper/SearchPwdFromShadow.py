#coding=utf-8

import os
import re
import optparse

SHADOW = 0
NUM = 0
ERR = []

# 检查shadow每行的格式是否正确
def shadowcheck(hashlist):
	n = hashlist.count(':')
	if n != 8:
		return False
	else:
		return True

# 获取文件名
def getFileName(fileName):
	return os.path.basename(fileName)

# 在shadow文件中搜索密码
def searchPwd(shadowFile,pwdFile):
	global NUM
	global ERR
	sopen = open(shadowFile,"r")
	
	textlist = []
	
	for shadowline in sopen:
		shadowline = shadowline.strip('\n').strip('\r')
		if not shadowcheck(shadowline):
			print '[-] this is not shadow file :' + shadowline 
			ERR.append(getFileName(shadowFile))
			return 
		
		username = shadowline.split(':')[0]
		popen = open(pwdFile,"r")
		for hashlist in popen:
			hash = hashlist.split(':')[0]
			if hash in shadowline:
				shadowfilename = getFileName(shadowFile)
				text = "%s:%s:%s" % (shadowfilename,username,hashlist)
				textlist.append(text.strip('\n').strip('\r'))
				NUM += 1
		popen.close()
	
	sopen.close()
	return textlist
		
	
def search(shadowDir,pwdFile,outFile):
	global SHADOW
	pathDir = os.listdir(shadowDir)
	for allDir in pathDir:
		child = os.path.join('%s%s' % (shadowDir,allDir))
		
		if os.path.isfile(child):
			SHADOW += 1
			print '[file]' + allDir.decode('gbk')
			textlist = searchPwd(child,pwdFile)
			write4file(textlist,outFile)
	

def write4file(textList,outFile):
	if textList == None:
		return 
	f = open(outFile,'a')
	for text in textList:
		f.write(text)
		f.write('\n')
		print '[+]' + text
	f.close()
	
	
def main():
	parser = optparse.OptionParser('python SearchPwdFromShadow.py -d <shadow dir> -p <pwd file> -o <out file>')
	parser.add_option('-d',dest='shadowDir',type="string",help="specify shadow file")
	parser.add_option('-p',dest='pwdFile',type="string",help="specify pwd file")
	parser.add_option('-o',dest='outFile',type="string",help="specify out file")

	(options,args) = parser.parse_args()
	shadowDir = options.shadowDir
	pwdFile = options.pwdFile
	outFile = options.outFile

	if shadowDir == None or pwdFile == None:
		print parser.usage
		exit(0)
		
	if outFile == None:
		outFile = 'out.txt'

	search(shadowDir,pwdFile,outFile)
	
	print '----------------------------finish------------------------'
	print 'Number of shadows: %d' % SHADOW
	print 'Password found: %d' % NUM
	print 'Bad format: %s' % str(ERR)
	

if __name__ == '__main__':
    main()
