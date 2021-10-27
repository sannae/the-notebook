# tsql

The reference repository is [:material-github: sannae/tsql-queries](https://github.com/sannae/tsql-queries).

## About database administration

### Resources and processes

* [:material-github:](https://github.com/sannae/tsql-queries/blob/master/TSQL/Get-Connections.sql) List all the processes with an open connection to the current instance:

```sql
SELECT hostname, COUNT(hostname) AS Processes
FROM sys.sysprocesses AS P
JOIN sys.sysdatabases AS D ON (D.dbid = P.dbid)
JOIN sys.sysusers AS U ON (P.uid = U.uid)
GROUP BY hostname
ORDER BY COUNT(hostname) DESC
```

* [:material-github:](https://github.com/sannae/tsql-queries/blob/master/TSQL/Get-CurrentResources.sql) Show the currently allocated physical memory:

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

### Users and authentication

* [:material-github:](https://github.com/sannae/tsql-queries/blob/master/TSQL/Set-SqlMixedAuthentication.sql) It activates the [:material-microsoft-windows: Mixed Mode Authentication](https://docs.microsoft.com/en-us/sql/relational-databases/security/choose-an-authentication-mode?view=sql-server-ver15#connecting-through-sql-server-authentication) in the current SQL Server instance:

```sql
USE [master]
GO
/* [Note: 2 indicates mixed mode authentication. 1 is for windows only authentication] */
EXEC xp_instance_regwrite N'HKEY_LOCAL_MACHINE', N'Software\Microsoft\MSSQLServer\MSSQLServer', N'LoginMode', REG_DWORD, 2
GO
```
:warning: Remember to restart the SQL Server engine service!


* [:material-github:](https://github.com/sannae/tsql-queries/blob/master/TSQL/Get-SqlUsersRoles.sql) It lists all SQL server users, specifying the corresponding roles:

```sql
SELECT spU.name, MAX(CASE WHEN srm.role_principal_id = 3 THEN 1 END) AS sysadmin
    ,MAX(CASE WHEN srm.role_principal_id = 4 THEN 1 END) AS securityadmin
    ,MAX(CASE WHEN srm.role_principal_id = 5 THEN 1 END) AS serveradmin
    ,MAX(CASE WHEN srm.role_principal_id = 6 THEN 1 END) AS setupadmin
    ,MAX(CASE WHEN srm.role_principal_id = 7 THEN 1 END) AS processadmin
    ,MAX(CASE WHEN srm.role_principal_id = 8 THEN 1 END) AS diskadmin
    ,MAX(CASE WHEN srm.role_principal_id = 9 THEN 1 END) AS dbcreator
    ,MAX(CASE WHEN srm.role_principal_id = 10 THEN 1 END) AS bulkadmin
FROM sys.server_principals AS spR
JOIN sys.server_role_members AS srm ON spR.principal_id = srm.role_principal_id
JOIN sys.server_principals AS spU ON srm.member_principal_id = spU.principal_id
WHERE spR.[type] = 'R' 
GROUP BY spU.name
```

* [:material-github:](https://github.com/sannae/tsql-queries/blob/master/TSQL/New-SqlSysadminUser.sql) It creates a new sysadmin login with the specified password:

```sql
USE DATABASE_NAME
-- Creates new login
CREATE LOGIN YOUR_USERNAME WITH PASSWORD = 'YOUR_PASSWORD';
GO
-- Assigns the sysadmin server role
EXEC master..sp_addsrvrolemember @loginame = N'YOUR_USERNAME', @rolename = N'sysadmin'
GO
```

### Data and log files

* [:material-github:](https://github.com/sannae/tsql-queries/blob/master/TSQL/Restore-DatabaseBackupWithMove.sql) It restores a backup set from a bak file in the current SQL Server instance, also moving the corresponding files (i.e. basically restoring to a new location, you can find a good guide on this [:material-microsoft-windows: Microsoft Docs page](https://docs.microsoft.com/en-us/sql/relational-databases/backup-restore/restore-a-database-to-a-new-location-sql-server?view=sql-server-ver15)). 
    * Start by getting the logical names of the data and log files. The following `RESTORE` statement cannot be embedded into a `SELECT`, although you can use it to `INSERT` the values in a temporary table (following [:material-stack-overflow: this answer on Stack Overflow](https://stackoverflow.com/a/4018782))
    ```sql
    -- Get logical names
    RESTORE FILELISTONLY FROM DISK='C:\MY\PATH\TO\BAK\FILE.bak' WITH FILE=1
    ```
    * Then perform the restore with the option `MOVE` to replace the original data and log paths with new ones, if required:
    ```sql
    -- Restore database
    RESTORE DATABASE YOUR_DATABASE FROM DISK='C:\MY\PATH\TO\BAK\FILE.bak'
    WITH 
    MOVE YOUR_DATA_LOGICAL_NAME TO 'C:\MY\NEW\PATH\TO\MDF\FILE.mdf',
    MOVE YOUR_LOG_LOGICAL_NAME TO 'C:\MY\NEW\PATH\TO\LDF\FILE.ldf',
    RECOVERY, REPLACE, STATS = 10;
    ```

* [:material-github:](https://github.com/sannae/tsql-queries/blob/master/TSQL/Get-SqlFilePaths.sql) Returns a list of all the logical and physical names for the files of every database in the current SQL Server instance. Source [here](https://blog.sqlauthority.com/2018/11/19/sql-server-get-list-of-the-logical-and-physical-name-of-the-files-in-the-entire-database/).

```sql
SELECT 
  d.name DatabaseName, 
  f.name LogicalName,
  f.physical_name AS PhysicalName,
  f.type_desc TypeofFile
FROM sys.master_files f
INNER JOIN sys.databases d ON d.database_id = f.database_id
GO
```

### Troubleshooting

* [:material-github:](https://github.com/sannae/tsql-queries/blob/master/TSQL/Stop-SqlConnections.sql) Isolate the database (i.e. put it in "single user mode") from any connection in order to perform maintenance tasks:
    ```sql
    USE YOUR_DATABASE
    GO
    ALTER DATABASE YOUR_DATABASE
    SET SINGLE_USER
    WITH ROLLBACK IMMEDIATE
    GO
    ```
    Then do all your operations, and finally:
    ```sql
    -- Set the database back in to multiple user mode
    USE YOUR_DATABASE
    GO
    ALTER DATABASE YOUR_DATABASE 
    SET MULTI_USER
    GO
    ```

* [:material-github:](https://github.com/sannae/tsql-queries/blob/master/TSQL/Get-SqlErrorLogPath.sql) Retrieves the SQL Server Error Log: it returns the error log path for the current SQL Server instance ([guide here](https://blog.sqlauthority.com/2015/03/24/sql-server-where-is-errorlog-various-ways-to-find-its-location/)):

    ```sql
    USE master
    GO
    EXEC xp_readerrorlog 0, 1, N'Logging SQL Server messages in file'
    GO
    ```
    If the connection to SQL Server is not available, you may find the error log with the following options:

    1. SQL Server Configuration Manager > SQL Server Services > SQL Server (INSTANCE_NAME) > Properties > Startup Parameters > add `-e`
    2. Open **regedit** > Go to `Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Microsoft SQL Server\(version)\MSSQLServer\Parameters`

## Browsing data and tables

* [:material-github:](https://github.com/sannae/tsql-queries/blob/master/TSQL/Get-TableName.sql) It searches a table in the specified DATABASE_NAME by looking for PATTERN in table name

```sql
USE DATABASE_NAME SELECT * FROM information_schema.tables WHERE Table_name LIKE '%PATTERN%'
```

* [:material-github:](https://github.com/sannae/tsql-queries/blob/master/TSQL/Get-TablesProperties.sql) It lists the general properties (rows, total occupied space, total free space, etc.) of all the tables in a specified DATABASE_NAME

```sql
USE DATABASE_NAME
SELECT 
    t.NAME AS TableName,
    s.Name AS SchemaName,
    p.rows AS RowCounts,
    SUM(a.total_pages) * 8 AS TotalSpaceKB, 
    CAST(ROUND(((SUM(a.total_pages) * 8) / 1024.00), 2) AS NUMERIC(36, 2)) AS TotalSpaceMB,
    SUM(a.used_pages) * 8 AS UsedSpaceKB, 
    CAST(ROUND(((SUM(a.used_pages) * 8) / 1024.00), 2) AS NUMERIC(36, 2)) AS UsedSpaceMB, 
    (SUM(a.total_pages) - SUM(a.used_pages)) * 8 AS UnusedSpaceKB,
    CAST(ROUND(((SUM(a.total_pages) - SUM(a.used_pages)) * 8) / 1024.00, 2) AS NUMERIC(36, 2)) AS UnusedSpaceMB
FROM sys.tables t
INNER JOIN sys.indexes i ON t.OBJECT_ID = i.object_id
INNER JOIN sys.partitions p ON i.object_id = p.OBJECT_ID AND i.index_id = p.index_id
INNER JOIN sys.allocation_units a ON p.partition_id = a.container_id
LEFT OUTER JOIN sys.schemas s ON t.schema_id = s.schema_id
WHERE t.NAME NOT LIKE 'dt%' AND t.is_ms_shipped = 0 AND i.OBJECT_ID > 255 
GROUP BY t.Name, s.Name, p.Rows
ORDER BY t.Name
```