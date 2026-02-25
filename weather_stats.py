import statistics

weather_data = [
    {"date": "25 Feb", "temp_high": 34, "temp_low": 19, "humidity": 21},
    {"date": "26 Feb", "temp_high": 33, "temp_low": 19, "humidity": 23},
    {"date": "27 Feb", "temp_high": 32, "temp_low": 18, "humidity": 32},
    {"date": "28 Feb", "temp_high": 33, "temp_low": 18, "humidity": 27},
    {"date": "1 Mar",  "temp_high": 34, "temp_low": 16, "humidity": 22},
    {"date": "2 Mar",  "temp_high": 34, "temp_low": 16, "humidity": 23},
    {"date": "3 Mar",  "temp_high": 37, "temp_low": 19, "humidity": 17},
    {"date": "4 Mar",  "temp_high": 38, "temp_low": 19, "humidity": 8},
    {"date": "5 Mar",  "temp_high": 39, "temp_low": 19, "humidity": 11},
    {"date": "6 Mar",  "temp_high": 38, "temp_low": 18, "humidity": 7},
    {"date": "7 Mar",  "temp_high": 38, "temp_low": 18, "humidity": 14},
    {"date": "8 Mar",  "temp_high": 38, "temp_low": 18, "humidity": 9},
    {"date": "9 Mar",  "temp_high": 38, "temp_low": 18, "humidity": 10},
    {"date": "10 Mar", "temp_high": 38, "temp_low": 18, "humidity": 8},
    {"date": "11 Mar", "temp_high": 38, "temp_low": 19, "humidity": 9},
]

# Extract data
temp_highs = [d['temp_high'] for d in weather_data]
temp_lows = [d['temp_low'] for d in weather_data]
humidities = [d['humidity'] for d in weather_data]

# Calculate averages
avg_temp_high = sum(temp_highs) / len(temp_highs)
avg_temp_low = sum(temp_lows) / len(temp_lows)
avg_humidity = sum(humidities) / len(humidities)

# Calculate medians
median_temp_high = statistics.median(temp_highs)
median_temp_low = statistics.median(temp_lows)
median_humidity = statistics.median(humidities)

# Store results in a text file
with open('weather_results.txt', 'w') as f:
    f.write(f"Average High Temperature: {avg_temp_high:.2f}°C\n")
    f.write(f"Median High Temperature: {median_temp_high}°C\n")
    f.write(f"Average Low Temperature: {avg_temp_low:.2f}°C\n")
    f.write(f"Median Low Temperature: {median_temp_low}°C\n")
    f.write(f"Average Humidity: {avg_humidity:.2f}%\n")
    f.write(f"Median Humidity: {median_humidity}%\n")

print("Results saved to weather_results.txt")