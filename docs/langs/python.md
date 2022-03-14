# Python

!!! Resources
    * Setting up Python 3.x in [VS Code](https://code.visualstudio.com/docs/python/python-tutorial)

## Package management

About [package management](https://docs.python.org/3/installing/index.html)

* `py -m pip install --upgrade pip` : it installs and upgrades pip
* `py -m pip install MODULE`: it installs the required module

## Creating and using virtual environments

About [virtual environments](https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments)

* `py -m venv .VIRTUALENVIRONMENTNAME`: it creates/uses the virtual environment specified in the path, then selectable in the terminal
* `py -m deactivate`: it destroys the current virtual environment

## Requirements

* `py -m pip freeze > requirements.txt`: it prints a file called _requirements_ with all the package necessary to the current project (they can be retrieved by the command `py -m pip install -r requirements.txt`)

## Inheritance

About [inheritance](https://docs.python.org/3/tutorial/classes.html#inheritance)

## Testing

### Using [Selenium](https://www.selenium.dev/) and [ChromeDriver](https://chromedriver.chromium.org/)

* [:material-stack-overflow:](https://stackoverflow.com/a/44698744) Download and install Chrome 

```bash
# Setup key
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -

# Setup repository
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
sudo apt-get update 
sudo apt-get install google-chrome-stable
```

* Install Selenium and [:material-github: `webdriver_manager`](https://github.com/SergeyPirogov/webdriver_manager) (this last one will take care of installing and updating the right version on the chromedriver, regardless of the local version of Google Chrome)
```bash
pip install selenium
pip install webdriver_manager
```

* In your Python script, add
```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
```

* To silence the webdriver, use
```python
# Shut webdriver manager logs up
os.environ['WDM_LOG_LEVEL'] = '0'
```

* To set up a browser session:
```python
chrome_options = Options()
chrome_options.add_argument("--headless") # Means with no interface
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
```
To close the session after the tests:
```python
browser.quit()
```