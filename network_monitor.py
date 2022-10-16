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

print("""

    Python Network Monitor (C) 2022 Binula Kavisinghe
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it under certain conditions as specified 
    in the GNU General Public License v3.0.

    Please see https://github.com/thebkaviya/Python-Network-Monitor/blob/main/LICENSE or LICENSE.txt for details.
        
    """)

mode_message = ("""

        +-----------------------+
        |  Full = F             |
        |  Lightweight = L      |
        +-----------------------+

 
    """)

def lightweight_mode():

    # get the network I/O stats from psutil
    io = psutil.net_io_counters()
    # extract the total bytes sent and received
    bytes_sent, bytes_recv = io.bytes_sent, io.bytes_recv

    while True:
        # sleep for `UPDATE_DELAY` seconds
        time.sleep(UPDATE_DELAY)
        # get the stats again
        io_2 = psutil.net_io_counters()
        # new - old stats gets us the speed
        us, ds = io_2.bytes_sent - bytes_sent, io_2.bytes_recv - bytes_recv
        # print the total download/upload along with current speeds
        print( f"    Upload: {get_size(io_2.bytes_sent)}   "
            f", Download: {get_size(io_2.bytes_recv)}   "
            f", Upload Speed: {get_size(us / UPDATE_DELAY)}/s   "
            f", Download Speed: {get_size(ds / UPDATE_DELAY)}/s      ", end="\r")
        # update the bytes_sent and bytes_recv for next iteration
        bytes_sent, bytes_recv = io_2.bytes_sent, io_2.bytes_recv

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
    
def main_func():
    while True:
        print(mode_message)
        selected_mode = str(input("Enter the letter of the mode you need... "))
        selected_mode = selected_mode.upper()#converts to uppercase
        #print("You entered", selected_mode)#To remind
        if selected_mode == str("F"):
                    print("Full mode selected")
                    full_mode()
        if selected_mode == str("L"):
                    print("Lightweight mode selected")
                    lightweight_mode()   

main_func()