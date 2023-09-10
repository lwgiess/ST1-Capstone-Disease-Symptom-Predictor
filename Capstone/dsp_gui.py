import tkinter as tk
import numpy as np
from dsp_model import best_model  # Import your trained model from dsp_model.py

class dsp_GUI:
    def __init__(self):
        # Create the main window.
        self.main_window = tk.Tk()
        self.main_window.title("Disease Symptom Predictor")

        # Create frames to group widgets.
        self.input_frame = tk.Frame(self.main_window)
        self.result_frame = tk.Frame(self.main_window)

        # Create labels and entry fields for user input.
        self.labels = [
            "Disease:",
            "Fever (1 for yes, 0 for no):",
            "Cough (1 for yes, 0 for no):",
            "Fatigue (1 for yes, 0 for no):",
            "Difficulty Breathing (1 for yes, 0 for no):",
            "Age (in years):",
            "Gender (1 for male, 0 for female):",
            "Blood Pressure:",
            "Cholesterol Level:"
        ]

        self.input_entries = []

        for i, label_text in enumerate(self.labels):
            label = tk.Label(self.input_frame, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=5)

            entry = tk.Entry(self.input_frame)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.input_entries.append(entry)

        # Create a predict button.
        self.predict_button = tk.Button(self.input_frame, text="Predict", command=self.make_prediction)
        self.predict_button.grid(row=len(self.labels), columnspan=2, padx=10, pady=10)

        # Create a label to display the prediction result.
        self.result_label = tk.Label(self.result_frame, text="")
        self.result_label.pack(padx=10, pady=10)

        # Pack the frames.
        self.input_frame.pack()
        self.result_frame.pack()

        # Enter the tkinter main loop.
        self.main_window.mainloop()

    def make_prediction(self):
        try:
            # Get user input values.
            user_input = [float(entry.get()) for entry in self.input_entries]

            # Make a prediction using the imported model from dsp_model.py.
            prediction = best_model.predict([user_input])

            # Display the prediction result.
            if prediction == 0:
                result = "Low risk of the specified disease."
            else:
                result = "High risk of the specified disease."

            self.result_label.config(text=result)
        except ValueError:
            self.result_label.config(text="Invalid input.")

if __name__ == "__main__":
    my_dsp_GUI = dsp_GUI()
