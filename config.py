config = {
    "timezoneadjust": "0",  # put the number needed to adjust to EST. E.g. East Coast would be 0, West Coast would be 3.
    "startdate": "all",  # use 'all' to include the entire data set. otherwise set a date in the format 2023-01-01
    "botfilter": "none",  # string to filter bots for the chart. use 'none' for no filter
    "notes": True,  # set to True if you want to include notes in a box in the upper left of the chart, False if not.
    "noteslocation": "/home/myfolder/wtchart/data/bots.html",  # location of the bots.html file on your computer
    "wtlogin": "https://whispertrades.com/login",
    "username": "user@email.com",  # your username
    "password": "yourpassword",  # your password
    "csv_location": "https://whispertrades.com/positions/export/",  # WT url to pull the csv file
    "save_location": "/home/myfolder/wtchart/data/WT Positions.csv",  # location on your computer to save the file
    "posttodiscord": False,  # set to true if you want to auto-post to discord. False if not.
    "discord_authtoken": "yourauthtoken",
    "channel_id": "channelid",  # specify the discord channel ID. posttodiscord must be set to true for this to work
}
