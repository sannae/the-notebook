# javascript :material-language-javascript:

!!! Resources
    * [:material-youtube: Javascript for Beginners](https://www.youtube.com/playlist?list=PLlrxD0HtieHhW0NCG7M536uHGOtJ95Ut2) by Microsoft Developers

## Intro

* **Client:** it runs in a web browser using `<script>` tags; it has access to the web page functions and objects (i.e. the Document Object Model or DOM)
* **Server:** the [:material-nodejs: Node.js](https://nodejs.org) runtime executes JavaScript on the server, it has access to built-in and third-party packages; usually used for building web services.
* **Native:** build native desktop and mobile applications with Electron, React Native and NativeScript

## Nodejs

[Node.js](https://nodejs.org) is a JavaScript runtime to execute scripts out of the browser.

To install Node.js, use [:material-github: nvm](https://github.com/nvm-sh/nvm) (Node Version Manager) following the [:material-github: install instructions](https://github.com/nvm-sh/nvm#install--update-script) on the official GitHub repository. Test it with just `nvm`.

Then install Node.js:
```bash
nvm install node
```
And test it with
```bash
node -v
```
To run any JavaScript application (as simple as `console.log('Ciao mondo! 🥙');`), use
```bash
node APPLICATION_NAME.js
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