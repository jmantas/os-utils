#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

""" utility to make crypted disk files on *nix"""

import click
import os_env
import block_device

@click.command()
@click.option('--name', default="crypteddisk",
                help='Disk name. Default = crypteddisk' )
@click.option('--size', default=64,
                help='Disk size. Default = 64M')
@click.option('--fstype', default="ext3",
                help='File system type. Default = ext3')
@click.option('--pgp/--no-pgp', default=False, 
                help='PGP encrypt. Default = False')
def main(name, size, fstype, pgp):
    loop_device = str(os_env.get_loop_device())
    mapper_interface = name + ".crypt" 
    mapper_interface_path = str(os_env.get_mapper_interface_full_path(mapper_interface))
    file_system_type = fstype
    disk_size = size

    file_disk_name = "%s/%s" % (os_env.get_user_homedir(), name)

    """If disk file does not exist, create it"""
    if not os_env.file_checker(file_disk_name):
        block_device.create_disk_file(file_disk_name, size)
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
   
    """Checks if --pgp option is set, for additional PGP encryptio. If true - PGP crypts it""" 
    if pgp:
        block_device.pgp_encrypt(file_disk_name)
        block_device.file_cleaner(file_disk_name)

    """Cleans not needed block devices"""
    block_device.remove_crypted_interface(mapper_interface)
    block_device.remove_loop_device(loop_device)


if __name__ == "__main__":
    main()
