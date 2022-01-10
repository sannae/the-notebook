# Windows :material-microsoft-windows:

## Windows Subsystems for Linux (WSL) 2

!!! info
    TBD

!!! warning
    Always use a Powershell session as Administrator!

### On Windows 11 / Windows 10 2004 build >= 19041

### On Windows 10 1903 build >= 18362


## To be ordered

* Activate WSL
    * On Windows 10 build >= 19041 or Windows 11: `wsl --install`
    * On previous versions of Windows: 
    ```powershell
    dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
    ```
* Upgrade to WSL2 and set default version
    * On Windows 10 build >= 19041 or Windows 11: automatically handled by the previous command
    * On previous versions of Windows:
* Solve DNS issue
    * Procedure: https://superuser.com/questions/1533291/how-do-i-change-the-dns-settings-for-wsl2
    * Also helpful: https://www.ricmedia.com/set-permanent-dns-nameservers-ubuntu-debian-resolv-conf/
    * Watch out the firewall!

* Create a SSH key pair on Windows