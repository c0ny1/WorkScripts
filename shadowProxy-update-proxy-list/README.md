# 借助proxylist项目给shadowProxy项目更新代理ip列表的脚本
## 说明

前段时间也想写一个小巧不带爬虫的代理池，来解决ip被ban问题。无意发现已经有大佬写好，项目名为[shadowProxy](https://github.com/odboy/shadowProxy)，结合项目[proxylist](https://github.com/fate0/proxylist)的代理资源正好美滋滋。 **由于[proxylist](https://github.com/fate0/proxylist)项目的代理ip列表为json格式，shadownProxy可以导入的代理ip列表每行格式为`scheme://host:port`，故需要改脚本来转换。**

## 使用方法

##### 情况一：全自动更新代理ip

自动下载proxy.list项目实时更新的代理ip列表,并自动提取去重，最终生成shadowProxy可以使用的代理ip列表proxylist.txt

```
$ python shandowPorxyUpdateProxyList.py
[+] Start downloading proxy.list...
[+] Download proxy.list file successfully!
[+] Get the proxy IP from the proxy.list file...
[+] Write the obtained IP to the proxylist.tmp file
[+] Begin to remove duplication.
[+] Remove repeat success
```

##### 情况二：半自动更新代理ip

有时访问github很慢，或者无法访问。可以自行去项目上下载proxy.list,然后用脚本去提取并去重出符合shadowProxy的代理地址。

```
$ python shandowPorxyUpdateProxyList.py
[+] Get the proxy IP from the proxy.list file...
[+] Write the obtained IP to the proxylist.tmp file
[+] Begin to remove duplication.
[+] Remove repeat success
```