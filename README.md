os-utils: utilities, wrappers and modules for various OS tasks
-


* mkcryptodisk.py - creates crypted disk using "cryptsetup", "dd" and "mkfs". Also has option to PGP encrypt
* mountcryptodisk.py - mounts crypted disk, if appropriate devices does not exits, it will creat them.
* umountcryptodisk.py - umounts crypted disk and cleans up block device mess.
* block_device.py - module for manipulating block devices and disk files.
* os_env.py - module for geting various OS parameters and performing checks.
* change-digitalvibrance.sh - little script for changing digital vibrance for nvidia GPU on linux
* sysdiag.sh - skeleton script for initial system diagnostics

To create awesome greyscale like:
```bash
./change-digitalvibrance.sh -1024
```
To play csgo:
```bash
./change-digitalvibrance.sh 1023
```
Back to default:
```bash
./change-digitalvibrance.sh 1023
```

