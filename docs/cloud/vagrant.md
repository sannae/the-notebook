# vagrant

## Initialization errors

* :warning: When you `vagrant up BOX_NAME`
    * you may get the error `The "metadata.json" file for the box 'BOX_NAME' was not found.`. As per [:material-stack-overflow: this post], you need to:
    ```bash
    cd ~/.vagrant.d/boxes
    rm -f BOX_NAME
    ```
    * If you get `A Vagrant environment or target machine is required to run this command.`... you're just not in the correct path! `cd` into  your `vagrantfile` folder.