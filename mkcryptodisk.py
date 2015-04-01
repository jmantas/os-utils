#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

""" utility to make crypted disk files on *nix"""

import argparse
import os_env
import block_device

def main():
    """ main function, gets parameters for creating crypted disk.
        by default creates disk named <username>.dat.disk size 64MB 
        with ext3 file system """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--disk", metavar='[disk name]', dest="disk_name",
        help="disk name, defaults to username", type=str, default=str(os_env.get_disk_name()))
    parser.add_argument("-s", "--size", metavar='[disk size]', dest="disk_size",
        help="disk size in MB, defaults to 64MB", type=str, default="64")
    parser.add_argument("-f", "--fstype", metavar='[file system type]', dest="fs_type",
        help="file system type ( ext3, ext4, vfat, ... ), defaults to ext3", type=str, default="ext3")
    parser.add_argument("-c", "--pgpencrypt", help="If set, also encrypt disk file with PGP", action="store_true")
    args = parser.parse_args()

    loop_device = str(os_env.get_loop_device())
    mapper_interface = args.disk_name + ".crypt" 
    mapper_interface_path = str(os_env.get_mapper_interface_full_path(mapper_interface))
    file_system_type = args.fs_type
    disk_size = args.disk_size

    file_disk_name = "%s/%s" % (os_env.get_user_homedir(), args.disk_name)

    """If disk file does not exist, create it"""
    if not os_env.file_checker(file_disk_name):
        block_device.create_disk_file(file_disk_name, disk_size)
    else:
        print "Exiting..."
        exit(1)

    """If loop device does not exists, create it"""
    if not os_env.file_checker(loop_device):
        block_device.create_loop_device(loop_device)
        block_device.link_loop_device(loop_device, file_disk_name)
   
    """If mapper interface does not exists, create it"""
    if not os_env.file_checker(mapper_interface_path):
        block_device.create_crypted_interface(mapper_interface, loop_device)

    """Creates file system on crypted mapper interface"""
    block_device.create_fs(file_system_type, mapper_interface_path)
   
    """Checks if -c option is set, for additional PGP encryptio. If true - PGP crypts it""" 
    if args.pgpencrypt:
        block_device.pgp_encrypt(file_disk_name)
        block_device.file_cleaner(file_disk_name)

    """Cleans not needed block devices"""
    block_device.remove_crypted_interface(mapper_interface)
    block_device.remove_loop_device(loop_device)

if __name__ == "__main__":
    main()
