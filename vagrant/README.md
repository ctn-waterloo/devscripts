# Windows Vagrant Box

This folder provides a Vagrantfile to run unit test easily in a windows
environment. You must be a CTN member to get access to the actual Vagrant box.

## Usage

1. Install [VirtualBox](https://www.virtualbox.org/).
2. Install [Vagrant](https://www.vagrantup.com/). You will need at least version
   1.6. The version provided by your linux distribution might be too old.
3. Copy `Vagrantfile` and `wintest.sh` to your project's root folder.
4. Execute `./wintest.sh`.

The first time you do this the vagrant base box has to be downloaded and
installed. The download requires authorization and you have to enter a
password. Unfortunately, there will be no prompt asking you for a password. The
cursor will just stay there on the screen and wait for your input. (Ask someone
in the lab for the password.)

That will run the unit tests with `tox`. When your finished with testing halt
the virtual machine with `vagrant halt`.

Windows remote desktop access is also working. It is supposed to work with
`vagrant rdp`, but might not. In that case connect with `rdesktop
127.0.0.1:3389` (you have to install rdesktop first).

To boot and shutdown use `vagrant up` and `vagrant halt`.

The directory containing the Vagrantfile will be synced into the `/vagrant`
Cygwin folder on boot with `rsync` (that folder is also accessible as normal
Windows folder somewhere in the filesystem). To resync after boot up use
`vagrant rsync`.

## Environment

The virtual machine has Python versions 2.6, 2.7, 3.3, and 3.4 installed. None
of them is in the path, thus you have to use full paths. Note that there is
also a Python install by Cygwin which might be in the path. **Avoid** using it.
It allows for some things (e.g. `os.statvfs`) which usually are not support by
Python on Windows.

In addition to the Python base installs some packages like NumPy, SciPy, and
Matplotlib are installed.

The base box contains also a Cygwin install providing SSH, Bash, Zsh, Vim, and
Emacs. Yes, you can ssh into the Windows system with `vagrant ssh`.
