#!/usr/bin/python

import os
import re

root='./linux-4.4.10'

used_files = set()
depends_files = set()

def get_source_file(path):
	for dirpath, dirnames, filenames in os.walk(path):
		for item in filenames:
			if os.path.splitext(item)[1]=='.o':
				n = os.path.splitext(item)[0]
				o = n + '.o'
				c = n + '.c'
				s = n + '.s'
				S = n + '.S'

				full = ''	
				if c in filenames:
					full = dirpath + '/' + c
				
				if s in filenames:
					full = dirpath + '/' + s

				if S in filenames:
					full = dirpath + '/' + S

				if full:
					used_files.add(full)	
	
def get_depends_files():
	for i in used_files:
		with open(i) as f:
			line = f.readline()
			line = line.strip()
			s = re.search('^#include', line)
			if s:
				print line
#				print line.split(' ')[1]
#				depends_files.add(line.split(' ')[1])

if __name__ == '__main__':
	get_source_file(root)
	print "num of used files : %d" % len(used_files)
	get_depends_files()
	print "num of depends files : %d" % len(depends_files)
	
