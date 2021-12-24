# reactjs :material-react:

??? Resources
    * [:material-react: React docs](https://reactjs.org/docs/hello-world.html)

??? Tutorials
    * [:material-youtube: Build a stock app with ReactJs](https://youtube.com/playlist?list=PL_kr51suci7WkVde-b09G4XHEWQrmzcpJ)

## Prerequisites

Install the latest version of `npm` :material-npm: (or to upgrade your current version):
```bash
npm install -g npm
```
or simply
```bash
apt-get install npm
```
Enter the npm script environment with `npx`.

## Get started

To [create your first React app](https://reactjs.org/docs/create-a-new-react-app.html), use the `create-react-app` utility:
```bash
npx create-react-app MY-APP
```
It will take some time!

The `create-react-app` will provide all the essential packages to start a React app, including:
* `src/`: the actual code to be edited
* `node_modules/`: the React packages, imported in each `js` file using the first row `import React from 'react'`
* `public/`: it contains the actual website, i.e. the `index.html`
* a convenient `readme.md` with all the instructions for using `create-react-app`

### Run the dev server

To run the development server,
```bash
cd MY-APP
npm start
```
The browser should automatically refresh at each change, as soon as you save your files. If it doesn't, you probably have to [:material-stack-overflow: increase the frequency](https://stackoverflow.com/questions/42189575/create-react-app-reload-not-working) of the [`inotify`](https://man7.org/linux/man-pages/man7/inotify.7.html) event monitoring process.

### Architecture

Reactjs is used to build Single-Page Apps (SPAs), meaning that each page and each component in the page is rendered as an independent javascript file. You may therefore implement each page or each component separately.

The main html page is `/public/index.html`:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="shortcut icon" href="%PUBLIC_URL%/favicon.ico">
    <title>Hotline front-end</title>
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>
```

The `root` element is rendered by `/src/index.js`:
```javascript
ReactDOM.render(
  <App />,
  document.getElementById('root')
);
```
Which contains the main `App` element, the one where all the routing and component rendering is implemented:
```javascript
function App() {
    return (
        /* Your app here */
    );
}
export default App;
```

### Data

Use [mockaroo](https://www.mockaroo.com) to create a large mock dataset in JSON format to feed your React App. 