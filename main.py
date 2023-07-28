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
#
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
    password = get_current_date()
    print(password)
    password = "23-07-27"
    try:
        with zipfile.ZipFile(location, "r") as zip_ref:
            zip_ref.extractall(pwd= password.encode("utf-8"))
        print("Successfully extracted the ZIP file.")
    except Exception as e:
        print("Error: Unable to extract the ZIP file.")
        print(str(e))
#
def zip_data(location):
    zip_window = tk.Toplevel()
    location_l = tk.Label(zip_window, text="Location ")
    location_e = tk.Entry(zip_window)
    location_e.insert(0, location)
    print(location)
    selction_l = tk.Label(zip_window, text="Unzip Date")
    selection_e = DateEntry(zip_window)
    output_file_name_l = tk.Label(zip_window, text="Output file name")
    output_file_name_e = tk.Entry(zip_window)
    output_file_name_e.insert(0, "output.zip")
    start_b = tk.Button(zip_window, text="Start Compression", command=lambda: start_shell_compression(location_e, selection_e, output_file_name_e))
    cancel_b = tk.Button(zip_window, text="Cancel", command=zip_window.destroy)
    location_l.pack(padx=10, pady=10)
    location_e.pack(padx=10, pady=10)
    selction_l.pack(padx=10, pady=10)
    selection_e.pack(padx=10, pady=10)
    output_file_name_l.pack(padx=10, pady=10)
    output_file_name_e.pack(padx=10, pady=10)
    start_b.pack(padx=10, pady=10)
    cancel_b.pack(padx=10, pady=10)
def start_shell_compression(location_entry, password_entry, output_name_entry):
    location = location_entry.get()
    password = password_entry.get()
    output_name = output_name_entry.get()

    e_password = encode_string(password)
    info_message = "This file can be opened after " + get_current_date()
    save_a_file(info_message)

    #for creating the protected data in zip with password  
    zip_result = subprocess.run(["zip", "-r", "-P", e_password, output_name, location], capture_output=True, text=True)
    #for creating the info file without password so it can tell when to unlock and how to unlock
    subprocess.run(["zip", "-r",  output_name, "_info.txt"], capture_output=True, text=True)
    
    if zip_result.returncode == 0:
        print("Successfully created the ZIP file.")
        print(zip_result.stdout)
    else:
        print("Error: Unable to create the ZIP file.")
        print(zip_result.stderr)

def save_a_file(string):
    with open("_info.txt", "w") as file:
        file.write(string)

root = tk.Tk()
root.title("Automate the app")
zip_file_b = tk.Button(root, text="Zip a file ", command=lambda : zip_file())
zip_folder_b = tk.Button(root, text="Zip a folder ", command=lambda :zip_folder())
unzip_file = tk.Button(root, text="Unzip file", command=lambda : unzip())
exit_b = tk.Button(root, text="Exit", command=lambda : root.destroy())
zip_file_b.pack(padx=10, pady=10)
zip_folder_b.pack(padx=10, pady=10)
unzip_file.pack(padx=10, pady=10)
exit_b.pack(padx=10, pady=10)

root.mainloop()