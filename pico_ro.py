#!/usr/bin/python3

import serial        #communicates with the Pico
import sys           #command-line arguments
import numpy as np   #calculations
import time          #current time on PC
import struct        #binary data
import csv           #csv files
import h5py          #hdf5 files
import json          #json files

def temperature_readout(target):

    #opens the serial port
    device_name = 'COM7'
    serial_device = serial.Serial(device_name, timeout=1.0)

    #store (pico_time_us, temperature, pc_time_us, latency_us)
    readings = []

    # 'n' counts how many valid samples have been read
    n = 0
    offset = None  #capture difference between the first sample's PC time and Pico time

    print(f"\n=== Acquiring {target} events ===")

    while n < target:
        line = serial_device.readline()
        if not line:
            continue

        pc_time_us = int(time.time() * 1_000_000)  #python time in microseconds
        text = line.decode(errors='replace').strip()

        words = text.split() #split the output

        #extract: pico_timestamp_us = words[3], temperature = words[5]
        try:
            pico_time_us = int(words[3])
            temperature  = float(words[5])
        except (ValueError, IndexError):
            continue

        #establish offset on the first sample (pico_time_us and pc_time_us share a common reference)
        if offset is None:
            offset = pc_time_us - pico_time_us

        #true latency = difference of the PC time and the Pico time (shifted by offset)
        latency_us = pc_time_us - (pico_time_us + offset)

        readings.append((pico_time_us, temperature, pc_time_us, latency_us))
        n += 1

    serial_device.close()


    #CSV
    csv_filename = f"temp_data_{target}_entries.csv"
    with open(csv_filename, "w", newline='') as f_csv:
        writer = csv.writer(f_csv)
        writer.writerow(["pico_timestamp_us", "temperature", "pc_time_us", "latency_us"])
        writer.writerows(readings)

    #Binary
    #unsigned long long, double, unsigned long long, unsigned long long (format specifier: "QdQQ")
    bin_filename = f"temp_data_{target}_entries.bin"
    with open(bin_filename, "wb") as f_bin:
        for pico_ts, temp, pc_ts, lat_us in readings:
            record_bytes = struct.pack("QdQQ", pico_ts, temp, pc_ts, lat_us)
            f_bin.write(record_bytes)

    #HDF5
    h5_filename = f"temp_data_{target}_entries.h5"
    with h5py.File(h5_filename, "w") as f_h5:
        dt = np.dtype([
            ('pico_timestamp_us', np.uint64),
            ('temperature',       np.float64),
            ('pc_time_us',        np.uint64),
            ('latency_us',        np.uint64)
        ])
        data_array = np.array(readings, dtype=dt)
        f_h5.create_dataset("temperature_data", data=data_array, compression=None)

    #JSON
    json_filename = f"temp_data_{target}_entries.json"
    data_list = []
    for (p_ts, temp, pc_ts, lat_us) in readings:
        entry_dict = {
            "pico_timestamp_us": p_ts,
            "temperature":       temp,
            "pc_time_us":        pc_ts,
            "latency_us":        lat_us
        }
        data_list.append(entry_dict)

    with open(json_filename, "w") as f_json:
        json.dump(data_list, f_json, indent=2)

    print(f"\nData stored in:\n"
          f"  {csv_filename}\n"
          f"  {bin_filename}\n"
          f"  {h5_filename}\n"
          f"  {json_filename}\n")

if __name__ == '__main__':
    n_arg = len(sys.argv)  #command-line argument
    if n_arg == 4:
        start = int(sys.argv[1])
        stop  = int(sys.argv[2])
        step  = int(sys.argv[3])
        actual_stop = (stop // step) * step
        print(f"I will take datasets with the number of events ranging from {start} to {actual_stop}, in steps of {step}")
        for n in range(start, stop, step):
            temperature_readout(n)
    elif n_arg == 2:
        n = int(sys.argv[1])
        temperature_readout(n)
    elif n_arg == 1:
        # infinite mode: reads until the script is terminated
        temperature_readout(float('inf'))
    else:
        print("Usage examples:")
        print("  python pico_ro.py 1000")
        print("  python pico_ro.py 1000 5000 1000")