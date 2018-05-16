# web-mon

## Pre-requisites
This project uses only standard libraries, 
but to be sure here's the checklist:
* Python 3
  * tkinter
  * sqlite3
  * html
  * urllib

## Client
GUI can be opened by running Python interpreter against **client.py**:
`python3 client.py`. 
Client also populates database with a sample dataset for the sake of demo.
GUI consists of three tabs: **Themes**, **Websites** and **Monitoring**.

#### Themes
This pane allows to configure list of *themes* by providing *theme name* and a *list of keywords* related to it.

#### Websites
Here you can setup targets with *url* and optional *crawl depth* (defaults to 1, max value is 10).

#### Monitoring
Finally, here we can see results of any successful crawling attempts, which include *timestamp*, *url* and detected *theme*.
Can be filtered by *date range*.

## Daemon
This is the module which actually crawls configured websites for defined themes (by searching for keywords on each HTML page).
You can setup a **cronjob** to run it periodically, e.g:
`0 0 * * * python3 daemon.py`.
Any results will be written into the databse. It also logs any successful findings into console.

## Database
Configuration changes (from **client**) and crawling results (from **daemon**) are written into SQLite database file: `web-mon.db`.
To start anew simply delete the file.
