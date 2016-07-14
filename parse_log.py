#!/usr/bin/python

# find ./linux-4.4.10 -name *.[ch]|xargs grep "#include"  > log 

import re

log_file='./log'
inc_c = set()
with open(log_file) as f:
	for line in f:
		line0 = line.split(':')[0]
		line1 = line.split(':')[1]
		line1 = line1.strip()
		s = re.search('\.c', line1)
		if s:
			inc_c.add(line1)

for i in inc_c:
	print i
#	print i.split(' ')[1]
