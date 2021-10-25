# Ruby on Rails

## Random Notes
* Ruby on Rails follows the Model-Controller-View (MVC) architectural pattern: **models** are database tables, **controllers** are actions performed on the models, **views** are HTML pages rendered on the browser
* To create a controller, `rails generate controller NAME [action]`
* Views templates have `.html.erb` extensions
* Django's corresponding URLs are called _routes_ (`\config\routes.rb`)
  * The `root` route can be referenced to a specific action of a specific controller (like `root CONTROLLERNAME#ACTION`)
  * To check the routes in this Rails project, run `rails routes` or go to <http://127.0.0.1:3000/rails/info/routes>
* A `resource` is generally anything that you want to reach with a URI and perform CRUD operations on. Simply put, it's a database table which is represented by a model, and acted on through a controller.