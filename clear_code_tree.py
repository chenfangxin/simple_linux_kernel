#!/usr/bin/python


import os
import sys
import re

root='./linux-4.4.10'

used_files = set()

def get_parent_dir(path, level):
	while level:
		path = os.path.split(path)[0]
		level = level - 1
	return path

def get_depends_files(item):
	depends_fils=set()
	with open(item) as f:
		for line in f.readlines():
			line = line.strip()
			s = re.search('^#include', line)
			if s:
				l = line.split(' ')  # split by whitespace
				if len(l)<=1:
					l = line.split('	') # some statement split by tab

				b = l[1]
				b = b.strip()
				if b[0]=='<':
					b = b[1:-1]
					filename =  os.path.join(root, 'include', b)
					if os.path.isfile(filename):
						depends_fils.add(filename)
					else:
						filename =  os.path.join(root, 'arch/x86/include', b)
						if os.path.isfile(filename):
							depends_fils.add(filename)
				else:
					b = b[1:-1]
					a = b.split('/')
					up_level = a.count('..')
					dirpath = os.path.dirname(item)
					parent = get_parent_dir(dirpath, up_level)

					while up_level:
						del a[0]
						up_level = up_level - 1

					filename = os.path.join(parent, '/'.join(a))
					if os.path.isfile(filename):
						depends_fils.add(filename)

					filename = os.path.join(parent, 'include', '/'.join(a))
					if os.path.isfile(filename):
						depends_fils.add(filename)
	return depends_fils

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
					a = get_depends_files(full)
					used_files.update(a)


def expand_depends_files():
	expand_files=set()
	for item in used_files:
		a = get_depends_files(item)	
		expand_files.update(a)
	used_files.update(expand_files)
		
def get_makefile():
	scripts = set()
	check_file = ['Makefile', 'Kconfig', 'Kbuild']
	global used_files
	for filename in used_files:
		dirpath = os.path.dirname(filename)
		l = os.listdir(dirpath)
		for i in check_file:
			if i in l:
				fullname = os.path.join(dirpath, i)
				scripts.add(fullname)
	used_files.update(scripts)
	
	
def write_depends_files():
	with open('./used_files', 'w') as f:
		for i in used_files:
			f.write(i+'\n')

def remove_unused_files(path):
	for dirpath, dirnames, filenames in os.walk(path):
		for item in filenames:
			d = os.path.join(dirpath, item)
			if d not in used_files:
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

	if len(used_files)==0:
		print "There're no object files"
		sys.exit(0)

	while 1:
		l1 = len(used_files)
		expand_depends_files()
		l2 = len(used_files)
		if l1==l2:
			break

	get_makefile()

	remove_unused_files(root)
	a = remove_empty_dir(root)
	while a:
		a = remove_empty_dir(root)

