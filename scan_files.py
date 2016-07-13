#!/usr/bin/python

import os

root='./linux-4.4.10'

c_files = []
S_files = []
h_files = []

for dirpath, dirnames, filenames in os.walk(root):
	c = [os.path.splitext(item)[0] for item in filenames if os.path.splitext(item)[1]=='.c']
	h = [os.path.splitext(item)[0] for item in filenames if os.path.splitext(item)[1]=='.h']
	S = [os.path.splitext(item)[0] for item in filenames if os.path.splitext(item)[1]=='.S']
	
	c_files.extend(c)
	S_files.extend(S)
	h_files.extend(h)

print "num of c : %d" % len(c_files)
print "num of h : %d" % len(h_files)
print "num of S : %d" % len(S_files)

