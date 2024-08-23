import json
import paho.mqtt.client as mqtt
import random
import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext
from group_2_util import create_data


class PublisherGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.canvas_temp_width = 600
        self.canvas_temp_height = 300

        self.canvas_width = 800
        self.canvas_height = 300

        self.my_pointer = None
        self.x_dist = 60
        self.y_dist = 5
        self.bar_width = self.x_dist - 6

        self.low_value = 18
        self.high_value = 27
        self.normal_range = [20, 25]
        self.title("Publisher")
        self.geometry("400x600")

        self.input_frame = ttk.Frame(self)
        self.input_frame.pack(pady=10)

        self.entry_label = ttk.Label(self.input_frame, text="Min Temperature:")
        self.entry_label.grid(row=0, column=0, padx=5, pady=5)

        self.min_temperature_entry = ttk.Entry(self.input_frame)
        self.min_temperature_entry.grid(row=0, column=1, padx=5, pady=5)

        self.entry_label = ttk.Label(self.input_frame, text="Max Temperature:")
        self.entry_label.grid(row=1, column=0, padx=5, pady=5)

        self.max_temperature_entry = ttk.Entry(self.input_frame)
        self.max_temperature_entry.grid(row=1, column=1, padx=5, pady=5)

        self.start_button = ttk.Button(
            self.input_frame, text="Start publishing", command=self.start_publishing
        )
        self.start_button.grid(row=2, column=0, padx=5, pady=5)

        self.stop_button = ttk.Button(
            self.input_frame,
            text="Stop publishing",
            command=self.stop_publishing,
            state="disable",
        )
        self.stop_button.grid(row=2, column=2, padx=5, pady=5)

        self.entry_label = ttk.Label(self.input_frame, text="Not publishing")
        self.entry_label.grid(row=3, column=1, padx=5, pady=5)

        self.txt_description = scrolledtext.ScrolledText(
            self.input_frame, width=45, height=27
        )
        self.txt_description.grid(row=4, column=0, padx=5, pady=5, columnspan=3)

        self.is_start = False

    def input_display(self, msg):
        self.txt_description.insert("insert", f"{msg}.\n\n")
        self.txt_description.see("end")

    def start_publishing(self):
        self.entry_label.config(text="publishing...", foreground="green")
        self.min_temperature_entry.config(state="disable")
        self.max_temperature_entry.config(state="disable")
        self.start_button.config(state="disabled")
        self.stop_button.config(state="!disabled")
        self.input_display("Start publishing")
        self.is_start = True
        self.input_frame.after(1000, self.publish)

    def stop_publishing(self):
        self.entry_label.config(text="Not publishing", foreground="black")
        self.min_temperature_entry.config(state="!disable")
        self.max_temperature_entry.config(state="!disable")
        self.start_button.config(state="!disabled")
        self.stop_button.config(state="disabled")
        self.input_display("Stop publishing")
        self.is_start = False

    def publish(self):

        try:
            if self.is_start:
                min_temp = (
                    int(self.min_temperature_entry.get())
                    if self.min_temperature_entry.get().isdecimal()
                    else 0
                )
                max_temp = (
                    int(self.max_temperature_entry.get())
                    if self.max_temperature_entry.get().isdecimal()
                    else 0
                )

                if min_temp >= max_temp:
                    self.is_start = False
                    raise Exception(f"Invaild temperature range.")

                topic = "auto_data"
                missing_transmission = random.randint(1, 100)
                send_index = 0
                sleep_time = 1
                client = mqtt.Client(
                    mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5
                )

                send_index += 1
                data = create_data(min_temp, max_temp)

                if missing_transmission == send_index:
                    print("miss transmission ")
                    self.input_display("miss transmission ")
                    missing_transmission = random.randint(1, 100)
                    send_index = 0

                data_str = json.dumps(data)

                client.connect("mqtt.eclipseprojects.io", 1883, 60)
                client.publish(topic, data_str)
                client.loop()
                print(f"Published data: {data_str}")
                self.input_display(f"Published data: {data_str}")

                client.disconnect()

                self.input_frame.after(1000, self.publish)

        except Exception as inst:
            if self.is_start:
                self.input_frame.after(1000, self.publish)
            self.input_display(f"Warning: {inst.args[0]}.\n")


if __name__ == "__main__":
    app = PublisherGUI()
    app.mainloop()
