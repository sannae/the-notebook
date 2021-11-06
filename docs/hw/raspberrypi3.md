# Raspberry Pi 3 :material-raspberry-pi:

A few notes on setting up a Raspberry Pi 3 for some experiments.

??? Resources
    * "Getting started" documentation: <https://www.raspberrypi.com/documentation/computers/getting-started.html> 

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
	protocol=PROVIDER
	login=MY_USERNAME
	password='MY_PASSWORD'
	FULL_HOSTNAME
    ```
    * Restart the service with `sudo service ddclient restart`
    * Remember to create `FULL_HOSTNAME` on `PROVIDER`
* Set up static IP address
```bash
# Set a static ip by editing /etc/dhcpcd.conf
interface [eth0,wlan0] 
static ip_address=STATIC_IP_ADDRESS
static routers=ROUTER_IP_ADDRESS
static domain_name_servers=DNS_IP_ADDRESS
```
* Set port forwarding on router
* Open SSH connection
    * Edit the file `/etc/ssh/sshd_config`:
    ```bash
    port=PORT_NUMBER  # Change SSH default port 
    PermitRootlogin=no entry # Changed SSH login of root 
    AllowUsers=user # Allowed SSH login of 'user'
    Banner=PATH_OF_BANNER_FILE # Created ssh-banner file containing a warning, then edited Banner entry with the path
    ```
    * Restart the service with `/etc/init.d/ssh restart`
    * Basically, now you can login as 'user' and then switch to a different administrator user
* Set up dev environment
  * VS code (`apt-get install code`)
  * Git (`apt-get instaLL git`)
  * Ruby (`apt-get install ruby-full`) an Rails (`gem install rails`)

## Set up an external storage

Full instructions [here](https://raspberrypi.org/documentation/configuration/external-storage.md>).

* Install exFAT driver: it may be useful in mounting the HDD storage
```bash
apt-get install exfat-fuse
```	
* listing all the disk partitions and indentifying the one corresponding to the USB driver)
```bash
lsblk -o UUID,NAME,FSTYPE,SIZE,MOUNTPOINT,LABEL,MODEL 
```  
* Getting the location of the disk partition, usually `/dev/DISK_LOCATION`
```bash
blkid
```
* Creating a target folder to be the mount point of the USB drive
```bash
mkdir /mnt/MOUNT_POINT_NAME 
```
* *Mounting the drive from the location of the partition to the mount point
```bash
mount /dev/DISK_LOCATION /mnt/MOUNT_POINT_NAME
```
* Check the content of the drive
```
ls -l /mnt/MOUNT_POINT_NAME
```
* Setting automounting
    * Retrieving the UUID
    ```bash
    blkid
    ```
    * editing the file `/etc/fstab` with the location of all partitions to be mounted at boot. Add the line
    ```bash
    UUID=<UUID> /mnt/MOUNT_POINT_NAME FORMAT BOOT_OPTIONS 0 2
    ```
* Format the USB drive in VFAT
    * retrieving the partition location
    ```bash
    lsblk
    ```
    * unmounting: it's mandatory before formatting
    ```bash
    umount /dev/PARTITION
    ```
    * formatting with VFAT
    ```bash
    mkfs.vfat -n 'PARTITION_NAME' /dev/PARTITION  
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
* Mounting an [external HDD](raspberrypi.org/documentation/configuration/external-storage.md) + Installing OwnCloud/NextCloud
* Continuing on SSH security: DSA public key authentication