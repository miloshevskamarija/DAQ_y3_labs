import os
import matplotlib.pyplot as plt
import numpy as np

event_counts = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]  #number of readings per file

#lists for storing the file sizes (in bytes) for each format 
csv_sizes = []
bin_sizes = []
h5_sizes  = []
json_sizes = []

#gets the file sizes per reading
for n in event_counts:
    csv_file = f"temp_data_{n}_entries.csv"
    bin_file = f"temp_data_{n}_entries.bin"
    h5_file  = f"temp_data_{n}_entries.h5"
    json_file = f"temp_data_{n}_entries.json"

    if os.path.exists(csv_file):
        csv_sizes.append(os.path.getsize(csv_file) / n) #divides by the number of events 'n' to show events per reading
    else:
        csv_sizes.append(np.nan)

    if os.path.exists(bin_file):
        bin_sizes.append(os.path.getsize(bin_file) / n) #divides by the number of events 'n' to show events per reading
    else:
        bin_sizes.append(np.nan)

    if os.path.exists(h5_file):
        h5_sizes.append(os.path.getsize(h5_file) / n) #divides by the number of events 'n' to show events per reading
    else:
        h5_sizes.append(np.nan)
        
    if os.path.exists(json_file):
        json_sizes.append(os.path.getsize(json_file) / n) #divides by the number of events 'n' to show events per reading
    else:
        json_sizes.append(np.nan)

#plotting
plt.figure(figsize=(8, 5))
plt.plot(event_counts, csv_sizes, 'o--', label='CSV (bytes per reading)')
plt.plot(event_counts, bin_sizes, 's--', label='Binary (bytes per reading)')
plt.plot(event_counts, h5_sizes, '^--', label='HDF5 (bytes per reading)')
plt.plot(event_counts, json_sizes, 'd--', label='JSON (bytes per reading)')
plt.xlabel("Number of Temperature Readings")
plt.ylabel("File Size per Reading (bytes)")
plt.title("File Size per Reading vs. Number of Temperature Readings")
plt.grid(True)
plt.legend()
plt.show()