from datetime import datetime, time
import pytz


class markettime:
    def marketopen():
        isMarketOpen = False
        # Get the current time in the Eastern Time Zone
        eastern_tz = pytz.timezone("US/Eastern")
        current_time_eastern = datetime.now(eastern_tz).time()

        # Create time objects for the start and end times
        start_time = time(9, 30)
        end_time = time(16, 25)

        # Check if the current time is on a weekday
        if datetime.now(eastern_tz).weekday() < 5:
            # Check if the current time is between market open and close
            if start_time <= current_time_eastern <= end_time:
                # Market is open
                isMarketOpen = True
            else:
                # Market is closed
                isMarketOpen = False
        else:
            # It's a weekend
            isMarketOpen = False

        print(f"The current time is {current_time_eastern}. ")
        return isMarketOpen
