import os
import json
import struct
import h5py
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#list of event counts
event_counts = list(range(1000, 10001, 1000))

def print_stats(latencies, label): #statistics calculations
    lat_series = pd.Series(latencies)
    mean_val = lat_series.mean()
    median_val = lat_series.median()
    std_val = lat_series.std()
    percentiles = np.percentile(lat_series, [5, 25, 50, 75, 95, 99])

    print(f"Statistics for {label}:")
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
    print("")


### JSON
for n in event_counts:

    json_file = f"temp_data_{n}_entries.json"
    if not os.path.exists(json_file):
        print(f"{json_file} not found. Skipping JSON for {n} entries.")
        continue

    latencies = []
    with open(json_file, "r") as f:
        try:
            data = json.load(f)
            for entry in data:
                try:
                    lat_us = float(entry["latency_us"])
                    latencies.append(lat_us)
                except (ValueError, KeyError):
                    continue
        except json.JSONDecodeError:
            print(f"Error reading {json_file}")
            continue

    if not latencies:
        print(f"No latency data found in {json_file}.")
        continue

    #plotting
    plt.figure(figsize=(8, 5))
    plt.hist(latencies, bins=50, color='lightgreen', edgecolor='black')
    plt.title(f"Latency Distribution (JSON) for {n} Entries")
    plt.xlabel("Latency (microseconds)")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()

    #stats
    print_stats(latencies, f"JSON ({n} entries)")


### Binary
for n in event_counts:
    bin_file = f"temp_data_{n}_entries.bin"
    if not os.path.exists(bin_file):
        print(f"{bin_file} not found. Skipping Binary for {n} entries.")
        continue

    latencies = []
    record_fmt = "QdQQ"  #(uint64, double, uint64, uint64)
    record_size = struct.calcsize(record_fmt)

    with open(bin_file, "rb") as f:
        while True:
            record_bytes = f.read(record_size)
            if not record_bytes or len(record_bytes) < record_size:
                break
            try:
                _, _, _, latency_us = struct.unpack(record_fmt, record_bytes)
                latencies.append(latency_us)
            except struct.error:
                break

    if not latencies:
        print(f"No latency data found in {bin_file}.")
        continue

    #plotting
    plt.figure(figsize=(8, 5))
    plt.hist(latencies, bins=50, color='salmon', edgecolor='black')
    plt.title(f"Latency Distribution (Binary) for {n} Entries")
    plt.xlabel("Latency (microseconds)")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()

    #stats
    print_stats(latencies, f"Binary ({n} entries)")


### HDF5
for n in event_counts:
    h5_file = f"temp_data_{n}_entries.h5"
    if not os.path.exists(h5_file):
        print(f"{h5_file} not found. Skipping HDF5 for {n} entries.")
        continue

    latencies = []
    with h5py.File(h5_file, "r") as hf:
        if "temperature_data" not in hf:
            print(f"'temperature_data' dataset not found in {h5_file}.")
            continue
        dataset = hf["temperature_data"]

        latencies = dataset["latency_us"][:] #extracting the latency

    if latencies.size == 0:
        print(f"No latency data found in {h5_file}.")
        continue

    #plotting
    plt.figure(figsize=(8, 5))
    plt.hist(latencies, bins=50, color='plum', edgecolor='black')
    plt.title(f"Latency Distribution (HDF5) for {n} Entries")
    plt.xlabel("Latency (microseconds)")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()

    #stats
    print_stats(latencies, f"HDF5 ({n} entries)")