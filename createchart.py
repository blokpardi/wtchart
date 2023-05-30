import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np
import requests
from urllib.parse import urlparse
from matplotlib.ticker import FuncFormatter
from matplotlib.dates import date2num
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import io
from PIL import Image
import imgkit
from config import config
import twill.commands as twill

from markettime import markettime
from posttodiscord import posttodiscord


def createChartFromFile(data):
    # Convert 'Entry Time' column to datetime format
    data["Entry Time"] = pd.to_datetime(data["Entry Time"])

    # Set the start date if specified in the config
    start_date = config["startdate"]
    if start_date != "all":
        start_date = pd.to_datetime("2023-03-13")

        # Filter the data to include entries from the start date onwards
        data = data[data["Entry Time"] >= start_date]

    # Filter the data if spedified in the config
    datafilter = config["botfilter"]
    if datafilter != "none":
        data = data[data["Bot"].str.contains("0 DTE")]

    # Remove the '$' sign and commas from 'Profit $' and 'Broker Fee' columns, then convert to numeric
    data["Profit $"] = (
        data["Profit $"].str.replace("$", "").str.replace(",", "").astype(float)
    )
    data["Broker Fee"] = (
        data["Broker Fee"].str.replace("$", "").str.replace(",", "").astype(float)
    )

    # Subtract broker fee from profit for each day
    data["Profit $"] = data["Profit $"] - data["Broker Fee"]

    # Group the data by date and calculate the cumulative profit
    grouped_data = (
        data.groupby(data["Entry Time"].dt.date)["Profit $"]
        .sum()
        .cumsum()
        .reset_index()
    )

    # Convert the dates to numerical values
    grouped_data["Entry Time"] = date2num(pd.to_datetime(grouped_data["Entry Time"]))

    # Create a figure and axis with adjusted width and height
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot the cumulative profit over time with smaller points
    ax.plot_date(
        grouped_data["Entry Time"], grouped_data["Profit $"], "o-", markersize=6
    )

    # Set the labels and title
    # ax.set_xlabel('Entry Time')
    # ax.set_ylabel('Cumulative Profit $')
    ax.set_title("0 DTE After Fees")

    # Format the x-axis as dates
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Remove the left vertical axis
    ax.spines["left"].set_visible(False)
    ax.yaxis.tick_right()

    # Create a custom formatter for the right y-axis to display profits in whole dollars
    def dollar_formatter(x, pos):
        return "${:,.0f}".format(x)

    # Set the formatter for the right y-axis
    ax.yaxis.set_major_formatter(FuncFormatter(dollar_formatter))

    # Set the limits of the right y-axis
    min_profit = grouped_data["Profit $"].min()
    max_profit = grouped_data["Profit $"].max()
    ax.set_ylim(bottom=min_profit, top=max_profit)

    # Add a trendline
    x = grouped_data["Entry Time"]
    y = grouped_data["Profit $"].values
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    trendline_x = np.linspace(x.min(), x.max(), len(x))
    trendline_y = p(trendline_x)
    ax.plot_date(trendline_x, trendline_y, "-", color="green")

    # This section reads the HTML file with bot details, creates an image, and
    # includes the image in the chart. I found it was the best way to get
    # formatted text and place it in the chart where I wanted it.

    print(f"Notes: {config['notes']}")

    if config["notes"]:
        # Read HTML-formatted text from another file
        with open("data/bots.html", "r") as file:
            html_content = file.read()

        # Specify options for the imgkit library (e.g., to set image width and height)
        options = {"width": "200", "height": "200"}

        # Convert HTML to an image using imgkit
        image = imgkit.from_string(html_content, False, options=options)

        # Create a BytesIO object to hold the image data
        image_io = io.BytesIO(image)

        # Open the image using PIL
        pil_image = Image.open(image_io)

        # Calculate the image size based on the plot size
        box_width = 0.3
        box_height = 0.1

        # Add the image to the plot
        offset_image = OffsetImage(pil_image, zoom=1)
        offset_image.image.axes = ax
        ab = AnnotationBbox(
            offset_image,
            (0.00, 0.95),
            xybox=(0, 0),
            xycoords="axes fraction",
            boxcoords="offset points",
            box_alignment=(0, 1),
        )
        ax.add_artist(ab)

    # Update the figure layout to accommodate the image
    plt.tight_layout()
    plt.subplots_adjust(left=0.02, right=0.94, top=0.95, bottom=0.13)

    # Set default font properties
    font = {"family": "Arial", "weight": "bold", "size": 12}
    matplotlib.rc("font", **font)

    # Hide the legend
    ax.legend().set_visible(False)

    # Add a light grey grid to the background
    ax.grid(color="lightgrey", linestyle="--")

    # Save the chart as an image
    plt.savefig("dailychart.png")

    # Show the plot. Uncomment this if you want a chart to display before generating the commentary.
    # plt.show()


