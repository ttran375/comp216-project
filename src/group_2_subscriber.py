import datetime
import json
import os
import threading
import tkinter.scrolledtext as scrolledtext
from tkinter import *
from tkinter import font
from tkinter.ttk import *

import numpy as np
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

from group_2_email_service import GmailService
from group_2_util import print_data

# Load environment variables from a .env file
load_dotenv()


class DynamicDisplayView(Tk):

    def __init__(self):
        Tk.__init__(self)

        # Set window title and dimensions
        self.title("Dynamic Display")
        self.width = 600
        self.height = 450

        # Initialize graph settings and temperature ranges
        self.maxTick = 10
        self.minValue = 16
        self.maxValue = 27
        self.xOffsetGraph = 60
        self.yOffsetGraph = 50
        self.xMaxGraph = 590
        self.yMaxGraph = 300
        self.isShowLineChart = True
        self.isShowBarChart = True

        # Initialize data storage and UI elements
        self.ticks = []
        self.points = []
        self.lines = []
        self.pointLabels = []
        self.bars = []
        self.tickLabels = []
        self.isconnected = False
        self.count = 0
        self.max_temp = 30
        self.min_temp = 0

        # Initialize Gmail credentials and recipient
        self.gmail_account = "comp216group2@gmail.com"
        self.gmail_token = "bhxp ajov ktna vnwm"
        self.reciever = "gavinlikewind@gmail.com"

        # Create the main canvas and UI container
        Canvas(self, width=self.width, height=self.height).pack(padx=20, pady=20)
        container = Frame(self)
        container.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)
        self.create_ui(container)

        # Set UI styling
        style = Style()
        style.theme_use("clam")
        style.configure(".", bd=0, background="white")
        style.configure("CustomButton.TButton", bd=4, background="white")
        style.configure("CustomCombobox.TCombobox", background="lightgray")
        style.configure("TLabel", background="lightgray")

    # Method to create UI elements within the parent frame
    def create_ui(self, parent=None):
        if not parent:
            parent = self

        # Create the header with buttons for actions
        header = Frame(parent, style="TLabel")
        header.pack(fill="x")
        Label(header, text="===============================", width=21).pack(side=LEFT)
        self.btnAction = Button(
            header,
            command=self.toggleConnection,
            text="Go",
            style="CustomButton.TButton",
        )
        self.btnAction.pack(side=LEFT, padx=5)
        self.btnSwitch = Button(
            header,
            command=self.toggleChart,
            text="Switch",
            style="CustomButton.TButton",
        )
        self.btnSwitch.pack(side=LEFT, padx=5)
        Label(header, text="===============================", width=21).pack(side=LEFT)

        # Create the main canvas for displaying the chart
        self.canvas = Canvas(parent, background="pink")
        self.canvas.create_text(
            self.width / 2 - 80,
            20,
            anchor=W,
            font=font.Font(size=16, weight="normal"),
            text="Temperature Over Time",
        )

        # Create X and Y axes on the canvas
        self.createXAxis()
        self.createYAxis()
        self.canvas.pack(fill=BOTH, expand=1)

        # Create the footer with a scrolled text box for logs
        footer = Frame(parent, style="TLabel")
        footer.pack(fill="x")
        self.txt_description = scrolledtext.ScrolledText(
            footer, width=(self.width - 20), height=5
        )
        self.txt_description.pack(side=LEFT, padx=5)

    # Method to create the Y-axis on the canvas
    def createYAxis(self):
        self.canvas.create_text(
            self.width / 2,
            self.yMaxGraph + 60,
            anchor=W,
            font=font.Font(size=14, weight="normal"),
            text="Time",
        )
        self.canvas.create_line(
            self.xOffsetGraph,
            self.yMaxGraph,
            self.xMaxGraph,
            self.yMaxGraph,
            arrow=LAST,
        )

        # Determine the number of labels and spacing on the Y-axis
        numLabel = (
            int(self.maxValue / 5) + 1
            if int(self.maxValue % 5) > 0
            else int(self.maxValue / 5)
        )
        numLabel = numLabel + 1
        hInterval = (self.yMaxGraph - self.yOffsetGraph) / numLabel

        # Create the labels and markers on the Y-axis
        for index in range(0, numLabel):
            if index != 0:
                self.canvas.create_line(
                    self.xOffsetGraph - 5,
                    self.yMaxGraph - hInterval * index,
                    self.xOffsetGraph,
                    self.yMaxGraph - hInterval * index,
                )

            markerLabel = 5 * index
            if markerLabel >= 10:
                self.canvas.create_text(
                    self.xOffsetGraph - 25,
                    self.yMaxGraph - hInterval * index,
                    anchor=W,
                    font=font.Font(size=14, weight="normal"),
                    text=markerLabel,
                )
            else:
                self.canvas.create_text(
                    self.xOffsetGraph - 18,
                    self.yMaxGraph - hInterval * index,
                    anchor=W,
                    font=font.Font(size=14, weight="normal"),
                    text=markerLabel,
                )

    # Method to create the X-axis on the canvas
    def createXAxis(self):
        self.canvas.create_text(
            20,
            self.height / 2,
            anchor=W,
            angle=90,
            font=font.Font(size=14, weight="normal"),
            text="Temperature(℃)",
        )
        self.canvas.create_line(
            self.xOffsetGraph,
            self.yMaxGraph,
            self.xOffsetGraph,
            self.yOffsetGraph,
            arrow=LAST,
        )

    # Method to update the chart with new data
    def updateChart(self):

        # Clear the existing graph
        self.clearAllGraph()
        x_p = 0
        y_p = 0

        # Calculate the width for each tick on the X-axis
        widthTick = (self.xMaxGraph - self.xOffsetGraph) / (self.maxTick + 1)

        # Determine the number of labels and unit height for the Y-axis
        numLabel = (
            int(self.maxValue / 5) + 1
            if int(self.maxValue % 5) > 0
            else int(self.maxValue / 5)
        )
        numLabel = numLabel + 1
        hUnit = (self.yMaxGraph - self.yOffsetGraph) / numLabel / 5

        # Loop through the data ticks and update the chart
        for index, tick in enumerate(self.ticks):
            if index > 0:
                x_p = xCenter
                y_p = y
            xCenter = self.xOffsetGraph + (index + 1) * widthTick - widthTick / 2
            y = int(self.yMaxGraph - (np.float64(tick.get("value")) * hUnit))

            # Add labels for the points on the chart
            self.pointLabels.append(
                self.canvas.create_text(
                    xCenter - 10,
                    y - 15,
                    anchor=W,
                    font=font.Font(size=12, weight="normal"),
                    text="{:.1f}".format(tick.get("value")[0]),
                )
            )

            # Add timestamp labels below the X-axis
            test = 0.5 * len(str(tick.get("index")))
            timestamp_datetime = datetime.datetime.fromtimestamp(tick.get("timestamp"))
            timestamp_str = timestamp_datetime.strftime("%H:%M:%S")
            self.tickLabels.append(
                self.canvas.create_text(
                    xCenter - test,
                    self.yMaxGraph + 25,
                    anchor=CENTER,
                    fill="green",
                    angle=-45,
                    font=font.Font(size=12, weight="normal"),
                    text=timestamp_str,
                )
            )

            # Add bars or lines depending on the chart type
            if self.isShowBarChart:
                self.bars.append(
                    self.canvas.create_rectangle(
                        xCenter - widthTick / 4,
                        y,
                        xCenter + widthTick / 4,
                        self.yMaxGraph,
                        outline="",
                        fill="#1f1",
                    )
                )
            if self.isShowLineChart:
                if not self.isShowBarChart:
                    self.points.append(
                        self.canvas.create_oval(
                            xCenter - 1,
                            y - 1,
                            xCenter + 1,
                            y + 1,
                            outline="red",
                            fill="red",
                            width=1,
                        )
                    )
                if index > 0:
                    self.lines.append(
                        self.canvas.create_line(
                            xCenter, y, x_p, y_p, fill="red", smooth=True
                        )
                    )

    # Method to clear all elements from the graph
    def clearAllGraph(self):
        for point in self.points:
            self.canvas.delete(point)
        for line in self.lines:
            self.canvas.delete(line)
        for label in self.pointLabels:
            self.canvas.delete(label)
        for label in self.tickLabels:
            self.canvas.delete(label)
        for bar in self.bars:
            self.canvas.delete(bar)
        self.points = []
        self.lines = []
        self.pointLabels = []
        self.bars = []
        self.tickLabels = []

    # Method to toggle between bar chart and line chart display
    def toggleChart(self):
        self.isShowBarChart = not self.isShowBarChart
        self.updateChart()

    # Method to toggle the connection status
    def toggleConnection(self):
        self.isconnected = not self.isconnected
        if self.isconnected:
            self.btnAction.config(text="Pause")
        else:
            self.btnAction.config(text="Go")

    # Method to update the data and chart with new MQTT messages
    def updateData(self, message):

        if self.isconnected:
            try:
                self.count += 1

                # Check if the temperature value is present
                if "outdoor_temperature" not in message:
                    raise Exception("Missing value.")
                newValue = message["outdoor_temperature"]

                # Validate the data type of the temperature value
                if type(newValue) not in (int, float, complex):
                    raise Exception("Wrong data type.")

                # Check if the temperature is within the expected range
                if newValue > self.max_temp or newValue < self.min_temp:
                    print("out range")
                    self.txt_description.insert(
                        "end",
                        f"The temperature value {newValue} is outside the normal outdoor temperature range from {self.min_temp} to {self.max_temp}.\n",
                    )

                    # Send an email if the temperature is out of range
                    dataThead = threading.Thread(target=self.send_email(newValue))
                    dataThead.daemon = True
                    dataThead.start()

                else:
                    self.txt_description.insert(
                        "end", f"The new temperature is {newValue}.\n"
                    )

                self.txt_description.see("end")

                # Add the new value to the ticks list and update the chart
                newValue = [message["outdoor_temperature"]]
                self.ticks.append(
                    {
                        "index": self.count,
                        "value": newValue,
                        "timestamp": message["timestamp"],
                    }
                )
                self.ticks = self.ticks[-self.maxTick :]
                self.updateChart()

            except Exception as inst:
                self.txt_description.insert("end", f"Warning: {inst.args[0]}.\n")

    # Method to send an email alert if the temperature is out of range
    def send_email(self, newValue):
        gmail_smtp = GmailService(
            os.getenv("GMAIL_USER"),
            os.getenv("GMAIL_PASSWORD"),
            os.getenv("RECIPIENT_EMAIL"),
        )
        gmail_smtp.set_subject("Outdoor temperature is out of range")
        gmail_smtp.set_body(
            user_input=newValue, normal_low=self.min_temp, normal_high=self.max_temp
        )
        gmail_smtp.send_email()


# Callback function to handle incoming MQTT messages
def on_message(client, userdata, message):

    # Decode the message payload
    msg_str = message.payload.decode("utf-8")

    # Parse the JSON data
    data = json.loads(msg_str)
    print_data(data)

    # Update the application with the new data
    app.updateData(data)


# Create an MQTT client and set the message callback function
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
client.on_message = on_message


# Function to subscribe to the MQTT topic and start listening for messages
def subscribe():

    # Connect to the broker
    client.connect("mqtt.eclipseprojects.io", 1883, 60)

    # Subscribe to the specified topic
    client.subscribe("auto_data")
    print("Subscribed to topic: test/topic")

    try:

        # Start the MQTT client loop
        client.loop_start()
    except KeyboardInterrupt:

        # Disconnect from the broker
        print("\nDisconnecting from broker")
        client.disconnect()


# Function to unsubscribe from the MQTT topic and stop listening for messages
def unsubscribe():
    client.loop_stop()
    client.disconnect()


app = DynamicDisplayView()
subscribe()
app.mainloop()
