import random
import time
from group_2_data_generator import DataGenerator
import datetime

start_id = 567


def create_data(min_temp, max_temp):
    global start_id
    missing_data_rate = 0.1
    t_bias = random.randint(-5, 5)

    data_enerator = DataGenerator(1)

    current_temp = (
        round(data_enerator.getTemperatureSensorData(min_temp, max_temp), 2) + t_bias
    )

    data = {
        "id": ""
        + str(int(datetime.datetime.utcnow().timestamp()))
        + "."
        + str(start_id),
        "time": time.asctime(),
        "timestamp": time.time(),
        "outdoor_temperature": current_temp,
        "message": "Hello, this is the temperature in Toronto",
    }

    if random.random() <= missing_data_rate:
        print("drop outdoor_temperature")
        del data["outdoor_temperature"]

    start_id += 1
    return data


def print_data(data):
    print()
    print(f"ID: {data['id']}")
    if "outdoor_temperature" in data:
        print(f"Outdoor Temperature: {data['outdoor_temperature']}")
    print(f"Message: {data['message']}")


if __name__ == "__main__":

    data = create_data(1, 29)
    print_data(data)
    random.random()
