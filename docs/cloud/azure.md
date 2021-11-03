# azure :material-microsoft-azure:

## Resources

* Adam Marczak's [Azure for Everyone](https://www.youtube.com/channel/UCdmEIMC3LBil4o0tjaTbj0w) and especially its [Azure Fundamentals](https://www.youtube.com/playlist?list=PLGjZwEtPN7j-Q59JYso3L4_yoCjj2syrM) playlist
* John Savill's [Azure Masterclass](https://www.youtube.com/playlist?list=PLlVtbbG169nGccbp8VSpAozu3w9xSQJoY)
* The [Azure Fundamentals Learning Path](https://docs.microsoft.com/en-us/learn/paths/az-900-describe-cloud-concepts/) in [Microsoft Learn](https://docs.microsoft.com/en-us/learn/)

## Azure VMs

### Set up a spot Windows Server 2019 VM with the Azure Powershell Module

* Install and import the Azure `Az` Powershell module in the current session
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
