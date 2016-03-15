#!/usr/bin/python

import os
import shutil
import sys

home_dir = os.environ.get("HOME")
git_dir = os.getcwd()

def link_file(filename, copy_file=False, target_filename = None):
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
    
    if copy_file:
        shutil.copyfile(git_dir + "/" + filename,target_filename)
    else:
        os.symlink(git_dir + "/" + filename,target_filename)


# Initialize submodules
os.system("git submodule update --init --recursive")

# Copy file or create links
if len(sys.argv) > 1:
    copy_file=True
else:
    copy_file=False

# Copy the configuration
link_file("gitignore",copy_file)
link_file("gitconfig",copy_file)
link_file("tmux.conf",copy_file)

link_file("bash_extensions",copy_file)
link_file("dircolors.ansi-dark",copy_file)
link_file("git-completion.bash",copy_file)
link_file("xmobarrc",copy_file)
link_file("Xmodmap",copy_file)
link_file("xsession",copy_file)

link_file("dircolors",copy_file)

link_file("minttyrc.dark",copy_file,".minttyrc")

link_file("vim")
link_file("emacs.d")

# Change colors in gnome-terminal
import platform
dist=platform.dist()[0].lower()
profile='Default'
if dist == 'fedora':
    profile='Unnamed'

os.system("./gnome-terminal-colors-solarized/install.sh -s dark -p {0}".format(profile))

# Execute the remapping of the keyboard
os.system("echo xmodmap ~/.Xmodmap >> ~/.bashrc")
os.system("echo source ~/.bash_extensions >> ~/.bashrc")

option = raw_input("Is this a Cygwin environment? ([y]/n): ")
if option == 'y' or option == 'Y':
    cmd = "cat " + git_dir + "/sol.dark >> " + home_dir + "/.bash.local"
    print cmd
    os.system(cmd)



print """
Now you have to setup solarized in your Gnome terminal.Do:

    git clone https://github.com/sigurdga/gnome-terminal-colors-solarized.git
    cd gnome-terminal-colors-solarized
    ./set_dark.sh
    """
