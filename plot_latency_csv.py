import os
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#defines the event counts to loop over
event_counts = list(range(1000, 10001, 1000))

for n in event_counts:
    csv_file = f"temp_data_{n}_entries.csv"
    if not os.path.exists(csv_file):
        print(f"{csv_file} not found. Skipping.")
        continue

    latencies = []
    
    #reads the latency data from the CSV file
    with open(csv_file, "r") as f:
        reader = csv.reader(f)
        header = next(reader)  #skips header row
        for row in reader:
            try:
                latency_us = float(row[3])
                latencies.append(latency_us)
            except (ValueError, IndexError):
                continue

    if not latencies:
        print(f"No latency data found in {csv_file}.")
        continue

    #histogram
    plt.figure(figsize=(8, 5))
    plt.hist(latencies, bins=50, color='skyblue', edgecolor='black')
    plt.title(f"Latency Distribution for {n} Entries")
    plt.xlabel("Latency (microseconds)")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()


##################### stats calculations
datasets = {
    '2k': 'temp_data_2000_entries.csv',
    '3k': 'temp_data_3000_entries.csv',
    '4k': 'temp_data_4000_entries.csv',
    '5k': 'temp_data_5000_entries.csv',
    '6k': 'temp_data_6000_entries.csv',
    '7k': 'temp_data_7000_entries.csv',
    '8k': 'temp_data_8000_entries.csv',
    '9k': 'temp_data_9000_entries.csv',
    '10k': 'temp_data_10000_entries.csv'
}

for label, filename in datasets.items():
    data = pd.read_csv(filename)
    latencies = data['latency_us']
    
    mean_val = latencies.mean()
    median_val = latencies.median()
    std_val = latencies.std()
    percentiles = np.percentile(latencies, [5, 25, 50, 75, 95, 99]) #explains how the data is distributed
                                                                    # i.e. how far out the tail of the distribution extends

    print(f"Dataset {label}:")
    print(f"  Mean: {mean_val:.2f} µs")
    print(f"  Median: {median_val:.2f} µs")
    print(f"  Standard Deviation: {std_val:.2f} µs")
    print("  Percentiles:")
    print(f"    5th: {percentiles[0]:.2f} µs")
    print(f"    25th: {percentiles[1]:.2f} µs")
    print(f"    50th (median): {percentiles[2]:.2f} µs")
    print(f"    75th: {percentiles[3]:.2f} µs")
    print(f"    95th: {percentiles[4]:.2f} µs")
    print(f"    99th: {percentiles[5]:.2f} µs")
    print("\n")