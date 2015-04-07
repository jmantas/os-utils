# -*- mode: python; coding: utf-8 -*-
#

""" module for manipulating block devices and disk files"""

import subprocess
import os
import os_env


def check_loop_device():
    """ implemented in os_env.py as file_checker() ?"""
    pass


def create_loop_device(loop_device):
    """ creates loop device ( block device major number 7 ) """

    user_id = str(os_env.get_user_id())
    print "Creating loop device disk %s" % loop_device
    if subprocess.check_call(["sudo", "mknod", loop_device, "b", "7", user_id]) == 0:
        os_env.print_success()


def link_loop_device(loop_device, file_disk_name_to_link):
    """ links disk file to loop device """

    print "Linking loop device %s to %s " % (loop_device, file_disk_name_to_link)
    if subprocess.check_call(["sudo", "losetup", loop_device, file_disk_name_to_link]) == 0:
        os_env.print_success()


def check_crypted_interface_status(crypted_mapper_interface):
    """ checks crypted interface status """

    if subprocess.check_call(["sudo", "cryptsetup", "status", crypted_mapper_interface]) != 0:
        print "% does not exist." % crypted_mapper_interface
        return False
    else:
        return True


def create_crypted_interface(mapper_interface, loop_device):
    """ creates crypted interface to the loop device which is linked to disk file """

    mapper_interface_path = str(os_env.get_mapper_interface_full_path(mapper_interface))

    print "Creating aes-cbc-essiv:sha256 crypted interface %s to %s" % (mapper_interface_path, loop_device)
    if subprocess.check_call(["sudo", "cryptsetup", "-c", "aes-cbc-essiv:sha256", \
        "create", mapper_interface, loop_device]) == 0:
        os_env.print_success()


def check_disk_file_status():
    """ implemented in os_env.py as file_checker() ?"""
    pass

def create_disk_file(file_disk_name_to_create, disk_size):
    """ creates disk file and fills it with zeroes
        todo: implement configuration parsing for disk size
    """
    print "Creating zeroed disk %s" % file_disk_name_to_create
    output_file = "of=" + file_disk_name_to_create
    input_file = "if=/dev/zero"
    block_size = "bs=1M"
    block_count = "count=%s" % disk_size
    if subprocess.check_call(["sudo", "dd", input_file, output_file, block_size, block_count]) == 0:
        os_env.print_success()


def create_fs(file_system_type, mapper_interface_path):
    """ creates file system on crypted mapper interface """

    print "Creating %s file system on %s " %  (file_system_type, mapper_interface_path)
    if subprocess.check_call(["sudo", "mkfs.%s" % file_system_type, mapper_interface_path]) == 0:
        os_env.print_success()


def check_mount_status(mount_point_to_check):
    """ checks if mountpoint is mounted or not """

    return os.path.ismount(mount_point_to_check)


def mount_crypted_disk(crypted_interface_to_mount, directory_to_mount):
    """ mounts already crypted disk """

    if not check_mount_status(directory_to_mount):
        print "Mounting %s to %s" % (crypted_interface_to_mount, directory_to_mount)
        if subprocess.check_call(["sudo", "mount", crypted_interface_to_mount, directory_to_mount]) == 0:
            print os_env.print_success()
    else:
        print "Disk/mountpoint is mounted"


def unmount_mount_point(mount_point_to_unmount):
    """ unmounts mountpoint """

    print "Unmounting %s" % mount_point_to_unmount
    if check_mount_status(mount_point_to_unmount):
        if subprocess.check_call(["sudo", "umount", mount_point_to_unmount]) == 0:
            os_env.print_success()
    else:
        print "Mountpoint is not mounted"


def remove_crypted_interface(mapper_interface):
    """ removes /dev/mapper/*.crypt interface """

    mapper_interface_path = str(os_env.get_mapper_interface_full_path(mapper_interface))
    if os_env.file_checker(mapper_interface_path):
        print "Removing crypted interface %s" % mapper_interface_path
        if subprocess.check_call(["sudo", "cryptsetup", "remove", mapper_interface]) == 0:
            os_env.print_success()


def remove_loop_device(loop_device):
    """ removes /dev/loop<userID> device"""

    if os_env.file_checker(loop_device):
        print "Detaching from loop device %s" % loop_device
        if subprocess.check_call(["sudo", "losetup", "-d", loop_device]) == 0:
            os_env.print_success()
        print "Removing loop device %s" % loop_device
        if subprocess.check_call(["sudo", "rm", loop_device]) == 0:
            os_env.print_success()


def pgp_encrypt(file_name_to_pgp_encrypt):
    """ encrypts using GnuPG with simple symetric key """

    print "Encrypting %s with symetric key" % file_name_to_pgp_encrypt
    if subprocess.check_call(["gpg", "--symetric", file_name_to_pgp_encrypt]) == 0:
        os_env.print_success()



def pgp_decrypt(file_name_to_pgp_decrypt, file_name_to_save):
    """ decrypts using GnuPG """

    print "Decrypting %s to %s" % (file_name_to_pgp_decrypt, file_name_to_save)
    if subprocess.check_call(["gpg","--output", file_name_to_save, "--decrypt", file_name_to_pgp_decrypt]) == 0:
        os_env.print_success()


def file_cleaner(file_to_remove):
    """Remove file"""
    print "Removing %s" % file_to_remove
    if subprocess.check_call(["sudo", "rm", "-f", file_to_remove]) == 0:
        os_env.print_success()
    
