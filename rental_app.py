import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

def calculate_rental_cost():
    try:
        # Get pickup and return times from the input fields
        pickup_time_str = pickup_entry.get()
        return_time_str = return_entry.get()

        # Convert strings to datetime objects
        # We assume the dates are the same for simplicity
        pickup_time = datetime.strptime(pickup_time_str, '%I:%M %p')
        return_time = datetime.strptime(return_time_str, '%I:%M %p')

        # --- Core Calculation Logic ---
        
        # 1. Calculate Minimum Return Time
        min_return_time = pickup_time + timedelta(hours=4)
        min_return_label.config(text=f"Minimum Return Time: {min_return_time.strftime('%I:%M %p')}")

        # 2. Calculate Total Rental Duration
        duration = return_time - pickup_time
        duration_hours = duration.total_seconds() / 3600

        # Enforce the 4-hour minimum
        if duration_hours < 4:
            duration_hours = 4

        duration_label.config(text=f"Total Rental Duration: {duration_hours:.2f} hours")

        # 3. Calculate Total Cost
        # Sample pricing: $25 for the 4-hour minimum, $5 per additional hour
        min_cost = 25.0
        hourly_rate = 5.0

        if duration_hours <= 4:
            total_cost = min_cost
        else:
            additional_hours = duration_hours - 4
            total_cost = min_cost + (additional_hours * hourly_rate)

        cost_label.config(text=f"Total Cost: ${total_cost:.2f}")

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter times in the format 'HH:MM AM/PM' (e.g., 01:00 PM)")

# --- GUI Setup ---
root = tk.Tk()
root.title("Rental Time Sheet")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

# Input Frame
input_frame = tk.Frame(root, bg="#f0f0f0", padx=10, pady=10)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Pickup Time (HH:MM AM/PM):", bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=5)
pickup_entry = tk.Entry(input_frame)
pickup_entry.grid(row=0, column=1, pady=5, padx=5)

tk.Label(input_frame, text="Actual Return Time (HH:MM AM/PM):", bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=5)
return_entry = tk.Entry(input_frame)
return_entry.grid(row=1, column=1, pady=5, padx=5)

# Calculate Button
calc_button = tk.Button(root, text="Calculate Rental", command=calculate_rental_cost, bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"))
calc_button.pack(pady=10)

# Output Frame
output_frame = tk.Frame(root, bg="#f0f0f0", padx=10, pady=10)
output_frame.pack(pady=10)

min_return_label = tk.Label(output_frame, text="Minimum Return Time:", bg="#f0f0f0", font=("Helvetica", 10))
min_return_label.pack(anchor="w", pady=5)

duration_label = tk.Label(output_frame, text="Total Rental Duration:", bg="#f0f0f0", font=("Helvetica", 10))
duration_label.pack(anchor="w", pady=5)

cost_label = tk.Label(output_frame, text="Total Cost:", bg="#f0f0f0", font=("Helvetica", 10, "bold"))
cost_label.pack(anchor="w", pady=5)

# Run the application
root.mainloop()

#needs more detail
