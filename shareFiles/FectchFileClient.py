#coding=utf-8
from xmlrpclib import ServerProxy, Fault
from cmd import Cmd
from random import choice
from string import lowercase
from FectchFileServer import Node,UNHANDLED  #引入前面的server
from threading import Thread
from time import sleep

import sys

HEAD_START = 0.1
SECRET_LENGTH = 100

def randomString(length):
    chars = []
    letters = lowercase[:26]
    while length > 0:
        length -= 1
        chars.append(choice(letters))
    return ''.join(chars)

class Client(Cmd):
    prompt = '> '

    def __init__(self, url, dirname, urlfile):

        Cmd.__init__(self)
        self.secret = randomString(SECRET_LENGTH)
        n = Node(url, dirname, self.secret)
        t = Thread(target = n._start)
        t.setDaemon(1)
        t.start()

        sleep(HEAD_START)
        self.server = ServerProxy(url)
	self.dirname=dirname
	self.urlfile=urlfile
	print "=============================",dirname+"/"+urlfile
        for line in open(dirname+"/"+urlfile):
            line = line.strip()
            self.server.hello(line)

    def do_fetch(self, arg):
        try:
		self.server.resetKnow
		for line in open(self.dirname+"/"+self.urlfile):
            		line = line.strip()
            		self.server.hello(line)

            	self.server.fetch(arg,self.secret)
        except Fault,f:
            if f.faultCode != UNHANDLED: raise
            print "Couldn't find the file",arg

    def do_exit(self,arg):
        print
        sys.exit()

    do_EOR = do_exit

def main():
    urlfile, directory, url = sys.argv[1:]
    client = Client(url, directory, urlfile)
    client.cmdloop()

if __name__ == '__main__':main()

