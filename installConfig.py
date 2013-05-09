#!/usr/bin/python

import os
home_dir = os.environ.get("HOME")
git_dir = os.getcwd()

def link_file(filename, hide_file=False):
	target_filename = home_dir + "/" + filename
	if hide_file:
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
link_file("gitignore",True)
link_file("gitconfig",True)
link_file("tmux.conf",True)

link_file("bash_extensions",True)
link_file("dircolors.ansi-dark",True)
link_file("git-completion.bash",True)
link_file("xmobarrc",True)
link_file("Xmodmap",True)
link_file("xsession",True)
