#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

""" utility to unmount crypted disk file in *nix"""

import click
import os_env
import block_device

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
    file_disk_name = "%s/%s" % (os_env.get_user_homedir(), name)
    loop_device = str(os_env.get_loop_device())
    crypted_mapper_interface = str(os_env.get_mapper_interface())
    
    crypted_interface_to_unmount = str(os_env.get_mapper_interface_full_path(crypted_mapper_interface))

    if block_device.check_mount_status(mount_point_to_unmount):
        block_device.unmount_mount_point(mount_point_to_unmount)
    
    """Checks if -p or --pgp option is set, for additional PGP encryption. If true - PGP crypts it. """ 
    if pgp:
        block_device.pgp_encrypt(file_disk_name)
        block_device.file_cleaner(file_disk_name)

    block_device.remove_crypted_interface(crypted_mapper_interface)
    block_device.remove_loop_device(loop_device)
    
    
if __name__ == "__main__":
    main()
