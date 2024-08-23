import json
import time

import paho.mqtt.client as mqtt

from group_2_util import create_data


def publish():

    # Create MQTT client
    topic = "auto_data"
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)

    # Connect to the MQTT server
    client.connect("mqtt.eclipseprojects.io", 1883, 60)

    for _ in range(5):

        # Create data
        data = create_data()

        # Convert dict to JSON string
        data_str = json.dumps(data)

        # Publish the data to a topic
        client.publish(topic, data_str)
        print("Published data:", data_str)
        time.sleep(1)

    # Print a message
    print("Data published:", data_str)

    # Close the connection
    client.disconnect()


if __name__ == "__main__":
    publish()