def commentary(df):
    # Convert 'Exit Time' column to datetime
    df["Exit Time"] = pd.to_datetime(df["Exit Time"])

    # Extract only the date from 'Exit Time' column
    df["Exit Date"] = df["Exit Time"].dt.date

    # Filter rows where '0 DTE' is in the 'Bot' column
    filtered_df = df[df["Bot"].str.contains("0 DTE")]

    # Find the latest date in the 'Exit Date' column
    latest_date = filtered_df["Exit Date"].max()

    # Filter rows with the latest date in the 'Exit Date' column
    latest_df = filtered_df[filtered_df["Exit Date"] == latest_date]

    # Remove the dollar sign and convert 'Profit $' column to numeric
    latest_df["Profit $"] = latest_df["Profit $"].str.replace("$", "").astype(float)

    # Calculate the sum of the 'Profit $' column
    total_profit = latest_df["Profit $"].sum()

    # Prepend dollar sign and +/- sign based on the value
    if total_profit >= 0:
        formatted_profit = "+${:,.2f}".format(total_profit)
    else:
        formatted_profit = "-${:,.2f}".format(abs(total_profit))

    # Add negative 'Bot' values for negative profits. We do this to create the commentary
    # on what bots stopped out
    tza = int(config["timezoneadjust"])
    negative_rows = latest_df[latest_df["Profit $"] < 0]
    negative_times = negative_rows["Bot"].str.extract(r"(-?\d+:\d+)")
    negative_times = negative_times[0].apply(
        lambda time: ":".join(
            [
                str((int(time.split(":")[0]) + tza) % 24 - 12)
                if int(time.split(":")[0]) + tza > 12
                else str((int(time.split(":")[0]) + tza) % 24),
                time.split(":")[1],
            ]
        )
    )
    negative_bots = ", ".join(negative_times.str.strip())

    negative_reasons = []
    if negative_bots:
        for index, row in negative_rows.iterrows():
            time = negative_times[index]
            if "PCS" in row["Bot"]:
                negative_reasons.append(f"{time} PUT ")
            elif "CCS" in row["Bot"]:
                negative_reasons.append(f"{time} CALL ")

    formatted_profit += " {}".format("and ".join(negative_reasons))
    if negative_bots:
        formatted_profit += "stopped."

    # Print the total profit/loss for the current day
    print(formatted_profit)
    return formatted_profit


# Globals for file download
whisper_trades_url = config["wtlogin"]
csv_location = config["csv_location"]
save_location = config["save_location"]

if not markettime.marketopen():
    # Connect to the whisper trades site
    twill.go(whisper_trades_url)

    # Login to whisper trades
    twill.fv("1", "email", config["username"])
    twill.fv("1", "password", config["password"])
    twill.submit()

    twill.go(csv_location)
    positions = twill.browser.html

    # Save the contents to a file
    file_path = save_location
    with open(file_path, "w") as file:
        file.write(positions)

    print(f"File saved successfully at: {file_path}")

    # Read the CSV file
    data = pd.read_csv("data/WT Positions.csv")

    createChartFromFile(data)
    comments = commentary(data)
    if config["posttodiscord"]:
        posttodiscord.createpost(comments)

else:
    print(
        f"The Market is open so we have incomplete data for today's trades. Please wait until the market is closed and try again."
    )
