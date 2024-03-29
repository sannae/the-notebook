# Microsoft SQL Server :material-database:

The reference repository is [:material-github: sannae/tsql-queries](https://github.com/sannae/tsql-queries).

## About database administration

### Resources, services and processes

* Name of the service and name of the instance:
```sql
select @@servername		-- Hostname and instance name
select @@servicename	-- Instance service name
```

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

* [:material-github:](https://github.com/sannae/tsql-queries/blob/master/Get-DatabaseAndTableSize.sql) It returns infos about the size of the database and the corresponding objects (tables, rows, etc.). On SQL Server:
```sql
/* SQL Server */
-- Returns database Name, Log Size, Row Size, Total Size for current db
SELECT 
      [Database Name] = DB_NAME(database_id)
    , [Log Size (MB)] = CAST(SUM(CASE WHEN type_desc = 'LOG' THEN size END) * 8./1024 AS DECIMAL(8,2))
    , [Row Size (MB)] = CAST(SUM(CASE WHEN type_desc = 'ROWS' THEN size END) * 8./1024 AS DECIMAL(8,2))
    , [Total Size (MB)] = CAST(SUM(size) * 8. / 1024 AS DECIMAL(8,2))
FROM sys.master_files WITH(NOWAIT)
WHERE database_id = DB_ID() -- for current db 
GROUP BY database_id
```                                                                
And on MySQL:
```sql
/* MySql */
-- Returns the database sizes in MB
SELECT 
  table_schema AS "Database", 
  ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS "Size (MB)" 
FROM information_schema.TABLES 
GROUP BY table_schema;

-- Returns the table of a specific DATABASE_NAME
SELECT table_name AS "Table",
ROUND(((data_length + index_length) / 1024 / 1024), 2) AS "Size (MB)"
FROM information_schema.TABLES
WHERE table_schema = "database_name"
ORDER BY (data_length + index_length) DESC;
```

### Users and authentication

* [:material-github:](https://github.com/sannae/tsql-queries/blob/master/TSQL/Set-SqlMixedAuthentication.sql) It activates the [:material-microsoft: Mixed Mode Authentication](https://docs.microsoft.com/en-us/sql/relational-databases/security/choose-an-authentication-mode?view=sql-server-ver15#connecting-through-sql-server-authentication) in the current SQL Server instance:

```sql
USE [master]
GO
/* [Note: 2 indicates mixed mode authentication. 1 is for windows only authentication] */
EXEC xp_instance_regwrite N'HKEY_LOCAL_MACHINE', N'Software\Microsoft\MSSQLServer\MSSQLServer', N'LoginMode', REG_DWORD, 2
GO
```
⚠️ Remember to restart the SQL Server engine service!


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
ALTER SERVER ROLE sysadmin ADD MEMBER YOUR_USERNAME ;  
GO 
```

* Find any object from its description with:

```sql
USE [YOUR_DATABASE]
Select 
  [name] as ObjectName, 
  Type as ObjectType
From Sys.Objects
Where 1=1
    and [Name] like '%YOUR_OBJECT_DESCRIPTION%'
```

Object Types acronyms and names are listed in [:material-microsoft: this MS Learn article](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-objects-transact-sql?view=sql-server-ver16).

### Data and log files

* [:material-github:](https://github.com/sannae/tsql-queries/blob/master/TSQL/Restore-DatabaseBackupWithMove.sql) It restores a backup set from a bak file in the current SQL Server instance, also moving the corresponding files (i.e. basically restoring to a new location, you can find a good guide on this [:material-microsoft: Microsoft Docs page](https://docs.microsoft.com/en-us/sql/relational-databases/backup-restore/restore-a-database-to-a-new-location-sql-server?view=sql-server-ver15)). 
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

* Migrating a SQL Server database to a lower version is not supported, in any version of SQL Server. You may want to consider [generating scripts for the whole database schema and the data](https://www.mssqltips.com/sqlservertip/2810/how-to-migrate-a-sql-server-database-to-a-lower-version) to be executed on the older-version instance.

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

* [:material-stack-overflow:](https://stackoverflow.com/questions/5658457/not-equal-operator-on-null) Check out any condition with `NULL` by using `IS NULL` instead of `=` (and similarly for `IS NOT NULL` and `<>`)! This is especially true with SQL Server:
```sql
/* NULL cheat sheet */
DECLARE @MyNullVariable nvarchar(1)
DECLARE @MyNonNullVariable nvarchar(1)
SET @MyNullVariable = NULL
SET @MyNonNullVariable = '1'

IF (@MyNullVariable = NULL) PRINT 'True' ELSE PRINT 'False'	-- Returns FALSE
IF (@MyNullVariable IS NULL) PRINT 'True' ELSE PRINT 'False' -- Returns TRUE
IF (@MyNullVariable <> NULL) PRINT 'True' ELSE PRINT 'False' -- Returns FALSE
IF (@MyNonNullVariable IS NOT NULL) PRINT 'True' ELSE PRINT 'False' -- Returns TRUE
IF (@MyNonNullVariable <> NULL) PRINT 'True' ELSE PRINT 'False' -- Returns FALSE
```

* ⚠️ **Error SQL71564: Error validating element [YOUR_USER]: The element [YOUR_USER] has been orphaned from its login and cannot be deployed** - means that the user specified in [YOUR_USER] is orphaned, i.e. does not have a corresponding login object, and this can occur even if there _actually_ is a login whose GUID is matching the user's GUID.

So first of all, list the orphaned users:

```sql
EXEC sp_change_users_login 'Report'
```

If you already have a login id and password for this user, fix it by doing:

```sql
EXEC sp_change_users_login 'Auto_Fix', 'YOUR_USER'
```

[:material-github: Here's a GitHub Gist](https://gist.github.com/bradchristie-velir/98b2a730b5594e0d8fccde95cf641d7b) to fix all the orphaned users.

* ⚠️ **Error SQL71654: Error validating element [YOUR_ELEMENT]: the element [YOUR_ELEMENT] cannot be deployed as the script body is encrypted** - in this case the database element [YOUR_ELEMENT] has been encrypted with TDE - i.e. `WITH ENCRYPTION`. [Find the element](#about-database-administration) and check if you can retrieve the encryption, or delete it.

* ⚠️ [**Lock request time out period exceeded** when trying to open tables in SSMS](https://sqljana.wordpress.com/2017/04/01/sql-server-ssms-says-lock-request-time-out-period-exceeded-find-blocking-quickly/). This is because someone is altering a table in the database you are working with and that session has reserved a schema-modification lock. 
  * Run `DBCC OPENTRAN` to find the current open transactions; read the `SPID` number and examine it with `EXEC sp_who2 <SPID>` (an undocumented updated version of [`sp_who2`](https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/sp-who-transact-sql?view=sql-server-ver16)). Also get the session details with `DBCC INPUTBUFFER(<SPID>)` by reading it in the `BlkBy` column. This should get you the 'offending' running operation.
  * A way to get the approximate amount of time required by the operation is to run
  ```sql
  SELECT *
  FROM sys.partitions
  WHERE OBJECT_NAME(object_id)='TransactionPreStage'
  ```
  reading the `object_id` from the inputbuffer table.

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

* [:material-github:](https://github.com/sannae/tsql-queries/blob/master/New-TempTable.sql) Create a *+temporary table** with the result of two other `SELECT`s on other tables:
```sql
-- Total n.1
DECLARE @Total1 NVARCHAR(100)
SET @Total1 = (SELECT COUNT(*) AS [Total1] FROM Table1)
-- Total n.2
DECLARE @Total2 NVARCHAR(100)
SET @Total2 = (SELECT COUNT(*) AS [Total2] FROM Table2)
-- Summary table
DECLARE @Totals TABLE (TableNumber NVARCHAR(100), Total INT)
INSERT INTO @Totals VALUES
	('Table1',@Total1),
	('Table2',@Total2)
SELECT * FROM @Totals
```

* In case you keep seeing the `Invalid object name` error in the query editor, even if SSMS properly shows the objects you're browsing, try [:material-stack-overflow: refreshing the IntelliSense cache](https://stackoverflow.com/questions/1362531/sql-server-invalid-object-name-but-tables-are-listed-in-ssms-tables-list).

## Triggers and automation

* To create an INSERT trigger, follow this template:
```sql
USE DATABASENAME
GO

-- Start transaction
BEGIN TRAN
GO

-- Create trigger
CREATE TRIGGER [dbo].[T_TableName_TriggerName] ON TableName
AFTER INSERT
AS
BEGIN
    /* Trigger body */
END
GO

-- Disable trigger after creation
DISABLE TRIGGER [dbo].[T_TableName_TriggerName] ON TableName

-- Commit transaction
COMMIT
GO
```
The trigger can then be enabled manually on SSMS, or by using
```sql
ENABLE TRIGGER [dbo].[T_TableName_TriggerName] ON TableName
```

* In the trigger body, the records inserted at each transaction are accessible through the virtual table `INSERTED`. Here's an example on how to reach for the values just inserted, i.e. the ones activating the trigger:
```sql
    /* This is the trigger body */
    /* The following example copies some values of the record inserted in TableName directly into DestinationTable */

  -- SET NOCOUNT ON added to prevent extra result sets from
  -- interfering with SELECT statements.
  SET NOCOUNT ON;

    -- Select the record from TableName and add it to DestinationTable
  INSERT INTO DestinationTable
	(field1, field2, ...)
	SELECT
		TableName.Field1, TableName.Field2, ...
	FROM INSERTED
	-- Some other conditions like JOIN or WHERE
```

* The same applies for a DELETE trigger (`CREATE TRIGGER [dbo].[T_TableName_TriggerName] ON TableName AFTER DELETE`): the deleted record are accessible by the trigger from the `DELETED` table