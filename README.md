# Sublime/Oz

[Oz language](http://mozart.github.io/) support for [Sublime Text 3](https://www.sublimetext.com/).
This plugin intends to be an alternative to the classic Emacs Oz interface.
It is however still in work. Particularly killing subprocesses is still not
correctly implemented and not automatic.

## Usage
The main feature that needs input from the user is feed like commands
When you feed something, it should automatically start *ozengine* subprocess.
The default shortcuts are the following :

 * Feed Line : **Ctrl-. + Ctrl-l**
 * Feed Region : **Ctrl-. + Ctrl-r**
 * Feed Buffer : **Ctrl-. + Ctrl-b**
 * Kill oz : **Ctrl-. + Ctrl-k**

Please note that once you started the ozengine
subprocess you will need to kill it manually.

## Features

  * Syntax Highlighting - detects files matching the pattern `*.oz`.
  * Comments - Applies Oz-style single line (%) comments using standard commands/shortcuts.
  * Feed Line - Feed the current line, compile and execute it within ozengine
as in the classic OPI
  * Feed Region - Feed the current region, compile and execute it within
ozengine as in the classic OPI
  * Feed Buffer - Feed the current buffer, compile and execute it within ozengine as in the classic OPI

## Automatic Installation

Sublime/Oz is available from [Package Control](https://packagecontrol.io/packages/Oz) under the name `Oz`.
This package contains only the syntax Highlighting and Comments. If you wish to
use the build/run features you need to install the plugin manualy.

## Manual Installation

Download this repo as an archive or `git clone` it under the `Packages\User` directory under your Sublime user path.

On Windows, this is something like `C:\Users\%USER_NAME%\AppData\Roaming\Sublime Text 3\Packages`.

On linux, this is something like `/home/user/.config/sublime-text-3`

Once the `sublime-oz` package is in place, just restart Sublime, and it should be ready to go.

## OPI

The Oz Programming Interface is started with the plugin command _view.run\_run\_command(oz\_run)_.
This command calls _ozengine x-oz://system/OPI.ozf_.
This creates two sockets to communicate with the process.
The first one, allows to give instruction to the compiler and the second one is used for special instruction, for example start the debugger.
We connect to the first one using [socket\_pipe.py](socket\_pype.py).
Please note that this file is a simple modification of pre-existing Class from this [repository](https://github.com/nasser/Socket)
The message we send to this socket is actually very simple. We just send what
we want to compile and add this \n\004\n.


## Future Work

  * Snippets
  * Feed line/Feed region
  * Formatting
  * Killing at close ozengine/ozemulator(on Unix like)/ozwish(if Browse is used)
  * Redirect compilation and emulator output.

## Contributing

Pull requests welcome. The latest version of Sublime should have everything you need to develop and test enhancements to this package.
