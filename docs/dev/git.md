# git :material-git:

!!! Resources
	* Official documentation in [:material-git: Git docs](https://git-scm.com/docs).
	* [:material-gitlab: Atlassian's tutorials](https://www.atlassian.com/git/tutorials).
	* [:material-youtube: Git for professionals](https://youtu.be/Uszj_k0DGsg) by [FreeCodeCamp](https://www.freecodecamp.org/)
	* [:material-youtube: Advanced Git](https://youtu.be/qsTthZi23VE) by [FreeCodeCamp](https://www.freecodecamp.org/)

## Most used commands

* `git add FILENAME(S)`: it adds the files in "stage", i.e. preparing to commit
* `git commit -m "MESSAGE"`: it does the commit (i.e. basically saving) the staged changes in the local repository 
* `git push`: it pushes the last commit towards the remote repository
* `git pull`: it updates your current HEAD branch with the latest diffs from remote

![git pull](https://girliemac.com/assets/images/articles/2017/12/git-purr.jpg)

### Used branches

* `git branch`: it shows the list of current branches

### Create a new branch:

* `git checkout -b NEWBRANCH` : it moves towards the newly created branch called NEWBRANCH
* Some best practices for naming the new branches [:material-stack-overflow: here](https://stackoverflow.com/questions/273695/what-are-some-examples-of-commonly-used-practices-for-naming-git-branches):
    * Use grouping tokens (words) at the beginning of your branch names. For example: 
		`Test/DESCRIPTION`  : For test branches
		`New/DESCRIPTION`   : For new features branches
		`Bug/DESCRIPTION`	: For bugfixes branches
		`Exp/DESCRIPTION`	: Experimental: for throwaway branch, to be trashed
		`Verified/DESCRIPTION`	: For verified branches, to be merged to main
* `git push --set-upstream origin NEWBRANCH`: it creates the remote branch from the local one, pushing to it as well; as epxlained [here](https://forum.freecodecamp.org/t/push-a-new-local-branch-to-a-remote-git-repository-and-track-it-too/13222)

## Pull from a different remote branch [:material-stack-overflow:](https://stackoverflow.com/questions/9537392/git-fetch-remote-branch)

* Check the remote branches (`git branch -r`) and the local branches (`git branch`)
* Switch to a specified branch (`git switch BRANCH_NAME`)

### Publish a local repo to a new remote repo

:warning: **Requirement**: the remote repo _must_ exist, otherwise it will return the error _Repository not found_

* `git remote add origin https://github.com/.../REPONAME.git`: (right after the first `commit`) it defines the upstream origin. It will ask the credentials:
```
	username: [insert USERNAME]
	password: [insert PERSONAL ACCESS TOKEN]
```
* `git push -u origin master`: pusha il branch master sull'origin, da qui in poi basterà usare `git push`

### Delete an unused branch:

* `git branch --delete|-d BRANCHNAME` : it deletes the local branch BRANCHNAME
* `git push -d origin BRANCHNAME` : it deletes the remote branch BRANCHNAME

### Move to an existing local branch:

* `git checkout DESTINATIONBRANCH`: it moves the tracking to the local branch DESTINATIONBRANCH

### Merge a branch

Sample procedure:

* `git checkout -b NEW-FEATURE main` : Start a new feature by creating the branch NEW-FEATURE from MAIN
* `git add <file>`: add a new file in the feature
* `git commit -m "Start a feature"`: commit the edit
* `git checkout main`: move to main
* `git merge NEW-FEATURE`: merge the branch into main
* `git branch -d NEW-FEATURE`: delete the branch
* `git push`: sync with remote repo

!!! warning
	If you get the `not something we can merge` error, it's probably because you don't have a local copy of the branch that you want to merge, as explained [:material-stack-overflow: here](https://stackoverflow.com/questions/16862933/how-to-resolve-gits-not-something-we-can-merge-error). Go on with:
	```
	git checkout BRANCH-NAME
	git checkout main
	git merge BRANCH-NAME
	```

## Switch remote URLs from HTTPS to SSH

From your local project folder,
```
$ git remote -v
> origin  https://github.com/USERNAME/REPOSITORY.git (fetch)
> origin  https://github.com/USERNAME/REPOSITORY.git (push)
```
Set
```
git remote set-url origin git@github.com:USERNAME/REPOSITORY.git
```
Then verify that the remote URL has changed:
```
$ git remote -v
# Verify new remote URL
> origin  git@github.com:USERNAME/REPOSITORY.git (fetch)
> origin  git@github.com:USERNAME/REPOSITORY.git (push)
```

## .gitignore

* Compile your `\.gitignore` file to prevent git from tracking files. Sample file:
```
*.exe						# Ignore _all_ exe files
.virtualenvironment/		# Ignore the folder .virtualenvironment and its whole content
```

* Make git forget about a file that's been tracked since now:
	* `git rm --cached <file>` - for the single file
	* `git rm -r --cached <folder>` - for a whole folder and all files in it recursively
	The removal of the file from the head revision will happen on the next commit.
	:warning: **Warning:** While this will not remove the physical file from your local, it will remove the files from other developers machines on next git pull
  
## Misc.

* Additional stuff:
`git gui`: it opens the integrated git GUI
`gitk`: it opens the commit viewer di Git

* Just reinstall git:
```
sudo apt-get purge git
sudo apt-get autoremove
sudo apt-get install git
```
