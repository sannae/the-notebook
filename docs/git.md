# git
Official documentation in [https://git-scm.com/docs](https://git-scm.com/docs).
Atlassian's tutorials in [https://www.atlassian.com/git/tutorials](https://www.atlassian.com/git/tutorials).

## Most used commands
* `git add FILENAME(S)`: it adds the files in "stage", i.e. preparing to commit
* `git commit -m "MESSAGE"`: it does the commit (i.e. basically saving) the staged changes in the local repository 
* `git push`: it pushes the last commit towards the remote repository

### Used branches
* `git branch`: it shows the list of current branches

### Create a new branch:
* `git checkout -b NEWBRANCH` : it moves towards the newly created branch called NEWBRANCH
* Some best practices for naming the new branches [here](https://stackoverflow.com/questions/273695/what-are-some-examples-of-commonly-used-practices-for-naming-git-branches):
    * Use grouping tokens (words) at the beginning of your branch names. For example: 
		`Test/DESCRIPTION`  : For test branches
		`New/DESCRIPTION`   : For new features branches
		`Bug/DESCRIPTION`	: For bugfixes branches
		`Exp/DESCRIPTION`	: Experimental: for throwaway branch, to be trashed
		`Verified/DESCRIPTION`	: For verified branches, to be merged to main
* `git push --set-upstream origin NEWBRANCH`: it creates the remote branch from the local one, pushing to it as well; as epxlained [here](https://forum.freecodecamp.org/t/push-a-new-local-branch-to-a-remote-git-repository-and-track-it-too/13222)

### Publish a local repo to a new remote repo
**Requirement**: the remote repo _must_ exist, otherwise it will return the error _Repository not found_
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
`git gui`: it opens the integrated git GUI
`gitk`: it opens the commit viewer di Git
