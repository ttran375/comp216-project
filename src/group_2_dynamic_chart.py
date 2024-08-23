import tkinter as tk
from tkinter import ttk, font
import threading
import time
from group_2_data_generator import DataGenerator


class DynamicChart(tk.Tk):

    def __init__(self):
        super().__init__()

        # Canvas dimensions for drawing the chart
        self.canvas_temp_width = 600
        self.canvas_temp_height = 300
        self.canvas_width = 800
        self.canvas_height = 300

        # Range values for the temperature data
        self.low_value = 18
        self.high_value = 27
        self.x_offset_graph = 40
        self.y_offset_graph = 50
        self.x_max_graph = 590
        self.y_max_graph = 280
        self.is_show_line_chart = True
        self.is_show_bar_chart = False

        # Lists to hold various elements of the chart (e.g., points, lines, bars)
        self.ticks = []
        self.points = []
        self.lines = []
        self.point_labels = []
        self.bars = []
        self.tick_labels = []
        self.is_connected = False

        # Set up the main window
        self.title("Dynamic Line and Bar Chart App")
        self.geometry("800x600")

        # Create a frame for the input and update button
        self.input_frame = ttk.Frame(self)
        self.input_frame.pack(pady=10)

        # Button to toggle data generation (start/pause)
        self.btn_action = ttk.Button(
            self.input_frame, text="Go", command=self.toggle_connection
        )
        self.btn_action.grid(row=0, column=0, padx=5)

        # Button to switch between Line and Bar Charts
        self.btn_switch = ttk.Button(
            self.input_frame, text="Switch Chart", command=self.toggle_chart
        )
        self.btn_switch.grid(row=0, column=1, padx=5)

        # Canvas for drawing the line chart
        self.canvas = tk.Canvas(
            self, width=self.canvas_width, height=self.canvas_height, bg="white"
        )
        self.canvas.pack(pady=10)

        # Frame for additional information display
        self.info_frame = ttk.Frame(self)
        self.info_frame.pack(pady=10)

        # Labels for displaying units and value ranges
        self.units_label = ttk.Label(self.info_frame, text="Units: °C")
        self.units_label.grid(row=0, column=0, padx=10)
        self.low_value_label = ttk.Label(
            self.info_frame, text=f"Low Value: {self.low_value}°C"
        )
        self.low_value_label.grid(row=0, column=1, padx=10)
        self.high_value_label = ttk.Label(
            self.info_frame, text=f"High Value: {self.high_value}°C"
        )
        self.high_value_label.grid(row=0, column=2, padx=10)

        # Start the thread for generating and updating data
        self.data_thread = threading.Thread(target=self.update_data)
        self.data_thread.daemon = True
        self.data_thread.start()

    def draw_chart(self):
        """
        Draw the chart on the canvas. This function clears the canvas and redraws
        the chart with the current set of values. The chart can display either
        a line chart or a bar chart based on the user selection.
        """

        # Clear existing chart elements before drawing the new chart
        self.clear_all_graph()

        # Calculate the width of each tick (X-axis division)
        width_tick = (self.x_max_graph - self.x_offset_graph) / (len(self.ticks) + 1)

        # Calculate the unit height (Y-axis scaling)
        h_unit = (self.y_max_graph - self.y_offset_graph) / (
            self.high_value - self.low_value
        )

        # Loop through the data points (ticks) to draw the chart elements
        for index, tick in enumerate(self.ticks):

            # Store previous tick coordinates to draw lines
            if index > 0:
                x_p = x_center
                y_p = y

            # Calculate the center position for each tick on the X-axis
            x_center = self.x_offset_graph + (index + 1) * width_tick - width_tick / 2

            # Calculate the Y position based on the value of the tick
            y = int(self.y_max_graph - (tick.get("value")[0] - self.low_value) * h_unit)

            # Add labels to indicate data values at the data points
            self.point_labels.append(
                self.canvas.create_text(
                    x_center - 10,
                    y - 15,
                    anchor=tk.W,
                    font=font.Font(size=12, weight="normal"),
                    text="{:.1f}".format(tick.get("value")[0]),
                )
            )

            # Add labels for each tick (X-axis)
            test = 0.5 * len(str(tick.get("index")))
            self.tick_labels.append(
                self.canvas.create_text(
                    x_center - test,
                    self.y_max_graph + 8,
                    anchor=tk.CENTER,
                    fill="green",
                    font=font.Font(size=12, weight="normal"),
                    text=tick.get("index"),
                )
            )

            # Draw bars if bar chart mode is enabled
            if self.is_show_bar_chart:
                self.bars.append(
                    self.canvas.create_rectangle(
                        x_center - width_tick / 4,
                        y,
                        x_center + width_tick / 4,
                        self.y_max_graph,
                        outline="",
                        fill="#1f1",
                    )
                )

            # Draw points and lines if line chart mode is enabled
            if self.is_show_line_chart:
                if not self.is_show_bar_chart:
                    self.points.append(
                        self.canvas.create_oval(
                            x_center - 1,
                            y - 1,
                            x_center + 1,
                            y + 1,
                            outline="red",
                            fill="red",
                            width=1,
                        )
                    )
                if index > 0:
                    self.lines.append(
                        self.canvas.create_line(
                            x_center, y, x_p, y_p, fill="red", smooth=True
                        )
                    )

    def clear_all_graph(self):
        """
        Clear all elements from the canvas before drawing a new chart.
        This ensures that no old elements interfere with the new chart rendering.
        """
        for point in self.points:
            self.canvas.delete(point)
        for line in self.lines:
            self.canvas.delete(line)
        for label in self.point_labels:
            self.canvas.delete(label)
        for label in self.tick_labels:
            self.canvas.delete(label)
        for bar in self.bars:
            self.canvas.delete(bar)
        self.points = []
        self.lines = []
        self.point_labels = []
        self.bars = []
        self.tick_labels = []

    def toggle_chart(self):
        """
        Toggle between displaying the line chart and the bar chart.
        This method is called when the user clicks the "Switch Chart" button.
        """
        self.is_show_bar_chart = not self.is_show_bar_chart
        self.draw_chart()

    def toggle_connection(self):
        """
        Start or pause the data generator.
        This method is called when the user clicks the "Go" button.
        """

        # Change button text to "Pause" when data generation is active
        self.is_connected = not self.is_connected
        if self.is_connected:
            self.btn_action.config(text="Pause")
        else:

            # Change button text to "Go" when data generation is paused
            self.btn_action.config(text="Go")

    def update_data(self):
        """
        Continuously generate new data and update the chart.
        This method runs in a separate thread and updates the chart every 0.5 seconds.
        """
        count = 1
        while True:
            if self.is_connected:

                # Generate new temperature data
                generator = DataGenerator(1)
                new_value = generator.getTemperatureSensorDataset(
                    self.low_value, self.high_value
                )

                # Append the new value to the list of ticks
                self.ticks.append({"index": count, "value": new_value})

                # Keep only the latest 10 ticks (for a clean chart display)
                self.ticks = self.ticks[-10:]

                # Redraw the chart with the updated data
                self.draw_chart()
                count += 1

            # Wait for 0.5 seconds before generating new data
            time.sleep(0.5)


if __name__ == "__main__":
    app = DynamicChart()
    app.mainloop()
