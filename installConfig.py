#!/usr/bin/python

import os
home_dir = os.environ.get("HOME")
git_dir = os.getcwd()

def link_file(filename, target_filename = None, hide_file=False):
	if target_filename != None:
		target_filename = home_dir + "/" + target_filename
	else:
		dirname = os.path.dirname(filename)
		new_filename = "."+os.path.basename(filename)
		target_filename = home_dir + "/" + dirname + "/" + new_filename

	if os.path.lexists(target_filename):
		option = raw_input(target_filename + " already exists. Do you want to erase it? ([y]/n): ")
		if option == 'n' or option == 'N':
			print "Skipping..."
			return
		else:
			os.remove(target_filename)
	
	os.symlink(git_dir + "/" + filename,target_filename)


# Copy the configuration
link_file("gitignore")
link_file("gitconfig")
link_file("tmux.conf")

link_file("bash_extensions")
link_file("dircolors.ansi-dark")
link_file("git-completion.bash")
link_file("xmobarrc")
link_file("Xmodmap")
link_file("xsession")

link_file("dircolors")
