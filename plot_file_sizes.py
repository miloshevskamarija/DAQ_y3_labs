#!/usr/bin/env python3

import os
import matplotlib.pyplot as plt
import numpy as np

def main():

    event_counts = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]

    #lists for storing the file sizes (in bytes) for each format
    csv_sizes = []
    bin_sizes = []
    h5_sizes  = []
    json_sizes = []

    #loops over each number of events and records the file sizes
    for n in event_counts:
        csv_file  = f"temp_data_{n}_entries.csv"
        bin_file  = f"temp_data_{n}_entries.bin"
        h5_file   = f"temp_data_{n}_entries.h5"
        json_file = f"temp_data_{n}_entries.json"

        csv_sizes.append(os.path.getsize(csv_file))
        bin_sizes.append(os.path.getsize(bin_file))
        h5_sizes.append(os.path.getsize(h5_file))
        json_sizes.append(os.path.getsize(json_file))

    #plotting file sizes vs. event counts
    plt.figure(figsize=(8, 5))

    plt.plot(event_counts, csv_sizes,  'o--', label='CSV')
    plt.plot(event_counts, bin_sizes,  's--', label='Binary')
    plt.plot(event_counts, h5_sizes,   '^--', label='HDF5')
    plt.plot(event_counts, json_sizes, 'd--', label='JSON')

    plt.xlabel("Number of Temperature Readings")
    plt.ylabel("File Size (bytes)")
    plt.title("File Size vs. Number of Temperature Readings")
    #plt.title("File Size vs. Number of Temperature Readings (Logarithmic scale)")   ##uncomment if showing the linear relationship
    plt.grid(True)
    plt.legend()
    #plt.yscale('log')   ##uncomment if showing the linear relationship
    plt.show()

if __name__ == "__main__":
    main()