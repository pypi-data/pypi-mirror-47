# Pyloges
The powerfull logging library for Python 3.
## Getting started
When app will be released, just install it with pip:
```
pip install pyloges
```
## Features
None (:
## Planned features
* Logging (1.0)
* Log levels (TRACE/INFO/WARNING/ERROR/FATAL) (1.0)
* Logging to file/stdout/stderr (1.0)
* Custom log format (1.0)
* Exiting on fatal error (1.0)
* Timestamps (1.0)
* Log format examples (1.1)
* Configuration files (1.1)
* File size limits (1.2)
* Mobile platforms (1.2)
* Saving options (1.2)
* Error reporting library integration (1.2)
* Miliseconds in time format (2.0)
* Error handler (2.0)
* Print log to syslog/WinEventLog/Network server/FTP server (2.0)
* Add your own log handlers (2.0)
* Load config file from network (2.0)
## Contribution
You can freely contribute to our github. There're many things you can do: fix bugs, add new features, make translations. Please follow several simple rules:
* Create one issue per one bug
* Do not duplicate issues
* Specify the platform in issues
* Specify steps to reproduce in issues
* Create one pull request per one feature
* Create one commit for one small piece of implementation
* Write simple functions. Every function must do one small thing. All actions in function must be on one abstraction level
* Specify type of return value and arguments, e.g.
```python 
def check(site: dict) -> bool:
    """Check if site is available."""
    
    pass
```
* Write pydocs if it's needed
* Write unit tests for your code (python unittest) and put it in "tests" folder
* Place copyright and licence header in top of every file, you can find example in any project source file
* Before starting pull request, run all unit tests to make sure that you did not break anything
* Add your name to list of contributors in end of this file
## License
![GNU GPL v3 logo](https://www.gnu.org/graphics/gplv3-127x51.png)

Prologes is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Prologes is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Prologes.  If not, see <https://www.gnu.org/licenses/>.

IMPORTANT NOTE: according to GNU GPL, you must licence your project to GNU GPL v3 if you use our library
## Authors and copyright
Copyright (C) 2018 NIkita S., All Rights Reserved<br>
*For any questions contact <nikitaserba@icloud.com><br>*
## Links
[Download library](https://github.com/Nekit10/pyloges/releases)<br>
[License](https://github.com/Nekit10/pyloges/blob/master/LICENSE)<br>
[Bug reporter](https://github.com/Nekit10/pyloges/issues)<br>
[Latest source](https://github.com/Nekit10/pyloges/tree/develop)<br>
