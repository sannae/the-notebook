# dotnet [:material-dot-net:]

!!! Resources
    * [:material-microsoft: Create Microservices with .NET](https://docs.microsoft.com/en-us/learn/paths/create-microservices-with-dotnet/) Microsoft Learn learning path
    * [:material-youtube: C# 101]
    * [:material-youtube: .NET Core 101]
    
## Random notes

* Create a new project by using `dotnet new TEMPLATE_NAME -o FOLDER_NAME` (the `FOLDER_NAME` will be created in the local path). `TEMPLATE_NAME` may assume the following values:
```bash
dotnet new console      # Console application template
dotnet new mvc          # ASP.NET Core MVC application template
dotnet new worker       # Worker Service application template
```
and so on
* The project main manifest is a file called `PROJECTNAME.csproj` and it looks like:
```xml
<Project Sdk="<NAME-OF-THE-SDK">
  <PropertyGroup>
    <TargetFramework>net6.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <!-- Other properties -->
  </PropertyGroup>
</Project>
```
Basically it contains the information needed to build the project.

* To build and run your application, use `dotnet run` in your project folder. The command will automatically build the project. 

* To activate a watcher and dynamically reloading the web page while editing the source file, use `dotnet watch run`