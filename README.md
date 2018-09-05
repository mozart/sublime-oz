# Sublime/Oz

[Oz language](http://mozart.github.io/) support for [Sublime Text 3](https://www.sublimetext.com/).
This plugin intends to be an alternative to the classic Emacs Oz interface.
It is however still in work. Particularly killing subprocesses is still not
correctly implemented and not automatic.

## Usage

To evaluate some code, you need to feed it to the Oz compiler.
This can be done from the "Oz" menu, from the context menu or with the following shortcuts.

 * Feed Line : **Ctrl-. + Ctrl-l**
 * Feed Region (selected text): **Ctrl-. + Ctrl-r**
 * Feed Buffer (the whole file): **Ctrl-. + Ctrl-b**

It may be useful to kill the running compiler. This is also available in the "Oz" menu, or with a shortcut.
The compiler will be restarted automatically on the next feed command.

 * Kill oz : **Ctrl-. + h**


## Features

  * OPI Integration - Submit current line/selection/file to the Oz compiler (as with the Emacs OPI).
  * Syntax Highlighting - detects files matching the pattern `*.oz`.
  * Comments - Comment/Uncomment Oz code using standard commands/shortcuts.

## Automatic Installation

Sublime/Oz is available from [Package Control](https://packagecontrol.io/packages/Oz) under the name `Oz`.
This package contains only the syntax Highlighting and Comments. If you wish to
use the build/run features you need to install the plugin manualy.

## Manual Installation

Download this repo as an archive or `git clone` it under the `Packages\User` directory under your Sublime user path.

On Windows, this is something like `C:\Users\%USER_NAME%\AppData\Roaming\Sublime Text 3\Packages`.

On linux, this is something like `/home/user/.config/sublime-text-3`

Once the `sublime-oz` package is in place, just restart Sublime, and it should be ready to go.

## Future Work

  * Snippets
  * Formatting

## Contributing

Pull requests welcome. The latest version of Sublime should have everything you need to develop and test enhancements to this package.
