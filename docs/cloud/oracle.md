# oracle cloud 

!!! Resources
    * [Launch Always Free Resources with Terraform](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources_Launching.htm)
    * [Oracle Cloud Free Tier](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier.htm)
    * [Oracle Cloud Always Free Resources](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm)

* Install with interactive installation
```bash
sudo bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)" 
```
While responding to the [installation prompts](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm#InstallingCLI__PromptsInstall), keep all the installed files and folders in the same path (e.g. your `$HOME`) for consistency.
Test your installation:
```bash
oci --version
```
* Configure the CLI with `oci setup config`; the prompts will ask for 
    * your `.oci/config` file location
    * your [user's OCID, tenancy's OCID, API Key fingerprint and region](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.htm#five)
* Test the connection with
```bash
oci os ns get   # It returns the tenancy's namespaces
```

!!! error
    Troubleshoot the `NotAuthenticated` error with [this blog post](https://realtrigeek.com/2020/04/25/oracle-cloud-infrastructure-oci-cli-notauthenticated-error/).

* Get the list of compartments with
```bash
oci iam compartment list
```

!!! info
    The output of the CLI are JSON records (readability is improved using `--output table`). Save them in a variable with `VARIABLENAME=$(oci ...)` then parse them in bash with [jq](https://stedolan.github.io/jq/) using `echo $VARIABLENAME | jq '.'`

Get the list of compartments' OCIDs:
```bash
COMPARTMENTS=$(oci iam compartment list)
echo $COMPARTMENTS > compartments.json
cat compartments.json | jq -r '.data[].id'
```

* Get the list of available instance shapes ([reference](https://docs.oracle.com/en-us/iaas/tools/oci-cli/3.4.1/oci_cli_docs/cmdref/compute/shape/list.html))
```
oci compute shape list --compartment-id COMPARTMENT-ID
```
