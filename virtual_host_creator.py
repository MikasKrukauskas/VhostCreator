#! /usr/bin/python
import getopt
from sys import argv
from os.path import exists
from os import makedirs, system

etc = '/mnt/storage/config/'
www = '/mnt/storage/'

#etc='/home/mikas/Desktop/'
#www='/home/mikas/Desktop/'
def show_usage():
	print("""
	Create a new vHost 
	    -s    SiteName - i.e. example.com or sub.example.com
	""")
	exit(1)

def create_vhost(suffix, site):
    out = """
    #
    #%s%s
    #
    <VirtualHost *:80>
    ServerAdmin mikas.krukauskas@squalio.com
    ServerName %s%s
    ServerAlias %s
    DirectoryIndex index.html index.htm index.php
    DocumentRoot /mnt/storage/%s%s/
    ErrorLog /mnt/storage/logs/%s%s-error.log
    CustomLog /mnt/storage/logs/%s%s-access.log combined
    </VirtualHost>"""%(suffix,site,suffix,site,site,suffix,site,suffix,site,suffix,site)
    return out

def edit_vhost_conf(site):
    makedirs(www+site,0o755)
    makedirs(www+site+'_moodledata',0o755)
    vhost= open(etc+'virtual_hosts.conf', 'a')
    host_to_write = create_vhost('www.',site)
    vhost.write(host_to_write)
    vhost.close()
    restart_httpd()

def restart_httpd():
    system('systemctl restart httpd')

site=None
try:
	opts, args = getopt.getopt(argv[1:], "hd:s:", ['site='])
except getopt.GetoptError as err:
	print(str(err))

if opts.__len__() == 0:
	show_usage()

for option, value in opts:
	if option in ('-s', '--site'):
		site = edit_vhost_conf(value)
	else:
		print ("Unknown parameter used")
		show_usage()
