# pitchfx_sql
Create your own database of NBA data in its rawest form using Python and SQL

*NOTE 2018.02.01*: data no longer available at http://stats.nba.com/stats/locations_getmoments/?eventid=1&gameid=0020800001

## Getting started
The NBA's player tracking data provides a wealth of information because it contains data in its rawest form: player and ball coordinates at 40 ms time sampling. In theory, nearly all traditional basketball stats can be derived from these data.

To obtain these data, you must scrape the data off the web. I've done that for you by writing a Python script that scrapes the data and organizes it in an SQL database. All you need to do is run a single line of code,  providing the beginning and end dates of games you are interested in. For instance, if you want to grab data from all games between March 1, 2015, and May 1, 2015, and place the data in a database called *example.db*, run the following code:

`./src/scrape_nbaptmov.py 03-01-2015 05-01-2015 ./Dat/example.db 1`
