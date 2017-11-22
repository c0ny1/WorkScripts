#coding=utf-8
import optparse
import os
		
def filter(shadowline,filterlist,rule):
    if rule == 'user': #过滤用户
        for user in filterlist:
            #print '%s-->%s' % (user,shadowline[0])
            if user == shadowline[0]:
                print 'True'
                return True
            else:
	            return False
	
    if rule == 'pwd': #过滤密码
        for s in shadowline[1]:
            if s in filterlist:
                return True
	    return False

    if rule == 'all': #过滤所有
         for fl in filterlist:
            if fl in shadowFile:
                return True
            else:
                return False

# 从shadow文件一行中获取多列数据进行拼凑
def get_colomns_for_list(shadowline,columns):
    hashline = []
    str = ':'
    for column in columns:
        hashline.append(shadowline[int(column)])

    return str.join(hashline)

## 从文件中获取hash
def gethash(file,columns,includeUserList,excludeUserList):
    fopen = open(file,"r")
    hashlist = []
    for line in fopen:
        l = line.split(':')

        try:
			# 包含用户
            if len(includeUserList)>1 and not filter(l,includeUserList,rule="user"):
                continue
			# 排除用户
            if len(includeUserList)>1 and filter(l,excludeUserList,rule="user"):
			    continue
			# 过滤空密码
            if not filter(l,filterlist=['*','!','','X','x'],rule='pwd'):
                hashline = get_colomns_for_list(l,columns)
                hashlist.append(hashline)
        except StandardError,e:
            print str(e)
            continue
			
    return hashlist

def read_for_files(filePath,columns,includeUserList,excludeUserList,outFile):
    pathDir = os.listdir(filePath)
    for allDir in pathDir:
    	child = os.path.join('%s%s' % (filePath, allDir))
        
        if os.path.isdir(child):
        	#print child.decode('gbk')+"is dir" # .decode('gbk')是解决中文显示乱码问题
        	pass

        if os.path.isfile(child):
            print '[file]'+allDir.decode('gbk')
            hashlist = gethash(child,columns,includeUserList,excludeUserList)
            write4file(outFile,hashlist)

## 校验shadow格式的函数
def check_shadow():
 	pass


## 将list写入txt
def write4file(outFile,hashlist):
    f = open(outFile,"a")#a模式可以追加写入
    for hash in hashlist:
        f.write(hash)
        f.write('\n')
        print '[+] ' + hash

    f.close()

def main():
    parser = optparse.OptionParser('python shadowFilter.py -d <target dir> -c <column> -o <directory>')
    parser.add_option('-F',dest='shadowFile',type="string",help="specify target file")
    parser.add_option('-d',dest='dir',type="string",help="specify target file")
    parser.add_option('-f',dest='filterUser',type="string",help="specify target file")
    parser.add_option('-m',dest='mode',type="string",help="specify target file")
    parser.add_option('-c',dest='columns',type="string",help="specify target file")
    parser.add_option('-o',dest='outFile',type="string",help="specify target file")
    parser.add_option('--iuser',dest='includeUser',type="string",help="specify target file")
    parser.add_option('--euser',dest='excludeUser',type="string",help="specify target file")
    (options,args) = parser.parse_args()
    dir = options.dir
    filterUser = options.filterUser
    outFile = options.outFile
    columns = str(options.columns).split(',')
    includeUserList = str(options.includeUser).split(',')
    excludeUserList = str(options.excludeUser).split(',')
    if dir == None or outFile == None:
        print parser.usage
        exit(0)

    if includeUserList == None:
        includeUserList = []
    if excludeUserList ==None:
        excludeUserList = []
	
    read_for_files(dir,columns,includeUserList,excludeUserList,outFile)	
    	
if __name__ == '__main__':
   main()
