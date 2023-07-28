import tkinter as tk
from tkinter import filedialog
import ntplib, base64, subprocess, zipfile
from datetime import datetime
from tkcalendar import DateEntry

def encode_string(string):
    string = str(string)
    encoded_string = base64.b64encode(string.encode("utf-8")).decode("utf-8")
    encoded_string = str(encoded_string)
    return encoded_string

def get_current_date():
    try :
        ntplib_client = ntplib.NTPClient()
        response = ntplib_client.request('pool.ntp.org')
        current_date = datetime.fromtimestamp(response.tx_time)
        current_date = datetime.strftime(current_date, "%y-%m-%d")
        print(current_date)
        return current_date
    except :
        today_Date = datetime.now()
        today_Date = datetime.strftime(today_Date, "%y-%m-%d")
        print("System date " + today_Date)
        return today_Date

def zip_file():
    location = filedialog.askopenfilename()
    zip_data(location)
def zip_folder():
    location = filedialog.askdirectory()
    zip_data(location)

def unzip():
    location = filedialog.askopenfilename()
    unzip_data(location)

def unzip_data(location):
    unzip_window = tk.Toplevel()
    location_l = tk.Label(unzip_window, text="Location ")
    location_e = tk.Entry(unzip_window)
    location_e.insert(0, location)
    location_l.pack(padx=10, pady=10)
    location_e.pack(padx=10, pady=10)

    start_b = tk.Button(unzip_window, text="Start Extraction", command=lambda: start_unzip(location_e))
    cancel_b = tk.Button(unzip_window, text="Cancel", command=unzip_window.destroy)
    start_b.pack(padx=10, pady=10)
    cancel_b.pack(padx=10, pady=10)

def start_unzip(location_entry):
    location = location_entry.get()

    try:
        with zipfile.ZipFile(location, "r") as zip_ref:
            zip_ref.extractall()
        print("Successfully extracted the ZIP file.")
    except Exception as e:
        print("Error: Unable to extract the ZIP file.")
        print(str(e))

root = tk.Tk()
root.title("Automate the app")
zip_file_b = tk.Button(root, text="Zip a file", command=zip_file)
zip_folder_b = tk.Button(root, text="Zip a folder", command=zip_folder)
unzip_file = tk.Button(root, text="Unzip file", command=unzip)  # Updated command to call the unzip function
exit_b = tk.Button(root, text="Exit", command=root.destroy)
zip_file_b.pack(padx=10, pady=10)
zip_folder_b.pack(padx=10, pady=10)
unzip_file.pack(padx=10, pady=10)
exit_b.pack(padx=10, pady=10)

root.mainloop()
