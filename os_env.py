# -*- mode: python; coding: utf-8 -*-
#

"""
module for setting and getting various environmental OS parameters
and functionality
"""

import os
import getpass
import time

def get_current_time():
    """gets current time in specific format"""
    return time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())


def get_user_homedir():
    """ wrapper to get users home directory """
    return os.path.expanduser("~")


def get_user_id():
    """ wrapper to get user ID """
    return os.getuid()


def get_user_group_id():
    """ wrapper to get user group ID """
    return os.getgid()


def get_disk_name():
    """ molds disk nicely looking disk name """
    return "%s.dat.disk" % getpass.getuser()


def get_mapper_interface():
    """ molds nicely looking mapper interface name """
    return "%s.crypt" % getpass.getuser()


def get_mapper_interface_full_path(mapper_interface):
    """ molds full path of mapper interface """
    return "/dev/mapper/%s" % mapper_interface


def get_disk_file_name():
    """ molds default path and name for disk located in users homedirectory """
    return "%s/%s" % (get_user_homedir(), get_disk_name())


def get_loop_device():
    """ molds distinctly looking loop device name """
    return "/dev/%s%s" % ("loop", os.getuid())


def file_checker(file_name):
    """ checks if file ( disk filename, loop device, crypted interface symlink, etc ) exits """
    if os.path.islink(file_name):
        print "Crypto device Symlink %s exists" % file_name
        return True
    else:       
        try:
            with open(file_name):
                print "File %s exists" % file_name
                return True
        except IOError:
            print "File %s does not exists" % file_name
            return False


def print_success():
    """ just prints success and returns true """
    print "Success!\n"
    return True


def prnt_error():
    """ just prints error and returns false """
    print "Error!\n"
    return False

