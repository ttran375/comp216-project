import json

import paho.mqtt.client as mqtt

from group_2_util import print_data


def on_message(client, userdata, message):

    # Decode the message
    msg_str = message.payload.decode("utf-8")

    # Convert the JSON string to a dictionary
    data = json.loads(msg_str)

    # Print the data using the utility function
    print_data(data)


def subscribe():

    # Create MQTT client
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)

    # Assign the on_message callback function
    client.on_message = on_message

    # Connect to the MQTT server
    client.connect("mqtt.eclipseprojects.io", 1883, 60)

    # Subscribe to the required topic
    client.subscribe("auto_data")

    # Print a message
    print("Subscribed to topic: test/topic")

    # Invoke the client loop_forever method
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nDisconnecting from broker")
        client.disconnect()


if __name__ == "__main__":
    subscribe()
