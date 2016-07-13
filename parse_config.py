#!/usr/bin/python

import os
import re

dst_file = './linux-4.4.10/.config'
configs = []
with open(dst_file) as f:
	for line in f:
		line=line.strip()
		if line:
			if not re.match('^#', line):
				item = line.split('=')[0]
				configs.append(item)

print "CFG item num :" + str(len(configs))
print configs
