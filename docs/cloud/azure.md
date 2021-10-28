# azure

## Azure VMs

### Set up a Windows Server VM

* Install and import the Azure Powershell module in the current session
```powershell
Install-Module -Name Az -Force -Verbose
Import-Module -Name Az
```
* Connect to your Azure subscription using the browser
```powershell
Connect-AzAccount
```
* Create the Resource Group and the VM; remember to set the `$region` and the `$user` variables. The password is prompted interactively.
```powershell
$ResourceGroup = 'dev-test'
$region = 'westeurope'
$passwd = ConvertTo-SecureString $(Read-Host "Password") -AsPlainText -Force
$Credential = New-Object System.Management.Automation.PSCredential ($user, $passwd);
New-AzResourceGroup -Name $ResourceGroup -Location $region -Verbose
New-AzVM -ResourceGroupName $ResourceGroup -Location $region -Name $ResourceGroup -Image Win2019Datacenter -Credential $Credential -Priority Spot -Verbose
```