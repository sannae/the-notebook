# git
Official documentation in https://git-scm.com/docs.
Atlassian's tutorials in https://www.atlassian.com/git/tutorials

## Most used commands
`git add FILENAME(S)`: it adds the files in "stage", i.e. preparing to commit
`git commit -m "MESSAGE"`: it does the commit (i.e. basically saving) the staged changes in the local repository 
`git push`: it pushes the last commit towards the remote repository

### Used branches
`git branch`: it shows the list of current branches

### Create a new branch:
`git checkout -b NEWBRANCH` : it moves towards the newly created branch called NEWBRANCH
* Some best practices for naming the new branches [here](https://stackoverflow.com/questions/273695/what-are-some-examples-of-commonly-used-practices-for-naming-git-branches):
1. Use grouping tokens (words) at the beginning of your branch names.
   1. For example: 
		`Test/DESCRIPTION`  : For test branches
		`New/DESCRIPTION`   : For new features branches
		`Bug/DESCRIPTION`	: For bugfixes branches
		`Exp/DESCRIPTION`	: Experimental: for throwaway branch, to be trashed
		`Verified/DESCRIPTION`	: For verified branches, to be merged to main
`git push --set-upstream origin NEWBRANCH`: crea il branch remoto da quello locale ed effettua il push in esso 
	(Spiegazione: https://forum.freecodecamp.org/t/push-a-new-local-branch-to-a-remote-git-repository-and-track-it-too/13222)

### Pubblica un repo locale nuovo su un nuovo repo remoto
**Prerequisito**: il repo remoto deve esistere, altrimenti restituisce l'errore _Repository not found_
Subito dopo il `commit`:
`git remote add origin https://github.com/.../REPONAME.git`: definisce l'origin upstream
Chiederà le credenziali:
	username: [inserire USERNAME]
	password: [inserire PERSONAL ACCESS TOKEN]
`git push -u origin master`: pusha il branch master sull'origin, da qui in poi basterà usare `git push`

### Per cancellare un branch (non in uso):
`git branch --delete|-d BRANCHNAME` : cancella il branch LOCALE indicato da BRANCHNAME
`git push -d origin BRANCHNAME` : cancella il branch REMOTO indicato da BRANCHNAME

### Per spostarsi su un branch esistente:
`git checkout DESTINATIONBRANCH`: sposta il branch attuale su branch DESTINATIONBRANCH

### Per mergiare un branch
Procedura di esempio:
`git checkout -b NEW-FEATURE main` : Start a new feature by creating the branch NEW-FEATURE from MAIN
`git add <file>`: add a new file in the feature
`git commit -m "Start a feature"`: commit the edit
`git checkout main`: move to main
`git merge NEW-FEATURE`: merge the branch into main
`git branch -d NEW-FEATURE`: delete the branch
`git push`: sync with remote repo

## .gitignore
* Compile your `\.gitignore` file to prevent git from tracking files
  File di esempio:
	*.exe						% Ignore _all_ exe files
	.virtualenvironment/		% Ignore the folder .virtualenvironment and its whole content
* Make git forget about a file that's been tracked since now:
	`git rm --cached <file>` - for the single file
	`git rm -r --cached <folder>` - for a whole folder and all files in it recursively
	The removal of the file from the head revision will happen on the next commit.
	**WARNING:** While this will not remove the physical file from your local, it will remove the files from other developers machines on next git pull
  
## Misc.
`git gui`: apre la GUI integrata di git
`gitk`: apre il commit viewer di Git
