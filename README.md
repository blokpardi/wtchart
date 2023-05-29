This will let you create a chart from Whispertrade position data. It does several things:

1. It downloads the latest csv file from Whispertrades (WT Positions.csv)
2. It creates a profit and loss chart using that data
3. Creates "commentary" - how much win or loss on the latest day, and notes the positions that stopped out.
4. It can post to Discord

IT WILL NOT WORK UNLESS THE CONFIG IS SETUP CORRECTLY. Here are the parameters and their supported values:

timezoneadjust - Since the community uses east coast time we adjust our output to match for those of us not on the East Coast. Put the number needed to adjust to EST. E.g. East Coast would be 0, West Coast would be 3.

startdate - If you want to start from any other date than what is in the data file. Use 'all' to include the entire data set. otherwise set a date in the format 2023-01-01

botfilter - Use this to filter bots for the chart. use 'none' for no filter, or whatever text would filter the correct bots for your chart. E.g. "0 DTE"

wtlogin - The login URL for Whispertrades "https://whispertrades.com/login"

username - Your Whispertrades login

password - your Whispertrades password

csv_location - The URL to fetch the positions CSV file: "https://whispertrades.com/positions/export/"

save_location - The location on your computer where you want to download the CSV file, e.g., "/home/myfolder/wtchart/data/WT Positions.csv" This sample almost certainly will not work for you, so make sure the location exists or you'll get an error.

posttodiscord - Set to true if you want to auto-post to discord. False if not.

discord_authtoken - your Discord authorization token. Google if you don't know how to get it.

channel_id - Specify the discord channel ID for the channel where you want your post to appear. Posttodiscord must be set to true for this to work.
