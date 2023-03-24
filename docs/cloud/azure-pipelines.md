# azure pipelines

## Build and publish a build task

### Requirements:

* An organization in Azure DevOps, with a project and a pipeline
* NodeJS, last release (check with `node -v`), >= 10.x
* TypeScript compiler >= 2.2.0
* `tfs-cli` (Cross-platform CLI for Azure DevOps)
    * `npm install -g tfx-cli`
* A `home` folder for the project, it will contain:
```
/readme.md      # readme
/images
  /extension-icon.png   # task's icon
/BuildAndReleaseTaskName    # Folder containing the task and all its scripts
  /...
/vss-extension.json     # task's manifest
```

### Scaffold the task

* Create a home folder for the project (e.g. `BuildAndReleaseTaskName`)
* Create the subfolder containing the task itself (you may call it the same as the home folder), and `cd` into it
* Install the dependencies:
    * `npm init`: creates the *packages.json* file, answer the prompt interactively
    * `npm install azure-pipelines-task-lib --save`: package for Azure Pipelines
    * `npm install @types/node --save-dev`: types definition for nodejs, only dev environment
    * `npm install @types/q --save-dev`: types definition for Q,only dev environment
* `echo node_modules > .gitignore` to ignore the `node_modules/` folder
    * It doesn't make any sense to bring everywhere all the packets, you can always restore them from the packages.json file
    * It would also increase significantly the repository size
* Install and setup TypeScript
    * `npm install -g typescript`: installing TypeScript, globally
    * `tsc --init`: creating the *tsconfig.json* file

### Create the task

* Create the *task.json* file
* Copy the *task.json* template from [here](https://github.com/jc566/Youtube_Solutions/blob/master/AzureDevOps_CustomTasks/Etc/Part1/task-json-schema.json), also copied below in case of dead link:
```json
{
    "$schema": "https://raw.githubusercontent.com/Microsoft/azure-pipelines-task-lib/master/tasks.schema.json",
    "id": "{{taskguid}}",
    "name": "{{taskname}}",
    "friendlyName": "{{taskfriendlyname}}",
    "description": "{{taskdescription}}",
    "helpMarkDown": "",
    "category": "Utility",
    "author": "{{taskauthor}}",
    "version": {
        "Major": 0,
        "Minor": 1,
        "Patch": 0
    },
    "instanceNameFormat": "Echo $(samplestring)",
    "inputs": [
        {
            "name": "samplestring",
            "type": "string",
            "label": "Sample String",
            "defaultValue": "",
            "required": true,
            "helpMarkDown": "A sample string"
        }
    ],
    "execution": {
        "Node10": {
            "target": "index.js"
        }
    }
}
```
* Replace the placeholders with your values:
    * `"id"`: a unique GUID for your task, if needed use [guidgen.com](https://www.guidgen.com/), a web version of the GuidGen tool from Microsoft
    * `"name"`: name without spaces
    * `"friendlyname"`: descriptive name, it may include spaces
    * `"description"`: detailed description about what the task is doing
    * `"author"`: short string describind the author
    * `"instanceNameFormat"`: it describes how the task will be viewed in the tasks list from the build/release pipeline
        * You may also use a variable name with `$(variablename)`
    * `"groups"`: it describes the items where the logical properties of the task can be grouped
    * `"inputs"`: inputs necessary to the task's execution
    * `"execution"`: execution options for the task, including scripts 
* Create the *index.ts* file and fill it with the template available [here](https://github.com/jc566/Youtube_Solutions/blob/master/AzureDevOps_CustomTasks/Etc/Part1/index-js-schema.ts), also reference for dead link:
```javascript
import tl = require('azure-pipelines-task-lib/task');

async function run() {
    try {
        const inputString: string | undefined = tl.getInput('samplestring', true);
        if (inputString == 'bad') {
            tl.setResult(tl.TaskResult.Failed, 'Bad input was given');
            return;
        }
        console.log('Hello', inputString); // It just prints Hello followed by the input string
    }
    catch (err) {
        tl.setResult(tl.TaskResult.Failed, err.message);
    }
}

run();
```
* Compile the TypeScript files into Javascript:
    * `tsc`: it basically build the current project, i.e. the *tsconfig.json* in the local folder
* Test the task with PowerShell: from the root folder run `node index.js`
    * Using the template above, it will return the error `Input required:  samplestring`
    * Create the input samplestring with an environment variable
        * `$env:INPUT_SAMPLESTRING=whoever_you_are`
    * Run the task again: this time it will print `"Hello whoever_you_are"` 

### Package the task

* In the home folder, create the subfolder `images` and add the task icon, naming it `extension-icon.png` (128x128)
* Create the file *vss-extension.json* using the template [here](https://github.com/jc566/Youtube_Solutions/blob/master/AzureDevOps_CustomTasks/Etc/Part1/vss-extension-json-schema.json):
```json
{
    "manifestVersion": 1,
    "id": "build-release-task",
    "name": "Fabrikam Build and Release Tools",
    "version": "0.0.1",
    "publisher": "fabrikam",
    "targets": [
        {
            "id": "Microsoft.VisualStudio.Services"
        }
    ],    
    "description": "Tools for building/releasing with Fabrikam. Includes one build/release task.",
    "categories": [
        "Azure Pipelines"
    ],
    "icons": {
        "default": "images/extension-icon.png"        
    },
    "files": [
        {
            "path": "buildAndReleaseTask"
        }
    ],
    "contributions": [
        {
            "id": "custom-build-release-task",
            "type": "ms.vss-distributed-task.task",
            "targets": [
                "ms.vss-distributed-task.tasks"
            ],
            "properties": {
                "name": "buildAndReleaseTask"
            }
        }
    ]
}
```
* Replace the `"publisher"` with your publisherId
    * You may create a new publisherId from your [publisher page in the Visual Studio Marketplace](marketplace.visualstudio.com/manage/createpublisher?managePageRedirect=true)
    * You just need to enter Name and PublisherId, everything else is optional
* Replace also `"name"`, `"description"`, `"files"`/`"path"` and `"contributions"`/`"properties"`/`"name"`
* Package the extension using the Azure DevOps TFS CLI:
    * `tfs extension create --manifest-globs vss-extension.json`
* The file `{publisherId}.{extension_Id}.{extension_version}.vsix` will appear, containing your packaged extension! 🎉

### Publish the task

* Publish and share the extension
    * Using the portal:
        * Back to the Visual Studio Marketplace portal > go to [Manage Publisher & Extensions](https://marketplace.visualstudio.com/manage/publishers/PUBLISHER_ID) 
        * New extension > Azure DevOps
        * Upload your vsix file
        * Once the upload is finished, there will be an automatic check
        * The extension will be uploaded on the marketplace as Private by default
            * Obviously, it can be made Public at any time
    * Using Powershell:
        * Get the OrganizationName (including *dev.azure.com/*)
        * Create a Personal Access Token from Azure DevOps
            * Azure DevOps > User settings > Personal Access Tokens > New Token
        * Share the extension
            * `tfx extension publish --manifest-globs vss-extension.json --share-with dev.azure.com/ORGANIZATION_NAME`
            * It will prompt you for the Personal Access Token
            * It will validate the extension and give you a feedback from your shell session
* On Azure DevOps, go to Organization Settings > Extensions > Shared
    * Select the shared extension and click on Install
        * The extension will appear among the Installed ones

### Use your task

* In Azure DevOps, go to your build/release pipeline
* Add task > you can search for it by using the `"name"` parameter in the *task.json* file used to publish