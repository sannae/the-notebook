# aws :material-aws:

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