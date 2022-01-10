# oracle cloud 

!!! Resources
    * [Launch Always Free Resources with Terraform](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources_Launching.htm)
    * [Oracle Cloud Free Tier](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier.htm)
    * [Oracle Cloud Always Free Resources](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm)

## Installation

Install with interactive installation:
```bash
sudo bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)" 
```
While responding to the [installation prompts](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm#InstallingCLI__PromptsInstall), keep all the installed files and folders in the same path (e.g. your `$HOME`) for consistency.

Test your installation:
```bash
oci --version
```

Configure the CLI with `oci setup config`; the prompts will ask for 
    * your `.oci/config` file location
    * your [user's OCID, tenancy's OCID, API Key fingerprint and region](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.htm#five)

Test the connection with
```bash
oci os ns get   # It returns the tenancy's namespaces
```

!!! error
    Troubleshoot the `NotAuthenticated` error with [this blog post](https://realtrigeek.com/2020/04/25/oracle-cloud-infrastructure-oci-cli-notauthenticated-error/).

## Check shape availability

Get the list of compartments with
```bash
oci iam compartment list
```

!!! info
    The output of the CLI are JSON records (readability is improved using `--output table`). Save them in a variable with `VARIABLENAME=$(oci ...)` then parse them in bash with [jq](https://stedolan.github.io/jq/) using `echo $VARIABLENAME | jq '.'`

Get the list of compartments' OCIDs into an array:

```bash
COMPARTMENTS=$(oci iam compartment list)
echo $COMPARTMENTS > compartments.json
COMPARTMENTS_OCID=$(cat compartments.json | jq -r '.data[].id')
COMPARTMENT_ARRAY=($(echo $COMPARTMENTS_OCID | tr " " "\n"))
```

You can access them with a `for` loop like:

```bash
for compartment_ocid in "${COMPARTMENT_ARRAY[@]}"
do
    echo $compartment_ocid
done
```

Using the same `for` loop as above, get the list of available instance shapes ([reference](https://docs.oracle.com/en-us/iaas/tools/oci-cli/3.4.1/oci_cli_docs/cmdref/compute/shape/list.html)). The `grep` part is used to check if a specific shape is available in each compartment:

```bash
for compartment_ocid in "${COMPARTMENT_ARRAY[@]}"
do
    SHAPE=$(oci compute shape list --compartment-id $compartment_ocid | grep "VM.Standard.A1.Flex")
    # Check if shape is available
    if [ -z "$SHAPE" ]
    then
        echo "No shape found in compartment $compartment_ocid"
    else
        echo $SHAPE
    fi
done
```

:green_circle: **Next:** create a .NET worker service with the [.NET SDK](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/dotnetsdk.htm) (documentation also available [:material-github: here](https://github.com/oracle/oci-dotnet-sdk))