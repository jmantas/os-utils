#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

""" utility to mount crypted disk file in *nix"""

import argparse   
import os_env
import block_device


def main():
    """ main function, gets parameters file disk and mount point, checks if loop device exists
        if not - creates it, links. Then checks if /dev/mapper/*.crypt device exists, if not -
        creates it.
        After that - mounts disk to mountpoint """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--disk", metavar='<disk name>', dest="disk_name", help="disk name", type=str)
    parser.add_argument("-m", "--mountpoint", metavar='<mount point>', dest="mount_point", type=str)
    args = parser.parse_args()

    disk_to_mount = args.disk_name 
    directory_to_mount = args.mount_point 
    loop_device = str(os_env.get_loop_device())
    crypted_mapper_interface = str(os_env.get_mapper_interface())
    crypted_interface_to_mount = str(os_env.get_mapper_interface_full_path(crypted_mapper_interface))
   
    """Check if it is PGP crypted and if true - decrypt it"""
    if disk_to_mount.endswith('.gpg'):
        block_device.pgp_decrypt(disk_to_mount, disk_to_mount.strip('.gpg'))
        disk_to_mount = disk_to_mount.strip('.gpg')

    """Create and link loop device if it does not exists""" 
    if not os_env.file_checker(loop_device):
        block_device.create_loop_device(loop_device)
        block_device.link_loop_device(loop_device, disk_to_mount)
    
    """Creates crypted mapper interface to loop device """
    if not os_env.file_checker(crypted_interface_to_mount):
        block_device.create_crypted_interface(crypted_mapper_interface, loop_device)

    """Mounts crypted mapper interface to mountpoint aka actual mount"""
    if os_env.file_checker(disk_to_mount) and os_env.file_checker(crypted_interface_to_mount):
        block_device.mount_crypted_disk(crypted_interface_to_mount, directory_to_mount)

    
if __name__ == "__main__":
    main()
