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

* Go on **Your GitHub profile > Your repo > Settings > Actions > Runners > New self-hosted runner**
* Choose your OS (macOS, Linux, Windows) and architecture
* `cd` in the path where you will store the runner
* Download the runner with
```bash
# Create a folder
$ mkdir actions-runner && cd actions-runner
# Download the latest runner package
$ curl -o actions-runner-linux-x64-2.284.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.284.0/actions-runner-linux-x64-2.284.0.tar.gz
# Optional: Validate the hash
$ echo "1ddfd7bbd3f2b8f5684a7d88d6ecb6de3cb2281a2a359543a018cc6e177067fc  actions-runner-linux-x64-2.284.0.tar.gz" | shasum -a 256 -c
# Extract the installer
$ tar xzf ./actions-runner-linux-x64-2.284.0.tar.gz
```
* Configure the runner with:
```bash
# Create the runner and start the configuration experience
$ ./config.sh --url https://github.com/<YOUR_USERNAME>/<YOUR_REPOSITORY> --token <YOUR_TOKEN>
# Last step, run it!
$ ./run.sh
```
When the runner is actually running, you will see it with the **:green-circle: Idle** label in **Settings > Actions > Runner**.

#### [:material-github:]() Configure your runner as a service

In the runner folder (`actions-runner`), 

* Stop the runner if it is running
* Install the service with
```bash
sudo ./svc.sh install
```
* Start the service with
```bash
sudo ./svc.sh start
```
* Check the service status with
```bash
sudo ./svc.sh status
```

#### [:material-github:](https://docs.github.com/en/actions/hosting-your-own-runners/using-self-hosted-runners-in-a-workflow) Use the self-hosted runner in a workflow

To use the runner, add in your `.github/workflows/WORFLOW_NAME.yml` file:
```yaml
# Use this YAML in your workflow file for each job
runs-on: self-hosted
```

### Define a workflow

#### Generic env variables

* `${GITHUB_WORKSPACE}`: the project root folder (i.e. the one containing the `.github\workflows` subfolder)
* `${{ github.event.repository.name }}`: the project name, in our case `the-notebook`
* `${{ github.repository_owner }}`: the repository owner, in our case `sannae` (i.e. myself!)


#### Use the secrets as env variables

Once you've defined a GitHub Secret, you can access it in your workflow as an environment variable from the step/job/workflow scope:

```yaml
      - name: Your step name

        # Define an environment variable ACCESS_TOKEN 
        # whose value is read from the GitHub Secret with the same name
        env:
          ACCESS_TOKEN: "${{ secrets.ACCESS_TOKEN }}"
        run: python3 ${GITHUB_WORKSPACE}/scripts/lang-tracker.py
```

In the example above, the script `lang-tracker.py` is able to see the environment variable with the `os.environ[]` function:

```python
g = Github(os.environ['ACCESS_TOKEN'])
```


## Github API

### Test the API via console (using `curl`)

#### Details of the user:

```bash
user=$"YOUR-GITHUB-USERNAME"
token=$"YOUR-GITHUB-PERSONAL-ACCESS-TOKEN"
curl -i -u "$user:$token" https://api.github.com/users/$user`
```
The switch `-i` will display also the HTTP headers: notice the `content-type` header (it should be `application/json`) and the `x-ratelimit-limit` header (maximum amount of available request per hour, it should be 5000 for authenticated requests - usage is tracked by the `x-ratelimit-remaining`).

#### Details of the user's repos (both public and private):

```bash
user=$"YOUR-GITHUB-USERNAME"
token=$"YOUR-GITHUB-PERSONAL-ACCESS-TOKEN"
curl -i -H "Authorization: token $token" https://api.github.com/users/$user/repos
```

#### Details of a specific repo

```bash
user=$"YOUR-GITHUB-USERNAME"
token=$"YOUR-GITHUB-PERSONAL-ACCESS-TOKEN"
repo=$REPO_NAME
curl -i -H "Authorization: token $token" https://api.github.com/repos/$user/$repo
```

#### Commits of a specific repo

```bash
user=$"YOUR-GITHUB-USERNAME"
token=$"YOUR-GITHUB-PERSONAL-ACCESS-TOKEN"
repo=$REPO_NAME
curl -i -H "Authorization: token $token" https://api.github.com/repos/$user/$repo/commits
```

#### Language statistics of a specific repo

```bash
user=$"YOUR-GITHUB-USERNAME"
token=$"YOUR-GITHUB-PERSONAL-ACCESS-TOKEN"
repo=$REPO_NAME
curl -i -H "Authorization: token $token" https://api.github.com/repos/$user/$repo/languages
```

### Calling the API with [:material-github: PyGithub](https://github.com/PyGithub/PyGithub)

Simply install with
```bash
pip install PyGithub
```

Then use it by calling all the supported Github objects:
```python
from github import Github

g = Github("YOUR_ACCESS_TOKEN_HERE")

for repo in g.get_user().get_repos():
  print(repo_name)
```
