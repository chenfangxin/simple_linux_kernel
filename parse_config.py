#!/usr/bin/python

import os
import re

def parse_config(path):
	configs = []
	dst_file = path + '.config'
	with open(dst_file) as f:
		for line in f:
			line=line.strip()
			if line:
				if not re.match('^#', line):
					item = line.split('=')[0]
					configs.append(item)
	return configs

if __name__=='__main__':
	configs = parse_config('./linux-4.4.10/')
#	print "CFG item num :" + str(len(configs))
	print configs
