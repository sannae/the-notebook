# javascript :material-language-javascript:

??? Resources

## Intro

* **Client:** it runs in a web browser using `<script>` tags; it has access to the web page functions and objects (i.e. the Document Object Model or DOM)
* **Server:** the [Node.js](https://nodejs.org) runtime executes JavaScript on the server, it has access to built-in and third-party packages; usually used for building web services.
* **Native:** build native desktop and mobile applications with Electron, React Native and NativeScript

## [Nodejs :material-nodejs:](https://nodejs.org)

Nodejs is a JavaScript runtime to execute scripts out of the browser.

To install NodeJs, use [nvm](https://github.com/nvm-sh/nvm) (Node Version Manager) following the [install instructions](https://github.com/nvm-sh/nvm#install--update-script) on the official GitHub repository. Test it with just `nvm`.

Then install Nodejs:
```bash
nvm install node
```
And test it with
```bash
node -v
```
To run any JavaScript application (as simple as `console.log('Ciao mondo! 🥙');`), use
```bash
node application_name.js
```

## Notes

### Variables

```javascript
const greeting = "Ciao"
const place = "Mondo🌍"
console.log("%s, %s!", greeting, place)
```
```javascript
const greeting = "Ciao"
const place = "Mondo🌍"
console.log(`${greeting}, ${place}!`)
```