# aws :material-aws:

## AWS CLI

* Installation instructions on Linux:
```bash
$ curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
$ unzip awscliv2.zip
$ sudo ./aws/install
```
For test:
```
$ aws --version
```
* Authenticate the workstation against the AWS API:
    * Create an Access Key in AWS Management Console > User account > Security Credentials > Access Key
    * On AWS CLI, `aws configure`
    * Insert the generated Access Key ID 
    * Insert the corresponding generated Secret Access Key
    * Insert your reference region (using region naming convention)
    

## EC2

### Set up a remote dev environment on an EC2 Debian machine

* Test SSH to remote host: `ssh -i FULL/PATH/TO/PRIVATE/KEYFILE.pem USER@REMOTE-HOSTNAME`
> <kbd>-i</kbd>: A file from which the [identity key (private key)](https://www.ssh.com/academy/ssh/identity-key) for [public key authentication](https://www.ssh.com/academy/ssh/public-key-authentication) is read.
* Configure WSL extension (the ideal one is the [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)) on VSCode (a powerful guide in the [VSCode docs](https://code.visualstudio.com/docs/remote/wsl))
    * Guide: <https://code.visualstudio.com/docs/remote/ssh#_remembering-hosts-you-connect-to-frequently>
    * Reduce permissions on the private key: <https://superuser.com/questions/1296024/windows-ssh-permissions-for-private-key-are-too-open>
* Open and save SSH VSCode workspace
* Forward used ports (`Rails` uses port 3000): `ssh -L 3000:localhost:3000 USER@REMOTE-HOSTNAME`
* Ready to go! :star_struck:

### Remote VSCode over SSH crashes EC2 instance :warning:

The main symptom is that the instance is not reachable via SSH anymore. Using `ssh -v`, the connection hangs with something like

```bash
OpenSSH_7.4p1, LibreSSL 2.5.0
debug1: Reading configuration data /Users/UserName/.ssh/config
debug1: Reading configuration data /etc/ssh/ssh_config
debug1: /etc/ssh/ssh_config line 53: Applying options for *
debug1: Connecting to host.domain [123.456.123.456] port 22.
debug1: Connection established.
debug1: identity file /Users/UserName/.ssh/ke> type 1
debug1: key_load_public: No such file or directory
debug1: identity file /Users/UserName/.ssh/key-cert type -1
debug1: Enabling compatibility mode for protocol 2.0
debug1: Local version string SSH-2.0-OpenSSH_7.4
```

According to [:material-github: this GitHub issue](https://github.com/microsoft/vscode-remote-release/issues/2692), the problem may be related to a [corrupted log file](https://github.com/microsoft/vscode-remote-release/issues/2692#issuecomment-778310041). 

Deleting all `~/.vscode-server/*.log` and `*.pid` files should solve the issue - the deletion apparently has not effect on VSCode Server whatsoever.

For additional troubleshooting, check `~/.vscode-server/data/logs/DATETIME/remoteagent.log` where `DATETIME` is the crashing datetime.


## S3

### Connect your web project with an S3 bucket

* Create your S3 bucket on aws.amazon.com
* In Properties > Permissions > CORS (Cross-Origin Resource Sharing) Configuration, add
```xml
<?xml version="1.0" encoding="UTF-8"?>
<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
<CORSRule>
    <AllowedOrigin>*</AllowedOrigin>
    <AllowedMethod>GET</AllowedMethod>
    <AllowedMethod>POST</AllowedMethod>
    <AllowedMethod>PUT</AllowedMethod>
    <AllowHeader>*</AllowHeader>
</CORSRule>
</CORSConfiguration>
```
Or, in JSON format
```json
[
    {
        "AllowedOrigins": [
            "*"
        ],
        "AllowedMethods": [
            "GET",
            "POST",
            "PUT"
        ],
        "AllowedHeaders": [
                "*"
        ],
    }
]
```
* Go to `IAM > Users` and create a new user selecting `Programmatic Access Type`
* To the same user, in `Set Permissions`, select `Attach existing policies direcly` and choose `AmazonS3FullAccess`
* This will create a special **Access key ID** and **Secret Access Key** that you can copy and paste in your secrets management function