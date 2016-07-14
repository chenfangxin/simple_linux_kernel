#!/usr/bin/python

import os

root='./linux-4.4.10'

c_files = []
S_files = []
h_files = []
o_files = []

# the used_files item format
# {
#	 "obj_file":"./xxx/yyy/zzz.o",
#	 "depend_files":{"./xxx/yyy/zzz.c","./xxx/yyy/zzz.h"}
# }


used_files = {}

def scan_all_file(path):
	for dirpath, dirnames, filenames in os.walk(path):
		c = [os.path.splitext(item)[0] for item in filenames if os.path.splitext(item)[1]=='.c']
		h = [os.path.splitext(item)[0] for item in filenames if os.path.splitext(item)[1]=='.h']
		S = [os.path.splitext(item)[0] for item in filenames if os.path.splitext(item)[1]=='.S']
	
		c_files.extend(c)
		S_files.extend(S)
		h_files.extend(h)

def scan_o_file(path):
	for dirpath, dirnames, filenames in os.walk(path):
#		o = [os.path.splitext(item)[0] for item in filenames if os.path.splitext(item)[1]=='.o']
		o = [item for item in filenames if os.path.splitext(item)[1]=='.o']
		o_files.extend(o)	
	
if __name__ == '__main__':
	scan_o_file(root)
	print "num of o : %d" % len(o_files)
	print o_files

