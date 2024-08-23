import tkinter as tk
from tkinter import ttk
from group_2_data_generator import DataGenerator


class DisplayChart(tk.Tk):

    # Class variables for minimum and maximum temperature thresholds
    _min_temp = 18
    _max_temp = 27

    def __init__(self):
        super().__init__()

        # Canvas dimensions for drawing the chart
        self.canvas_temp_width = 600
        self.canvas_temp_height = 300
        self.canvas_width = 800
        self.canvas_height = 300

        # Initialize pointer for temperature indicator
        self.my_pointer = None
        self.x_dist = 60
        self.y_dist = 5
        self.bar_width = self.x_dist - 6

        self.low_value = 18
        self.high_value = 27
        self.normal_range = [20, 25]
        # Set up the main window
        self.title("Line Chart App")
        self.geometry("800x600")

        # Create a frame for the input and update button
        self.input_frame = ttk.Frame(self)
        self.input_frame.pack(pady=10)

        # Label and entry for new value input
        self.entry_label = ttk.Label(self.input_frame, text="Data range:")
        self.entry_label.grid(row=0, column=0, padx=5)

        self.value_entry = ttk.Entry(self.input_frame)
        self.value_entry.grid(row=0, column=1, padx=5)

        # Button to update the chart with the new value
        self.update_button = ttk.Button(
            self.input_frame, text="Update Chart", command=self.draw_chart
        )
        self.update_button.grid(row=0, column=2, padx=5)

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

        self.normal_range_label = ttk.Label(
            self.info_frame,
            text=f"Normal Range: {self.normal_range[0]}°C to {self.normal_range[1]}°C",
        )
        self.normal_range_label.grid(row=0, column=2, padx=10)

        self.high_value_label = ttk.Label(
            self.info_frame, text=f"High Value: {self.high_value}°C"
        )
        self.high_value_label.grid(row=0, column=3, padx=10)

        generator = DataGenerator(20)
        self.dataset = generator.getTemperatureSensorDataset(-10, 40)

        # Initialize the list of values and draw the initial chart
        self.values = []
        self.values2 = []
        self.draw_chart()

    def draw_chart(self):
        """
        Draw the line chart on the canvas.
        This function clears the canvas and redraws the chart with the current values.
        """
        my_range_start = (
            int(self.value_entry.get()) if self.value_entry.get().isdecimal() else 0
        )
        data_range = [my_range_start, my_range_start + 5]

        self.canvas.delete("all")

        # Draw the Data range label
        data_range_label = f"Data range: {data_range[0]}-{data_range[1]}"
        self.canvas.create_text(
            self.canvas_width / 2,
            20,
            text=data_range_label,
            fill="black",
            font=("Arial", 16),
        )

        # Display the values using both a line chart and a bar chart
        self.values2 = []
        for i in self.dataset[data_range[0] : data_range[1] + 1]:
            self.values2.append(i)

            # Draw the bar chart
            self.rect_top_left = [
                (50 - self.bar_width / 2) + len(self.values2) * self.x_dist,
                280 - (i + 10) * self.y_dist,
            ]
            self.rect_bottom_right = [
                (50 + self.bar_width / 2) + len(self.values2) * self.x_dist,
                280,
            ]
            self.canvas.create_rectangle(
                self.rect_top_left[0],
                self.rect_top_left[1],
                self.rect_bottom_right[0],
                self.rect_bottom_right[1],
                outline="",
                fill="#1f1",
            )

            # Draw the line chart
            if len(self.values2) > 1:
                pre_point = [
                    50 + (len(self.values2) - 1) * self.x_dist,
                    280 - (self.values2[-2] + 10) * self.y_dist,
                ]
                new_point = [
                    50 + len(self.values2) * self.x_dist,
                    280 - (i + 10) * self.y_dist,
                ]
                self.canvas.create_line(
                    new_point[0],
                    new_point[1],
                    pre_point[0],
                    pre_point[1],
                    fill="blue",
                    width=2,
                )


if __name__ == "__main__":
    app = DisplayChart()
    app.mainloop()
