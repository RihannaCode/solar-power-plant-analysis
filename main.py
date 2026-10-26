
import numpy as np
import matplotlib.pyplot as plt


#* Step 1: Load solar power plant data

data = np.genfromtxt(
    "Plant_1_Generation_Data.csv",
    delimiter=",",
    dtype=str,
    skip_header=1
)

print("Data Shape:", data.shape)
print("First 5 Rows:", data[:5])


#* Step 2: Extract DC and AC power

dc_power = data[:, 3].astype(float)
ac_power = data[:, 4].astype(float)

max_dc = np.max(dc_power)
max_ac = np.max(ac_power)

print("Maximum DC Power:", max_dc)
print("Maximum AC Power:", max_ac)


#* Step 3: Calculate basic statistics

average_dc = np.mean(dc_power)
average_ac = np.mean(ac_power)
minimum_dc = np.min(dc_power)

print("Average DC Power:", average_dc)
print("Average AC Power:", average_ac)
print("Minimum DC Power:", minimum_dc)


#* Step 4: Check active power records

total_records = len(ac_power)
active_records = np.sum(ac_power > 0)

active_percentage = active_records / total_records * 100

print("Total Records:", total_records)
print("Active Records:", active_records)
print("Active Percentage:", active_percentage, "%")


#* Step 5: Find the highest AC power

max_index = np.argmax(ac_power)

peak_power = ac_power[max_index]
peak_time = data[max_index, 0]

print("Peak AC Power:", peak_power)
print("Peak Production Time:", peak_time)


#* Step 6: Compare inverter performance

# Get inverter IDs
inverters = data[:, 2]

# Find unique inverters
unique_inverters = np.unique(inverters)

print("Number of Inverters:", len(unique_inverters))


# Calculate average AC power for each inverter
averages = []

for inverter in unique_inverters:
    power = ac_power[inverters == inverter]
    average = np.mean(power)

    averages.append(average)

    print("Inverter:", inverter, "Average AC Power:", average)


# Convert the list to a NumPy array
averages = np.array(averages)


# Find the inverter with the highest average AC power
best_index = np.argmax(averages)

best_inverter = unique_inverters[best_index]
best_average = averages[best_index]

print("Best Inverter:", best_inverter)
print("Best Average AC Power:", best_average)


#* Step 7: Analyze daily energy production

# Extract dates from the DATE_TIME column
date_time = data[:, 0]

dates = np.array([
    value.split(" ")[0]
    for value in date_time
])

# Find unique dates
unique_dates = np.unique(dates)

print("Number of Days:", len(unique_dates))


# Extract daily energy values
daily_yield = data[:, 5].astype(float)


# Calculate total daily energy for all days
all_daily_energy = []

for date in unique_dates:
    daily_energy = []

    for inverter in unique_inverters:
        mask = (dates == date) & (inverters == inverter)

        if np.any(mask):
            inverter_energy = np.max(daily_yield[mask])
            daily_energy.append(inverter_energy)

    total_energy = np.sum(daily_energy)
    all_daily_energy.append(total_energy)

all_daily_energy = np.array(all_daily_energy)


# Find the day with the highest energy production
best_day_index = np.argmax(all_daily_energy)

best_day = unique_dates[best_day_index]
best_day_energy = all_daily_energy[best_day_index]

print("Best Production Day:", best_day)
print("Daily Energy:", best_day_energy)


# Find the day with the lowest energy production
worst_day_index = np.argmin(all_daily_energy)

worst_day = unique_dates[worst_day_index]
worst_day_energy = all_daily_energy[worst_day_index]

print("Lowest Production Day:", worst_day)
print("Daily Energy:", worst_day_energy)


#* Step 8: Find low production days

# Calculate average daily energy
average_daily_energy = np.mean(all_daily_energy)

# Set the threshold to 90% of the average
threshold = average_daily_energy * 0.9

# Find days with energy below the threshold
low_energy_mask = all_daily_energy < threshold

low_energy_dates = unique_dates[low_energy_mask]
low_energy_values = all_daily_energy[low_energy_mask]

# Count low production days
low_energy_count = len(low_energy_dates)

print("Average Daily Energy:", average_daily_energy)
print("Threshold:", threshold)
print("Low Production Days:", low_energy_count)


# Show the dates and energy values
for date, energy in zip(low_energy_dates, low_energy_values):
    print("Date:", date, "Energy:", energy)



#* Step 9: Visualize daily energy production

# Convert dates to YYYY-MM-DD format
date_values = np.array([
    np.datetime64(
        date[6:10] + "-" + date[3:5] + "-" + date[:2]
    )
    for date in unique_dates
])

# Sort dates and energy values
order = np.argsort(date_values)

sorted_dates = date_values[order]
sorted_energy = all_daily_energy[order]


# Plot daily energy production
plt.figure(figsize=(12, 5))

plt.plot(
    sorted_dates,
    sorted_energy,
    marker="o",
    label="Daily Energy"
)

# Add average daily energy line
plt.axhline(
    y=average_daily_energy,
    color="orange",
    linestyle="--",
    label="Average Daily Energy"
)

# Highlight low production days
plt.scatter(
    sorted_dates[sorted_energy < threshold],
    sorted_energy[sorted_energy < threshold],
    color="red",
    s=80,
    label="Low Production Days",
    zorder=5
)

plt.title("Solar Power Plant - Daily Energy Production")
plt.xlabel("Date")
plt.ylabel("Daily Energy")

plt.xticks(rotation=45)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.show()


#* Step 10: Visualize inverter performance

# Sort inverters by average AC power
order = np.argsort(averages)

sorted_inverters = unique_inverters[order]
sorted_averages = averages[order]


# Plot average AC power for each inverter
plt.figure(figsize=(12, 7))

plt.barh(
    sorted_inverters,
    sorted_averages,
    color="steelblue"
)

plt.title("Solar Power Plant - Inverter Performance")
plt.xlabel("Average AC Power")
plt.ylabel("Inverter ID")

plt.grid(axis="x", alpha=0.3)
plt.tight_layout()

plt.show()