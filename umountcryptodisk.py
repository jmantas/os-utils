#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

""" utility to unmount crypted disk file in *nix"""

import click
from osutilslib.os_env import *
from osutilslib.block_device import *

@click.command()
@click.option('-n', '--name', default="crypteddisk",
                help='Disk name. Default = crypteddisk' )
@click.option('-m', "--mountpoint", help='Mountpoint')
@click.option('-p', "--pgp/--no-pgp", default=False,
                help='If set, also encrypt disk file with PGP')
def main(mountpoint, pgp, name):
    """ main function, gets parameters for unmount, and unmounts mountpoint defined by -m 
        and cleans up mapper interface and loop devices """
    
    mount_point_to_unmount = mountpoint
    file_disk_name = "%s/%s" % (get_user_homedir(), name)
    loop_device = str(get_loop_device())
    crypted_mapper_interface = str(get_mapper_interface())
    
    crypted_interface_to_unmount = str(get_mapper_interface_full_path(crypted_mapper_interface))

    if check_mount_status(mount_point_to_unmount):
        unmount_mount_point(mount_point_to_unmount)
    
    """Checks if -p or --pgp option is set, for additional PGP encryption. If true - PGP crypts it. """ 
    if pgp:
        pgp_encrypt(file_disk_name)
        file_cleaner(file_disk_name)

    remove_crypted_interface(crypted_mapper_interface)
    remove_loop_device(loop_device)
    
    
if __name__ == "__main__":
    main()
