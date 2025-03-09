# ###infinite readings
# #!/usr/bin/python3

# import serial
# import sys

# def temperature_readout(target):

#         device_name='COM7'
#         serial_device = serial.Serial(device_name)  # open serial port

#         # event counter
#         n=1

#         # csv file
#         f_csv = open(f"temp_data_{target}_entries.csv", "w")

#         while n<=target:
#                 line = serial_device.readline()
#                 text = line.decode()
                
#                 # extract data
#                 words = text.split()
#                 timestamp = words[3]
#                 temperature = words[5]

#                 data_string=f"{timestamp},{temperature}"

#                 # csv
#                 f_csv.write(data_string+"\n")
#                 print(data_string)

#                 n+=1

#         f_csv.close()

# if __name__ == '__main__':

#         n_arg=len(sys.argv)

#         if n_arg == 4:
#                 start = int(sys.argv[1])
#                 stop = int(sys.argv[2])
#                 step = int(sys.argv[3])
#                 actual_stop=(stop//step)*step
#                 print(f"I will take datasets with the number of events ranging from {start} to {actual_stop}, in steps of {step}")
#                 n_events_range=range(start,stop,step)
#                 for n in n_events_range:
#                         print(f"I will read {n} events")
#                         temperature_readout(n)
#         elif n_arg == 2:
#                 n=int(sys.argv[1])
#                 print(f"I will read {n} events")
#                 temperature_readout(n)
#         elif n_arg == 1:
#                 temperature_readout(float('inf'))
#         else:
#                 print(f"Invalid number of arguments: {n_arg}")

##########################################################################################################################
#!/usr/bin/python3

import serial
import sys
import time
import csv
import matplotlib.pyplot as plt

def temperature_readout(target): 

    device_name = 'COM7'  
    baud_rate   = 115200

    ser = serial.Serial(device_name, baud_rate, timeout=1.0) #opens the serial port
    time.sleep(2)  #small delay to ensure the Pico is ready

    #store data in Python lists
    timestamps = []
    temperatures = []

    #opens a CSV file to save data
    csv_filename = f"temp_data_{target}_entries.csv"
    f_csv = open(csv_filename, "w", newline='')
    csv_writer = csv.writer(f_csv)
    csv_writer.writerow(["timestamp_us", "temperature_C"])  #header row

    print(f"Reading {target} lines from {device_name}...")

    n = 0
    while n < target:
        line = ser.readline().decode(errors='replace').strip()
        if not line:
            continue  #no data received

        parts = line.split(",")
        if len(parts) != 2: #if the line doesn't match the expected format, skip
            continue

        #parse
        try:
            timestamp_us = int(parts[0])
            temperature  = float(parts[1])
        except ValueError:
            continue

        #store in memory
        timestamps.append(timestamp_us)
        temperatures.append(temperature)

        #write to CSV
        csv_writer.writerow([timestamp_us, temperature])
        #print(line)

        n += 1

    #closes the file and serial port
    f_csv.close()
    ser.close()

    print(f"\nData stored in {csv_filename}.")

    ###analysis

    #average temperature
    avg_temp = sum(temperatures) / len(temperatures)

    #average sampling interval from consecutive timestamps
    #i.e the difference in microseconds between consecutive samples
    intervals_us = []
    for i in range(len(timestamps)-1):
        dt = timestamps[i+1] - timestamps[i]
        intervals_us.append(dt)

    avg_interval_us = sum(intervals_us) / len(intervals_us)
    avg_interval_ms = avg_interval_us / 1000.0
    sample_rate_hz  = 1e6 / avg_interval_us  #approximate samples/second

    print(f"\nAnalysis of {len(timestamps)} samples:")
    print(f"  Average temperature:  {avg_temp:.2f} C")
    print(f"  Average interval:     {avg_interval_us:.0f} us  ({avg_interval_ms:.2f} ms)")
    print(f"  Approx. sample rate:  {sample_rate_hz:.1f} Hz")

    ###plotting
    plt.figure(figsize=(10,4))

    #Temperature vs Sample Index
    plt.subplot(1,2,1)
    plt.plot(range(len(temperatures)), temperatures, marker='o', linestyle='-')
    plt.title("Temperature vs. Sample Index")
    plt.xlabel("Sample Index")
    plt.ylabel("Temperature (C)")

    #Interval vs. Index
    plt.subplot(1,2,2)
    plt.plot(range(len(intervals_us)), intervals_us, marker='o', linestyle='-')
    plt.title("Sampling Interval (microseconds)")
    plt.xlabel("Index")
    plt.ylabel("Delta t (µs)")

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    n_args = len(sys.argv)
    if n_args == 2:
        n = int(sys.argv[1])
        temperature_readout(n)
    else:
        print("Usage:")
        print("  python sending.py <N>")
        print("  e.g. python sending.py 10")