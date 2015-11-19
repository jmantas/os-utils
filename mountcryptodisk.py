#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

""" utility to mount crypted disk file in *nix"""

import click
from osutilslib.os_env import *
from osutilslib.block_device import *


@click.command()
@click.option('-d', "--disk", help='Disk name to mount.' )
@click.option('-m', "--mountpoint", help='Mountpoint')
def main(disk, mountpoint):
    """ main function, gets parameters file disk and mount point, checks if loop device exists
        if not - creates it, links. Then checks if /dev/mapper/*.crypt device exists, if not -
        creates it.
        After that - mounts disk to mountpoint """

    disk_to_mount = disk
    directory_to_mount = mountpoint 
    loop_device = str(get_loop_device())
    crypted_mapper_interface = str(get_mapper_interface())
    crypted_interface_to_mount = str(get_mapper_interface_full_path(crypted_mapper_interface))
   
    """Check if it is PGP crypted and if true - decrypt it"""
    if disk_to_mount.endswith('.gpg'):
        pgp_decrypt(disk_to_mount, disk_to_mount.strip('.gpg'))
        disk_to_mount = disk_to_mount.strip('.gpg')

    """Create and link loop device if it does not exists""" 
    if not file_checker(loop_device):
        create_loop_device(loop_device)
        link_loop_device(loop_device, disk_to_mount)
    
    """Creates crypted mapper interface to loop device """
    if not file_checker(crypted_interface_to_mount):
        create_crypted_interface(crypted_mapper_interface, loop_device)

    """Mounts crypted mapper interface to mountpoint aka actual mount"""
    if file_checker(disk_to_mount) and file_checker(crypted_interface_to_mount):
        mount_crypted_disk(crypted_interface_to_mount, directory_to_mount)

    
if __name__ == "__main__":
    main()
