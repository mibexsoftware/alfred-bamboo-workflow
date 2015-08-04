# Alfred Workflow for Atlassian Bamboo #

[![Build Status](http://img.shields.io/travis/mibexsoftware/alfred-bamboo-workflow.svg?style=flat-square)](https://travis-ci.org/mibexsoftware/alfred-bamboo-workflow)
[![Latest Version](http://img.shields.io/github/release/mibexsoftware/alfred-bamboo-workflow.svg?style=flat-square)](https://github.com/mibexsoftware/alfred-bamboo-workflow/releases)
[![License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](http://mibexsoftware.mit-license.org/2015)


Alfred workflow to search for Bamboo projects, plans, build results and more in [Atlassian Bamboo][bamboo].


![][screencast]


## Download ##

Get it from the [releases][releases] tab and download the `atlassian-bamboo-workflow-x.x.x.alfredworkflow` file. Install it by opening the downloaded file.


## Usage ##

Start typing `bamboo` in Alfred and you will be guided by a menu.

Please note that you have special actions available for Bamboo build results: use `SHIFT+ENTER` to trigger a build for
the plan and `CMD+ENTER` to download the first artifact of the build result.


## Configuration ##

You have to configure the parameters for connecting to your Bamboo instance. Use the following command:

- `bamboo:config` — Configure the Bamboo host URL, and if necessary, a username and password


## Credits ##

Thanks to [Dean Jackson][deanishe] for building the awesome Python library [Alfred Workflow][alfred-workflow].
Also thanks to Ian Paterson for the awesome [Wunderlist Alfred workflow][wunderlist] which is one of the nicest menu-based Alfred workflows we’ve seen so far and which has inspired our workflow deeply.
Also thanks to Liam McKay for the [build status icons][build-status-icons] and Google for their nice [material design icons][google-material-design].


## License ##

This workflow, excluding the Atlassian Bamboo logo and the Google material icons, is released under the [MIT Licence][mit].


## Author

![https://www.mibexsoftware.com][mibexlogo]


[bamboo]: http://www.atlassian.com/bamboo
[releases]: https://github.com/mibexsoftware/alfred-bamboo-workflow/releases
[mibexlogo]: https://www.mibexsoftware.com/wp-content/uploads/2015/06/mibex.png
[wunderlist]: https://github.com/idpaterson/alfred-wunderlist-workflow
[build-status-icons]: https://www.iconfinder.com/iconsets/function_icon_set
[google-material-design]: https://github.com/google/material-design-icons
[deanishe]: hhttps://github.com/deanishe
[mit]: http://opensource.org/licenses/MIT
[alfred-workflow]: hhttps://github.com/deanishe
[gh-releases]: https://github.com/mibexsoftware/alfred-bamboo-workflow/releases
[packal-page]: http://www.packal.org/workflow/atlassian-bamboo-workflow
[screencast]: https://raw.githubusercontent.com/mibexsoftware/alfred-bamboo-workflow/master/screencast.gif
[alfred-workflow-installation]: http://support.alfredapp.com/workflows:installing/
