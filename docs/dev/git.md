# git :material-git:

!!! Resources
	* Official documentation in [:material-git: Git docs](https://git-scm.com/docs).
	* [:material-gitlab: Atlassian's tutorials](https://www.atlassian.com/git/tutorials).
	* [:material-youtube: Git for professionals](https://youtu.be/Uszj_k0DGsg) by [FreeCodeCamp](https://www.freecodecamp.org/)
	* [:material-youtube: Advanced Git](https://youtu.be/qsTthZi23VE) by [FreeCodeCamp](https://www.freecodecamp.org/)


## Theory

Git is:
* a persistent map
* a 'stupid' content tracker
* a revision control system
* a distributed revision control system

There are four basic objects in Git's object database:
* blobs: hashes of files
* trees: files containing references to other trees or blobs
* commits: files containing references to blobs or trees
* annotated tags: files containing references to commits

The four areas:
* Stash: temporary storage area
* Working area: the project directory on the local file system
* Staging index: aka Cached, contained in .git/index
	* It's a binary file, it cannot be opened
* Repository: contained in .git/objects and in more folders
	* It's made of immutable objects, they can be created or deleted but not changed

## Plumbing commands

### git hash-object

> Returns the hash (20 hex bytes) of a file 
> if two files have the same content, they will have the same hash
git hash-object readme.md

> Get the hash of a file and save it into .git/objects/NN/MMMMM...
> NN are the first two digits of the hash
> MMMMM.. are the following 38 digits of the hash
readme.md | git hash-object --stdin --write

### git cat-file

> Prints the type of the file 
> There are 4 types in the object database: blobs, trees, commits, annotated tags) from its hash
git cat-file 23b40d196e0a4b81637b255c945feab0084f5f88 -t

> Prints the content of a file from its hash
git cat-file 23b40d196e0a4b81637b255c945feab0084f5f88 -p

### git show-ref

> Lists all the references of the current commit containing the string 'main'
> It returns both the local and the remote references
git show-ref main

### git count-objects


## Porcelain commands

### git status

> Gives the current status of the changes across the four areas
> "Nothing to commit, working tree clean" is referred to as 'Clean Status'
git status

### git add

> Moves a file from the working area to the staging index
> "Changes not staged for commit" are changes only present in the working area
git add readme.md

### git rm

> Removes a file from index, keeping it in the working area
> It doesn't have any effect on the repository area
git rm --cached readme.md

> Removes a file from the index and the working area, effectively deleting the file
> It doesn't have any effect on the repository area
git rm -f readme.md

### git mv

> It renames a file in the working area, then adds it to staging index and removes the old file from the staging index
> It's basically the same as:
>   mv readme.txt readme.md
>   git add readme.md
>   git rm readme.txt
git mv readme.txt readme.md

### git commit 

> Creates a 'commit', i.e. a new file in .git/objects/NN/MMMMM.. 
> The file contains the root of the project ('tree'), author and date, message
> It basically contains the reference to blobs or trees
> It also moves the staged files from the index to the repository
git commit -m "This is a commit"

### git branch

> Get the current branch
> A branch is a reference to a commit
> It basically reads the content of .git/HEAD
> HEAD is our current position 
git branch

> Creates a new file in .git/refs/heads/NEW_BRANCH pointing to the current commit
git branch NEW_BRANCH

### git switch

> Moves HEAD to the commit referenced by NEW_BRANCH
> Restores the state of the working directory to the commit we're pointing
git switch NEW_BRANCH

### git checkout 

> Moves HEAD to the commit referenced by NEW_BRANCH
> Restores the state of the working directory to the commit we're pointing
> May set commits into 'detached head' status: they then will be garbage-collected
> It also copies the content of the repository into the staging index and the working area
git checkout NEW_BRANCH

### git merge

> Merges branch NEW_BRANCH into current branch
> The merge commit will have two commit parents
git merge NEW_BRANCH

### git rebase

> Rearranges the branches so that they look one single branch
> Being HEAD on NEW_BRANCH, rebases NEW_BRANCH on top of main
> Basically it detaches all the commits after the last common commit and reattaches them on top of the destination branch
git rebase main

### git tag

> Sets the simple tag (i.e. with no metadata) 'release_1' to the current commit
> The tag is saved in .git/refs/tags/release_1
> It only contains the reference to the commit
git tag release_1

> Sets an annotated tag (i.e. with metadata) 'release_1' to the current commit
> The tag is saved in .git/refs/tags/release_1
> It contains the reference to the commit, the tagger, the date and the message
git tag release_1 -a -m "First release"

> Lists all the tags
git tag

> Checks out the commit with the specific tag 'release_1'
git checkout 'release_1'

### git pull

> Synchronizes the local changes with the remote changes
> It's a combination of `git fetch` and `git merge`
git pull

> In case of conflicts:
> Force the local push: the remote commit gets detached and garbage-collected
git push -f

> In case of conflicts:
> Resolve conflicts locally

### git push

> Synchronizes the remote changes with the local changes
git push

### git reset 

> Moves the current branch to a different commit, without moving the HEAD reference
> And copies content of the current commit from the repository to the staging index
git reset [--mixed] 23b40d196e0a4b81637b255c945feab0084f5f88

> Copies the content of the current commit from the repository into the working area and staging index
git reset --hard 23b40d196e0a4b81637b255c945feab0084f5f88

> Just moves the branch to the new commit
git reset --soft 23b40d196e0a4b81637b255c945feab0084f5f88

### git log

> Commit history in reversed chronological order
git log

> Last commit
git log -1

> Log in short format
git log --oneline

> Detailed commit history
git log --stat

> Super-detailed commit history, with diff
git log --patch

### git stash

> Moves the uncommitted changes (staged and unstaged) to the stash area
> Stashed objects are identified by `stash@{N}` number, where `{0}` is always the most recent one
> It doesn't include the untracked files
git stash

> Moves the uncommitted changes to the stash area, including the untracked files
git stash --include-untracked

> List everything in the stash area
git stash list

> Applies the most recent stashed changes to the working area, removing it from the stash
git stash pop

> Applies the most recent stashed changes to the working area, while keeping it in the stash
git stash apply

> Applies the stash element identified by the `stash@{2}`, keeping it in the stash
git stash apply stash@{2}

> Deletes all elements in the stash
git stash clear

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
