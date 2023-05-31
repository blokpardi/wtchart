## Welcome

These Python scripts will let you create a chart from Whispertrade position data. It does several things:

1. It downloads the latest csv file from Whispertrades (WT Positions.csv).
2. It creates a profit and loss chart using that data, as well as inserts a list of current bots and notes.
3. Creates "commentary" - how much win or loss on the latest day, and notes the positions that stopped out.
4. It can automatically post the chart and commentary to Discord.

### How it works

1. Setup the config (see _Config_ below)
2. Setup your HTML file with bot info (see _Notes File_ below)
3. Run _createchart.py_

The script drops an image of the chart in the location of the _createchart.py_ script, and the commentary is output to the console. If you setup your config to post to Discord it will automatically create a post with the chart and commentary and post it to the Discord channel of your choice.

### Setup

You'll need to have some basic familiarity with Python, have an environment where you can run Python code, and install all the necessary libraries:

    * matplotlib
    * pandas
    * numpy
    * imgkit
    * twill
    * discord
    * pytz

I built this on Python 3.10.6. It's not setup as a virtual environment, but no reason you can't set it up that way if you want to.

### Config

IT WILL NOT WORK UNLESS THE CONFIG IS SETUP CORRECTLY. At a minimum you need to include your WT username and password and a save location. The notes file is sample data, so that will display what's there unless you change it.

The config file is _config.py_. Here are the parameters and their supported values:

- _timezoneadjust_ - Since the community generally talks about trades in East Coast time I want to follow community patterns and "talk the talk" :-). So we adjust our output to match for those of us not on the East Coast. Put the number needed to adjust to EST. E.g. East Coast would be 0, West Coast would be 3.

- _startdate_ - Use this if you want to start from any other date than the earliest found in the data file. Use 'all' to include the entire data set. Otherwise set a date in the format: 2023-01-01

- _botfilter_ - Use this to filter bots for the chart. Use 'none' for no filter (it will include the entire dataset), or whatever text would filter the correct bots for your chart, e.g. "0 DTE". I built this to create a chart for 0 DTE trades, and all my 0 DTE bots include '0 DTE' in their names, so I use that filter when creating the chart. But any string will work here, so you can create charts for any set of bots as long as your bot names have a consistent string to filter on.

- _notes_ - Specifies whether to include the content of the _bots.html_ file in the upper left of the chart (see _Notes File_ below). Set to True if you want to include notes, False if not.

- _wtlogin_ - The login URL for Whispertrades "https://whispertrades.com/login". No need to change this unless WT makes a change.

I put username and password in the config to keep them out of the code. Up to you to make sure they are secret and safe!!!

- _username_ - Your Whispertrades login
- _password_ - Your Whispertrades password

- _csv_location_ - The URL to fetch the positions CSV file: "https://whispertrades.com/positions/export/". No need to change this unless WT makes a change.

- _save_location_ - The location on your computer where you want to download the CSV file, e.g., "/home/myfolder/wtchart/data/WT Positions.csv". This sample location almost certainly will not work for you (it would be pretty odd if it did!), so make sure the location exists or you'll get an error. Note that the filename is included. You can change that to anything you want.

- _posttodiscord_ - Set to true if you want to auto-post to Discord, False if not.

- _discord_authtoken_ - your Discord authorization token. Google if you don't know how to get it.

- _channel_id_ - Specify the Discord channel ID for the channel where you want your post to appear. posttodiscord config must be set to True for this to have any effect, otherwise it's ignored.

### Notes File

The _bots.html_ file contains the details of the bots included in the chart, and any corresponding notes. The content will appear in a box in the upper left side of the chart if it's turned on in your config. You should be comfortable with very basic HTML editing to change this, though following the formatting in the included example should work fine for most people.

The HTML is a simple table with two columns. The first column is a list of the bots represented in the chart. Obviously this is not automagic, you must put them in manually. Maybe someday I'll automate this, but it's manual right now. The second column is any notes related to that list of bots.

The HTML can be changed to anything you want really, but just know that any changes may not appear correctly on the chart and you'll have to make some size adjustments. You can test changes quickly by turning on the chart display (see _Chart preview_ in the _Misc_ section below). Adjustments can be made in the HTML itself for things like column widths, etc. You may also have to change the size of the box on the chart. This can be done in the following line in _createchart.py_:

    options = { "width": 200, "height": 200, "format": "png", "quality": 100, }

### Misc

**Using while Market is open**

The WT position data is kept current during the day. That means that while there are open trades the data is incomplete. Rather than try and sort all that out, and only use the most up to date data (which I'm not sure is overly useful for this purpose), I'm checking to see if the market is open and will not run the chart creator if it is. Just wait until the market is closed and all open positions are updated. I'm using 4:25PM EST to be safe.

- This is a binary check to see if it's currently market hours during weekdays, so not very sophisticated. For example, it does not check to see if you have any open positions and run if all positions are closed. It will just tell you to wait. :)
- It does not account for holidays, etc. So if it is a Monday holiday, for example, and the Market would ordinarily be open, it will still not run the chart creator.

If you want to force the code to run, just change the following line in _createchart.py_

    if not markettime.marketopen:

to

    if markettime.marketopen:

and it will run. You'll need to change it back for normal function during normal Market hours.

**Chart preview**

The following line appears at the end of the createChartFromFile function in _createchart.py_:

    # plt.show()

Uncommenting ply.show() will display the chart in a window. Know that this is a blocking action and nothing else will run until the chart is dismissed. But it's helpful if you want to see the chart for testing purposes or to take a quick check before posting, etc. A chart image (dailychart.png) is dropped to the same folder location as _createchart.py_ by the time it reaches this point in the code, so there's a local copy there as well.
