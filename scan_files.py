#!/usr/bin/python


import os
import re

root='./linux-4.4.10'

used_files = set()
depends_files = set()

def get_source_file(path):
	for dirpath, dirnames, filenames in os.walk(path):
		for item in dirnames:
			d = os.path.join(dirpath, item)
			if os.path.islink(d):
				os.remove(d)

		for item in filenames:
			d = os.path.join(dirpath, item)
			if os.path.islink(d):
				os.remove(d)
				continue

			if os.path.splitext(item)[1]=='.o':
				n = os.path.splitext(item)[0]
				c = n + '.c'
				s = n + '.s'
				S = n + '.S'

				full = ''	
				if c in filenames:
					full = os.path.join(dirpath, c)
				
				if s in filenames:
					full = os.path.join(dirpath, s)

				if S in filenames:
					full = os.path.join(dirpath, S)

				if full:
					used_files.add(full)	
	
def get_parent_dir(path, level):
	while level:
		path = os.path.split(path)[0]
		level = level - 1
	return path

def get_depends_files(path):
	for i in used_files:
		with open(i) as f:
			line = f.readline()
			line = line.strip()
			s = re.search('^#include', line)
			if s:
				b = line.split(' ')[1]
				if b[0]=='<':
					b = b[1:-1]
					filename =  os.path.join(path, 'include', b)
					depends_files.add(filename)	
				else:
					b = b[1:-1]
					a = b.split('/')
					up_level = a.count('..')
					dirpath = os.path.dirname(i)
					parent = get_parent_dir(dirpath, up_level)

					while up_level:
						del a[0]
						up_level = up_level - 1

					filename = os.path.join(parent, '/'.join(a))
					depends_files.add(filename)	

		depends_files.add(i)

def write_depends_files():
	with open('./depends_files', 'w') as f:
		for i in depends_files:
			f.write(i+'\n')

def del_unused_files(path):
	for dirpath, dirnames, filenames in os.walk(path):
		for item in filenames:
			d = os.path.join(dirpath, item)
			if d not in depends_files:
				os.remove(d)

def remove_empty_dir(path):
	deled_dir = set()
	for dirpath, dirnames, filenames in os.walk(path):
		if not filenames:
			if not dirnames:
				deled_dir.add(dirpath)
				os.rmdir(dirpath)
	return deled_dir	

if __name__ == '__main__':
	get_source_file(root)
	get_depends_files(root)

	del_unused_files(root)
	a = remove_empty_dir(root)
	while a:
		a = remove_empty_dir(root)

