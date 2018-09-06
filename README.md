# Sublime/Oz

[Oz language](http://mozart.github.io/) support for [Sublime Text 3](https://www.sublimetext.com/).

## Features

  * Syntax Highlighting - detects files matching the pattern `*.oz`.
  * Comments - Comment/Uncomment Oz code using standard commands/shortcuts.
  * OPI Integration - Submit current line/selection/file to the Oz compiler.
    * Still a work in progress. Killing subprocesses does not work reliably.

## Installation

Sublime/Oz is available from [Package Control](https://packagecontrol.io/packages/Oz) under the name `Oz`.

In order to build and run Oz code, the Oz compiler will need to be installed separately.

## Usage

Code can be submitted to the compiler in individual lines, in regions (selected text) or entire files (buffer). These commands can be accessed from the "Oz" menu, the context menu or with the following shortcuts:

  * Feed Line: `Ctrl-. + Ctrl-l`
  * Feed Region: `Ctrl-. + Ctrl-r`
  * Feed Buffer: `Ctrl-. + Ctrl-b`
  * Kill Oz Compiler Subprocess: `Ctrl-. + h`

If killed, the compiler subprocess will be restarted automatically on the next feed command.

## Future Work

  * Snippets
  * Formatting
  * Linting

## Contributing

Pull requests welcome. The latest version of Sublime should have everything you need to develop and test enhancements to this package.
