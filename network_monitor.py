import psutil
import time
import os
import pandas as pd

UPDATE_DELAY = 1 # in seconds

def get_size(bytes):
    """
    Returns size of bytes in a nice format
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024

def full_mode():

    # get the network I/O stats from psutil on each network interface
    io = psutil.net_io_counters(pernic=True)

    while True:

        time.sleep(UPDATE_DELAY)
        io_2 = psutil.net_io_counters(pernic=True)  # get the network I/O stats again per interface
        
        data = []
        for iface, iface_io in io.items():
            # new - old stats gets us the speed
            upload_speed, download_speed = io_2[iface].bytes_sent - iface_io.bytes_sent, io_2[iface].bytes_recv - iface_io.bytes_recv
            data.append({
                "iface": iface, "Download": get_size(io_2[iface].bytes_recv),
                "Upload": get_size(io_2[iface].bytes_sent),
                "Upload Speed": f"{get_size(upload_speed / UPDATE_DELAY)}/s",
                "Download Speed": f"{get_size(download_speed / UPDATE_DELAY)}/s",
            })
        io = io_2 # update the I/O stats
        df = pd.DataFrame(data) # construct a Pandas DataFrame to print stats in a tabular style
        df.sort_values("Download", inplace=True, ascending=False) # sort values per column
        os.system("cls") if "nt" in os.name else os.system("clear") # clear the screen
        print(df.to_string())

full_mode()