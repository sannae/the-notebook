# tsql

The reference repository is [:github: sannae/tsql-queries](https://github.com/sannae/tsql-queries).

## About database administration

* [:github:](https://github.com/sannae/tsql-queries/blob/master/TSQL/Get-Connections.sql) List all the processes with an open connection to the current instance:

```sql
SELECT hostname, COUNT(hostname) AS Processes
FROM sys.sysprocesses AS P
JOIN sys.sysdatabases AS D ON (D.dbid = P.dbid)
JOIN sys.sysusers AS U ON (P.uid = U.uid)
GROUP BY hostname
ORDER BY COUNT(hostname) DESC
```

* [:github:](https://github.com/sannae/tsql-queries/blob/master/TSQL/Get-CurrentResources.sql) Show the currently allocated physical memory:

```sql
-- The following queries return information about currently allocated memory.
SELECT
(total_physical_memory_kb/1024) AS Total_OS_Memory_MB,
(available_physical_memory_kb/1024)  AS Available_OS_Memory_MB
FROM sys.dm_os_sys_memory;

SELECT  
(physical_memory_in_use_kb/1024) AS Memory_used_by_Sqlserver_MB,  
(locked_page_allocations_kb/1024) AS Locked_pages_used_by_Sqlserver_MB,  
(total_virtual_address_space_kb/1024) AS Total_VAS_in_MB,
process_physical_memory_low,  
process_virtual_memory_low  
FROM sys.dm_os_process_memory; 

-- The following query returns information about current SQL Server memory utilization.
SELECT
sqlserver_start_time,
(committed_kb/1024) AS Total_Server_Memory_MB,
(committed_target_kb/1024)  AS Target_Server_Memory_MB
FROM sys.dm_os_sys_info;
```

* [:github:](https://github.com/sannae/tsql-queries/blob/master/TSQL/Get-SqlErrorLogPath.sql) Retrieve the SQL Server Error Log: it returns the error log path for the current SQL Server instance ([guide here](https://blog.sqlauthority.com/2015/03/24/sql-server-where-is-errorlog-various-ways-to-find-its-location/)):

```sql
USE master
GO
EXEC xp_readerrorlog 0, 1, N'Logging SQL Server messages in file'
GO
```
If the connection to SQL Server is not available, you may find the error log with the following options:
1. SQL Server Configuration Manager > SQL Server Services > SQL Server (INSTANCE_NAME) > Properties > Startup Parameters > add `-e`
2. Open **regedit** > Go to `Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Microsoft SQL Server\(version)\MSSQLServer\Parameters`

