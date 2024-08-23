import datetime
import random
import time

from group_2_data_generator import DataGenerator

# Initialize the starting ID for the data records
start_id = 567


def create_data(min_temp, max_temp):

    # Use the global start_id variable
    global start_id

    # Probability to omit the temperature data
    missing_data_rate = 0.1

    # Random bias for the temperature
    t_bias = random.randint(-5, 5)

    # Generate temperature data using an external data generator class
    data_enerator = DataGenerator(1)
    current_temp_array = data_enerator.getTemperatureSensorDataset(min_temp, max_temp)

    # Adjust the temperature by the bias and round to 2 decimal places
    current_temp = round(current_temp_array[0], 2) + t_bias

    # Create a dictionary to store the data entry
    data = {
        "id": "" + str(int(datetime.datetime.utcnow().timestamp())) + "."
        # Unique ID combining the current timestamp and start_id
        + str(start_id),
        # Current time in a human-readable format
        "time": time.asctime(),
        # Current time as a timestamp
        "timestamp": time.time(),
        # Temperature data
        "outdoor_temperature": current_temp,
        # Sample message
        "message": "Hello, this is the temperature in Toronto",
    }

    # Randomly decide whether to drop the temperature data
    if random.random() <= missing_data_rate:
        print("drop outdoor_temperature")
        del data["outdoor_temperature"]

    # Increment the ID for the next data entry
    start_id += 1

    # Return the created data entry
    return data


def print_data(data):

    # Print the unique ID
    print()
    print(f"ID: {data['id']}")
    if "outdoor_temperature" in data:
        print(f"Outdoor Temperature: {data['outdoor_temperature']}")
    print(f"Message: {data['message']}")


if __name__ == "__main__":
    data = create_data(1, 29)
    print_data(data)
    random.random()
