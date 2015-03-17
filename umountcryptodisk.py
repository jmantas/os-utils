#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

""" utility to unmount crypted disk file in *nix"""

import argparse
import os_env
import block_device

def main():
    """ main function, gets parameters for unmount, and unmounts mountpoint defined by -m """
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mountpoint", metavar='<mount point>', dest="mount_point",
        help="mount point to unmount", type=str)
    args = parser.parse_args()
    
    mount_point_to_unmount = args.mount_point 
    loop_device = str(os_env.get_loop_device())
    crypted_mapper_interface = str(os_env.get_mapper_interface())
    crypted_interface_to_unmount = str(os_env.get_mapper_interface_full_path(crypted_mapper_interface))
    
    if block_device.check_mount_status(mount_point_to_unmount):
        block_device.unmount_mount_point(mount_point_to_unmount)
    
    block_device.remove_crypted_interface(crypted_mapper_interface)
    block_device.remove_loop_device(loop_device)

    
if __name__ == "__main__":
    main()
