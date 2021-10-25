# Raspberry Pi 3

A few notes on setting up a Raspberry Pi 3 for some experiments.

## Initial
* Update all the packages
```bash
sudo apt-get update && sudo apt-get upgrade
```
* Set up DNS
    * Install ddclient:
    ```bash
    sudo apt-get install ddclient
    ``` 
    * Configure ddclient by editing ` /etc/ddclient.conf`
    ```
	use=web 
	ssl=yes 
	protocol=[provider]
	login=[username]
	password='[password]'
	[full_hostname]
    ```
    * Restart the service with `sudo service ddclient restart`
    * Remember to create `[full_hostname]` on `[provider]`
* Set up static IP address
```bash
# Set a static ip by editing /etc/dhcpcd.conf
interface [eth0,wlan0] 
static ip_address=[static_ip_address]
static routers=[router_ip_address]
static domain_name_servers=[dns_ip_address]
```
* Set port forwarding on router
* Open SSH connection
    * Edit the file `/etc/ssh/sshd_config`:
    ```bash
    port=[port_number]  # Change SSH default port 
    PermitRootlogin=no entry # Changed SSH login of root 
    AllowUsers=user # Allowed SSH login of 'user'
    Banner=[path_of_banner_file] # Created ssh-banner file containing a warning, then edited Banner entry with the path
    ```
    * Restart the service with `/etc/init.d/ssh restart`
    * Basically, now you can login as 'user' and then switch to a different administrator user
* Set up dev environment
  * VS code (`apt-get install code`)
  * Git (`apt-get instaLL git`)
  * Ruby (`apt-get install ruby-full`) an Rails (`gem install rails`)

## Set up an external storage
Full instructions at <raspberrypi.org/documentation/configuration/external-storage.md>

* Install exFAT driver: it may be useful in mounting the HDD storage
```bash
apt-get install exfat-fuse
```	
* listing all the disk partitions and indentifying the one corresponding to the USB driver)
```bash
lsblk -o UUID,NAME,FSTYPE,SIZE,MOUNTPOINT,LABEL,MODEL 
```  
* Getting the location of the disk partition, usually /dev/<disk-location>
```bash
blkid
```
* Creating a target folder to be the mount point of the USB drive
```bash
mkdir /mnt/[mount-point-name] 
```
* *Mounting the drive from the location of the partition to the mount point
```bash
mount /dev/[disk-location] /mnt/[mount-point-name]
```
* Check the content of the drive
```
ls -l /mnt/[mount-point-name]
```
* Setting automounting
    * Retrieving the UUID
    ```bash
    blkid
    ```
    * editing the file with the location of all partitions to be mounted at boot
    ```bash
    nano /etc/fstab # add line "UUID=<UUID> /mnt/<mount-point-name> <format> <boot-options> 0 2"
    ```
* Format the USB drive in VFAT
    * retrieving the partition location
    ```bash
    lsblk
    ```
    * unmounting: it's mandatory before formatting
    ```bash
    umount /dev/[partition]
    ```
    * formatting with VFAT
    ```bash
    mkfs.vfat -n '[partition-name]' /dev/[partition]  
    ```
USB key -made of one single VFAT partition- perfectly usable!

## Install Jupyter Notebook

* Install python3
```bash
apt-get update
apt-get install python3-matplotlib
apt-get install python3-scipy
pip3 install --upgrade pip
```
* Reboot
* Install jupyter
```bash
sudo pip3 install jupyter
sudo apt-get clean
```
* SSH-ing with a specific user ID runs the Jupyter Notebook from `/run/user/ID`, which may not have the permissions. 
This comes from the env variable `$XDG_RUNTIME_DIR`, which does not change after substituting user. Just go with:
```bash
export XDG_RUNTIME_DIR=""
```
(but since it's uncomfortable to set it at each login, just edit `~/.profile` adding `export XDG_RUNTIME_DIR`)
* Run jupyter notebook:
```bash
jupyter notebook
```
!!! warning
    If port 8888 is still not reachable from SSH, go to PuTTY `Settings > Tunnels > Source port = 8888, Destination=127.0.0.1:8888`
* Now your Jupyter Notebook is working from browser on <127.0.0.1:8888/TOKEN> !

### Next steps
* Making an SD gzipped image of the system and uploading it in the cloud (e.g. Dropbox)
* Mounting an external HDD + Installing OwnCloud/NextCloud (<raspberrypi.org/documentation/configuration/external-storage.md>)
* Continuing on SSH security: DSA public key authentication