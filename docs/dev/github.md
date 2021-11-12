# github :material-github:

### Getting started 

### [:material-github:]((https://docs.github.com/en/authentication/connecting-to-github-with-ssh)) Setup SSH connection with GitHub

When you set up SSH, you will need to generate a new SSH key and add it to the ssh-agent. You must add the SSH key to your account on GitHub before you use the key to authenticate.

#### Check for existing keys

First of all, check if there is any existing key supported by GitHub:
```bash
ls -al ~/.ssh | grep -E 'id_rsa.pub|id_ecdsa.pub|id_ed25519.pub' 
```

#### Create a new key

If no supported key is available, create a SSH key with:
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```
It will prompt you for a secure passphrase. Then start the SSH agent:
```bash
eval "$(ssh-agent -s)"
```
and add your SSH private key to your SSH agent (replace `id_ed25519` if different). This ensure you won't have to reenter your passphrase every time you use your SSH key.
```bash
ssh-add ~/.ssh/id_ed25519
```
Add your newly created SSH key to your GitHub account from the browser, by copying the _whole_ content of `cat ~/.ssh/id_ed25519.pub` (replace `ed25519` if different) in **Your GitHub profile > Settings > SSH and GPG keys > New SSH key**, giving it a Title and confirming with **Add SSH key**

#### Test your SSH connection

Test your connection with `ssh -T git@github.com`. A successful response should be like:
```
Hi USERNAME! You've successfully authenticated, but GitHub does not provide shell access.
```

!!! danger
    If it doesn't work, troubleshoot the [:material-github: **Error: permission denied (publickey)**](https://docs.github.com/en/authentication/troubleshooting-ssh/error-permission-denied-publickey) error.

## Github Actions

### Set up a self-hosted runner

#### [:material-github:](https://docs.github.com/en/actions/hosting-your-own-runners/adding-self-hosted-runners) Add a self-hosted runner on your repository

## Github API
