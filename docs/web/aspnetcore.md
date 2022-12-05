# ASP.NET Core [:material-dot-net:]

![architecture](https://docs.microsoft.com/it-it/dotnet/architecture/modern-web-apps-azure/media/image5-12.png)

![stack](https://files.speakerdeck.com/presentations/ae3a80c1020e47f5af633bb96e0968fd/slide_5.jpg)

## dotnet cli

Obviously you're going to need the latest .NET SDK (check it with `dotnet check`).

### Standard `new` templates

```powershell
dotnet new mvc --name MyMvcWebApplicationProjectName
dotnet new sln --name MyMvcWebApplicationSolutionName
dotnet sln ./MyMvcWebApplicationSolutionName.sln add ./MyMvcWebApplicationProjectName.csproj 
```

### Using an OrchardCore Project

The following example is to create a new project with an OrchardCoreCMS template in the current directory:

```powershell
dotnet new install OrchardCore.ProjectTemplates # Optional: to install 'dotnet new' templates
dotnet new occms --name OrchardCoreTest
dotnet new sln --name OrchardCoreTest
dotnet sln ./OrchardCoreTest.sln add ./OrchardCoreTest.csproj
dotnet build --verbosity normal # Optional: testing that the project is building
dotnet run # Run Kestrel
```

## Creating the project

## Using Entity Framework Core

:book: Following the [Entity Framework Core for Beginners series](https://www.youtube.com/playlist?list=PLdo4fOcmZ0oXCPdC3fTFA3Z79-eVH3K-s) on the [.NET YouTube channel](https://www.youtube.com/c/dotNET)!

### Creating a database

* Install NuGet packages:
	* EntityFrameworkCore
	* EntityFrameworkCore.Design
	* EntityFrameworkCore.Tools
	* EntityFrameworkCore.SqlServer (if you're planning to use SqlServer)
* In VSCode, use
```csharp
dotnet tool install --global dotnet-ef
```
* Create the classes in `/Models` mirroring the data models
* Create the database context in `/Data/DATABASENAMEContext.cs`
	* The connection string should _not_ be hardcoded: instead it should be securely stored, e.g. [follow here](https://aka.ms/ef-core-connection-strings)
	
> One way to do this is by storing them in a separate JSON file using [User Secrets](https://docs.microsoft.com/en-us/aspnet/core/security/app-secrets?view=aspnetcore-6.0&tabs=windows) ([YourProject]>[Manage User Secrets]) that you can exclude from source control. 

> User secrets are automatically added to the `appsettings.json` configuration file, so they're available in the `builder.Configuration` object. 

> The snippet to be used when configuring the db context in `Program.cs` is
```csharp
builder.Services.AddDbContext<assistenza_backupContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("PARAMETERNAME")));
```
> Where the parameter will appear in your `secrets.json` as:
```json
{
	"ConnectionString:PARAMETERNAME": "Data Source=(localdb)\\SQLEXPRESS; ..."
}
```
> in VSCode, use `dotnet user-secrets init` then `dotnet user-secrets set "PROPERTY" "VALUE"`

:warning: `secrets.json` is _not_ encrypted!

If you don't wish to use the User Secrets, you can add the connection string in the configuration file, for example:
```json
  "ConnectionStrings": {
    "DBNAME": "Server=SERVERNAME\\INSTANCENAME;Database=DBNAME;Trusted_Connection=True;"
  }
```

* Create the database with the first initial create migration
	* In VS, use the Package Manager Console and type `Add-migration InitialCreate`
	* In VSCode, `dotnet ef migrations add InitialCreate`
* Review the migration before committing it!
* Apply the migration using:
    * In VS, the command `Update-database` in the Package Manager Console
	* In VSCode, `dotnet ef database update`

### Using an existing database

⭐ Start with [this tutorial](https://www.learnentityframeworkcore.com/walkthroughs/existing-database).

* From the Package Manager Console, use `Scaffold-DbContext "CONNECTIONSTRING" Microsoft.EntityFrameworkCore.SqlServer -ContextDir data -OutputDir Models -DataAnnotation` where:
    * `"CONNECTIONSTRING"` is just the connection string, like `"Server=(local)\localdb;Database=DB_NAME;Trusted_Connection=True"`
	* `Microsoft.EntityFrameworkCore.SqlServer` is the provider
	* `-ContextDir` specifies the destination of the DbContext class
	* `-OutputDir` specifies the destination of the created Models
	* `-DataAnnotation` specifies the usage of Data Annotation
* In VSCode, use `dotnet ef dbcontext scaffold ...` followed by the same options
* Then, to match the scaffolded schema within the migration logic,
    * `Add-migration InitialCreate` to create the migration first script
	* Manually remove the content of the `Up` method in the script
    * `Update-database` to apply the migration

* The fields in a model can be renamed by just changing the properties names (it will rename the corresponding db columns) and then migrating up

### Applying migrations

* ❌ When applying the migration (`upgrade-database...`) if you ever encounter the error `Execution Timeout Expired.  The timeout period elapsed prior to completion of the operation or the server is not responding. Could not create constraint or index. See previous errors. Operation cancelled by user. The statement has been terminated.` you may [extend the command timeout](https://stackoverflow.com/questions/39006847/how-to-set-entity-framework-core-migration-timeout) using something like:
```csharp
builder.Services.AddDbContext<YOUR_DB_CONTEXT>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("YOUR_DB_CONTEXT_CONNECTION_STRING"),
    opts => opts.CommandTimeout((int)TimeSpan.FromMinutes(5).TotalSeconds)));
```

### Connect to multiple DBs

Note: https://khalidabuhakmeh.com/how-to-add-a-view-to-an-entity-framework-core-dbcontext

#### First try connecting to multiple providers (e.g. MS Access & SQL Server )

Following for instance this [DEV article](https://dev.to/moesmp/ef-core-multiple-database-providers-3gb7).

#### Migrate from MS Access to SQL Server

* Unfortunately, the [MS Access JET provider](https://github.com/bubibubi/EntityFrameworkCore.Jet) for Entity Framework Core is not supported from EFCore>=6.0.0 and compatibility would require a downgrade to <5.0.0
* Therefore, the best way is to convert your MS Access database into a more recent and supported RDBMS, e.g. SQL Server
    * Download and open [SQL Server Management Assistant (SSMA) for Access](https://docs.microsoft.com/en-us/sql/ssma/access/sql-server-migration-assistant-for-access-accesstosql?view=sql-server-ver16)
	* Convert all the objects in your MS Access database into object of a newly created empty SQL Server database
	* Add the new ODBC link to the new SQL Server database
	* In your UI/mask/report structure, update any linked table or query to the new data source
	* 🎭 There you go!

#### Finally, connecting multiple times to the same provider

Following for instance this [CodeMaze article](https://code-maze.com/aspnetcore-multiple-databases-efcore/).

* Follow the instructions at the [paragraph above for an existing database](#using-an-existing-database) to scaffold the DbContext and the Models
* Add the new connection string wherever your database connection configuration is stored

> For instance, if you're using the user secrets or a separate json file, it may look like:
> > ```json
> > {
> > "ConnectionStrings": {
> >   "FIRST_DBCONTEXT_NAME": "FIRST_DBCONTEXT_CONNECTION_STRING",
> >   "SECOND_DBCONTEXT_NAME": "SECOND_DBCONTEXT_CONNECTION_STRING"
> >  }
> > }
> ```

* Add the new context in `Program.cs` with something like:
```csharp
builder.Services.AddDbContext<YOURNEWCONTEXTNAME>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("CONNECTIONSTRINGNAME")));
```
* Add the first migration by specifying the context, with `Add-Migration MIGRATIONNAME -Context CONTEXTNAME`
* Remove the content of the `Up` method in the first migration file
* Apply the first migration by using `Update-database -Context CONTEXTNAME`


## Scaffold Razor Pages

(i.e. automatically create CRUD pages)

* Install `Microsoft.VisualStudio.Web.CodeGeneration.Design`
* For each object you wish to scaffold the Razor Pages for:
    * In the Pages folder, add a new subfolder in your project, naming it like the object you want to scaffold (es. _Interventions_)
    * Right-click on the new subfolder and _Add a scaffolded item_
	* Select the _Razor Pages with Entity Framework (CRUD)_ option
	* Select the specified class you wish to scaffold
	* Select the Database Context
	* The scaffolding process creates new files for each object to handle the Index, Create, Edit, Delete an Details features, both in:
    	* `.cshtml` the actual C#-HTML page rendered
		* `.cshtml.cs` the code behind

* In VSCode:
    * `dotnet add package Microsoft.VisualStudio.Web.CodeGeneration.Design`, 
	* then `dotnet tool install --global dotnet-aspnet-codegenerator`
	* then `dotnet aspnet-codegenerator razorpage --model MODELNAME --dataContext DBCONTEXTNAME --relativeFolderPath Pages/MODELNAMEs --referenceScriptLibraries`

* Test the model directly on the web app by running the debugger on IISExpress and going to `http://localhost:PORT/MODELNAMEs`

## A little bit of style

* To play a bit with Bootstrap, you can use the free [Bootswatch](https://bootswatch.com/) themes.
    * Example of CDN link for the [Minty](https://bootswatch.com/minty/) theme: https://www.bootstrapcdn.com/bootswatch/
	* jQuery required: https://cdn.jsdelivr.net/npm/jquery@3.6.0/dist/jquery.min.js

## Building the solution

* ❌ If you ever encounter the error `System.InvalidOperationException : No method 'public static IHostBuilder CreateHostBuilder(string[] args)' or 'public static IWebHostBuilder CreateWebHostBuilder(string[] args)' found on 'AutoGeneratedProgram'. Alternatively, WebApplicationFactory'1 can be extended and 'CreateHostBuilder' or 'CreateWebHostBuilder' can be overridden to provide your own instance.`, it looks like a Visual Studio bug. Just open your `Program.cs` file and launch build from there.