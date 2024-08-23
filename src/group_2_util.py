import random
import time

# Initialize a starting ID
start_id = 567


def create_data():
    global start_id
    """
    Function to create a dictionary of data related to either a patient or a car.
    Depending on the context, the data includes patient health metrics or car specifications.
    """

    # Patient information (commented out)
    patient = "Carrie Fisher"

    # Data structure for patient information
    data = {
        # Incremented sequence number  for each new data
        "id": start_id,
        # Name of the patient
        "patient": patient,
        # Current time when the data is generated
        "time": time.asctime(),
        # Simulated heart rate
        "heart_rate": int(random.gauss(80, 1)),
        # Simulated respiratory rate
        "respiratory_rate": int(random.gauss(12, 2)),
        # Fixed heart rate variability
        "heart_rate_variability": 65,
        # Simulated body temperature
        "body_temperature": random.gauss(99, 0.5),
        # Nested dictionary for blood pressure values
        "blood_pressure": {
            # Simulated systolic pressure
            "systolic": int(random.gauss(105, 2)),
            # Simulated diastolic pressure
            "diastolic": int(random.gauss(70, 1)),
        },
        # Current activity of the patient
        "activity": "Walking",
        # Message field with test content
        "message": "Hello, this is a COMP216 test message",
    }

    # Data structure for car information
    data_car = {
        # Fixed sequence number
        "id": 567,
        # Car make
        "make": "Honda",
        # Car model
        "model": "Civic Type-R",
        # Simulated horsepower
        "housepower": int(random.gauss(300, 2)),
        # Manufacture time (current time for simulation)
        "maketime": time.asctime(),
        # Drivetrain information
        "drivetrain": "6-speed manual transmission",
        # Nested dictionary for car dimensions
        "dimensions": {
            # Simulated height of the car
            "height": int(random.gauss(1406, 10)),
            # Simulated width of the car
            "width": int(random.gauss(1889, 9)),
            # Simulated wheelbase of the car (typo corrected from 'weelbase')
            "weelbase": int(random.gauss(2735, 8)),
        },
        # Message field with test content
        "message": "Hello, this is a COMP216 test message",
    }

    # Increment the start ID for the next data entry
    start_id += 1

    # Return the car data (you can switch to return 'data' if patient data is needed)
    return data_car


def print_data(data):
    """
    Function to print out car data in a formatted manner.
    Takes a dictionary as input and prints each field.
    """
    print()
    print(f"ID: {data['id']}")
    print(f"Make: {data['make']}")
    print(f"Model: {data['model']}")
    print(f"Housepower: {data['housepower']}")
    print(f"Manufacture Time: {data['maketime']}")
    print(f"Drivetrain: {data['drivetrain']}")
    print(f"Dimension:")
    print(f"   Height: {data['dimensions']['height']}")
    print(f"   Width: {data['dimensions']['width']}")
    print(f"   Wheelbase: {data['dimensions']['weelbase']}")
    print(f"Message: {data['message']}")


if __name__ == "__main__":
    data = create_data()
    print_data(data)
