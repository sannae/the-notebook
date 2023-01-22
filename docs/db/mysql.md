# mysql

* [material-stack-overflow] In case of error similar to:

```
2023-01-22 20:41:05 0 [ERROR] mysqld.exe: Aria recovery failed. Please run aria_chk -r on all Aria tables and delete all aria_log.######## files
...
2023-01-22 20:41:05 0 [ERROR] Could not open mysql.plugin table. Some plugins may be not loaded
2023-01-22 20:41:05 0 [ERROR] Failed to initialize plugins.
2023-01-22 20:41:05 0 [ERROR] Aborting
```

Remove (or rename) the following files in the MySQL root folder (in this case `C:\XAMPP\MySql\data`, in Linux in `/var/lib/mysql`):

```
ib_logfile0
ib_logfile1
aria_log_control
```

Then restart the service.
