# Ruby on Rails :material-language-ruby-on-rails:

??? Resources
    * [:material-youtube: Ruby on Rails for beginners](https://youtube.com/playlist?list=PLm8ctt9NhMNV75T9WYIrA6m9I_uw7vS56)
    * [:material-youtube: Let's build with Ruby on Rails](https://youtube.com/playlist?list=PL01nNIgQ4uxNkDZNMON-TrzDVNIk3cOz4) :star:

## Set up your dev environment

There are several good instllation guides online, such as [GoRails](https://gorails.com/setup/windows/10) and [Seriva's WSL2 Rails setup](https://github.com/serivas/wsl2_rails_setup).

* Update all packages: `sudo apt update && sudo apt upgrade`
* Install dependencies: `sudo apt install build-essential git procps curl`
* Install [brew](https://brew.sh):
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> /home/admin/.profile
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
brew install gcc
```
* Install [rbenv](https://github.com/rbenv/rbenv): `brew install rbenv`
* Install [Ruby](https://www.ruby-lang.org/en/):
```bash
sudo apt-get install -y zlib1g-dev
rbenv install 3.0.2 --verbose
rbenv global 3.0.2
rbenv init # Copy in ~/.profile
```
* Install [Rails](https://rubyonrails.org/):
    * Install the [yarn](https://yarnpkg.com/) package manager: `npm install -g yarn`
    * Install [node](https://nodejs.org/it/): `brew install node`
    * Install [libsqlite3-dev](https://packages.debian.org/it/sid/libsqlite3-dev): `apt-get install libsqlite3-dev`
    * Install the [rails gem](https://rubygems.org/gems/rails/versions/5.0.0): `gem install rails`
    * Install [webpacker](https://github.com/rails/webpacker): `rails webpacker:install`

### Get started

* To create an app (it automatically includes `git init` for the project): `rails new MY_APP_NAME`
* To run the web server: 
```bash
cd MY_APP_NAME
rails server
```
* Configure git:
```bash
git config --global color.ui true
git config --global user.name "YOUR-NAME"
git config --global user.email "YOUR-EMAIL"
```

> Create a Rails dockerized dev environment, [guide here](https://www.cloudbees.com/blog/running-rails-development-environment-docker)

## Random Notes
* Ruby on Rails follows the Model-Controller-View (MVC) architectural pattern: **models** are database tables, **controllers** are actions performed on the models, **views** are HTML pages rendered on the browser
* To create a controller, `rails generate controller NAME [action]`
* Views templates have `.html.erb` extensions
* Django's corresponding URLs are called _routes_ (`\config\routes.rb`)
  * The `root` route can be referenced to a specific action of a specific controller (like `root CONTROLLERNAME#ACTION`)
  * To check the routes in this Rails project, run `rails routes` or go to <http://127.0.0.1:3000/rails/info/routes>
* A `resource` is generally anything that you want to reach with a URI and perform CRUD operations on. Simply put, it's a database table which is represented by a model, and acted on through a controller.
