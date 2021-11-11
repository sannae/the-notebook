# github :material-github:

## Setup connection with GitHub

### Create a [Private SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

* Create a SSH key with:
```
ssh-keygen -t ed25519 -C "your_email@example.com"
```
* Start the SSH agent:
```
eval "$(ssh-agent -s)"
```
* Add your SSH private key to your SSH agent (replace `id_ed25519` if different):
```
ssh-add ~/.ssh/id_ed25519 
```
Then [https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account]

Then test

## Github Actions

## Github API
