# reactjs :material-react:

!!! **Resources:*
    * :material-react: [React docs](https://reactjs.org/docs/hello-world.html)

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
The browser should automatically refresh at each change.

### Architecture

Reactjs is used to build Single-Page Apps (SPAs), meaning that each page and each component in the page is rendered as an independent javascript file. You may therefore implement each page or each component separately.
