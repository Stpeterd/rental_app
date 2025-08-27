import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import threading
import time

class RentalTimeSheet:
    def __init__(self, root):
        self.root = root
        self.root.title("Rental Time Sheet")
        self.root.geometry("600x500")
        
        # Variables
        self.pickup_datetime = None
        self.return_datetime = None
        self.timer_running = False
        self.timer_thread = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Customer Information
        ttk.Label(main_frame, text="Customer Information", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=4, pady=(0, 10), sticky=tk.W)
        
        ttk.Label(main_frame, text="Customer Name:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        self.customer_name = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.customer_name, width=30).grid(row=1, column=1, columnspan=3, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Label(main_frame, text="Tool Name:").grid(row=2, column=0, sticky=tk.W, padx=(0, 5))
        self.tool_name = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.tool_name, width=30).grid(row=2, column=1, columnspan=3, sticky=(tk.W, tk.E), pady=2)
        
        # Pickup Time Section
        ttk.Label(main_frame, text="Pickup Time", font=("Arial", 12, "bold")).grid(row=3, column=0, columnspan=4, pady=(20, 10), sticky=tk.W)
        
        # Date
        ttk.Label(main_frame, text="Date (YYYY-MM-DD):").grid(row=4, column=0, sticky=tk.W, padx=(0, 5))
        self.pickup_date = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(main_frame, textvariable=self.pickup_date, width=12).grid(row=4, column=1, sticky=tk.W, pady=2)
        
        # Hour
        ttk.Label(main_frame, text="Hour (0-23):").grid(row=5, column=0, sticky=tk.W, padx=(0, 5))
        self.pickup_hour = tk.StringVar(value=str(datetime.now().hour))
        hour_spinbox = tk.Spinbox(main_frame, from_=0, to=23, textvariable=self.pickup_hour, width=5)
        hour_spinbox.grid(row=5, column=1, sticky=tk.W, pady=2)
        
        # Minute
        ttk.Label(main_frame, text="Minute (0-59):").grid(row=6, column=0, sticky=tk.W, padx=(0, 5))
        self.pickup_minute = tk.StringVar(value=str(datetime.now().minute))
        minute_spinbox = tk.Spinbox(main_frame, from_=0, to=59, textvariable=self.pickup_minute, width=5)
        minute_spinbox.grid(row=6, column=1, sticky=tk.W, pady=2)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=4, pady=20)
        
        ttk.Button(button_frame, text="Start Rental", command=self.start_rental).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Return Tool", command=self.return_tool).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_form).pack(side=tk.LEFT, padx=5)
        
        # Results Section
        ttk.Label(main_frame, text="Rental Information", font=("Arial", 12, "bold")).grid(row=8, column=0, columnspan=4, pady=(20, 10), sticky=tk.W)
        
        # Results text area
        self.results_text = tk.Text(main_frame, height=12, width=70, wrap=tk.WORD)
        self.results_text.grid(row=9, column=0, columnspan=4, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for text area
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        scrollbar.grid(row=9, column=4, sticky=(tk.N, tk.S))
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(9, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
    def start_rental(self):
        try:
            # Validate inputs
            if not self.customer_name.get().strip():
                messagebox.showerror("Error", "Please enter customer name")
                return
            
            if not self.tool_name.get().strip():
                messagebox.showerror("Error", "Please enter tool name")
                return
            
            # Parse pickup time
            date_str = self.pickup_date.get()
            hour = int(self.pickup_hour.get())
            minute = int(self.pickup_minute.get())
            
            pickup_date = datetime.strptime(date_str, "%Y-%m-%d")
            self.pickup_datetime = pickup_date.replace(hour=hour, minute=minute)
            
            # Calculate minimum return time (4 hours later)
            min_return_time = self.pickup_datetime + timedelta(hours=4)
            
            # Display rental information
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"RENTAL STARTED\n")
            self.results_text.insert(tk.END, f"{'='*50}\n")
            self.results_text.insert(tk.END, f"Customer: {self.customer_name.get()}\n")
            self.results_text.insert(tk.END, f"Tool: {self.tool_name.get()}\n")
            self.results_text.insert(tk.END, f"Pickup Time: {self.pickup_datetime.strftime('%Y-%m-%d %I:%M %p')}\n")
            self.results_text.insert(tk.END, f"Minimum Return Time: {min_return_time.strftime('%Y-%m-%d %I:%M %p')}\n")
            self.results_text.insert(tk.END, f"Minimum Rental Period: 4 hours\n\n")
            
            # Start timer
            self.timer_running = True
            self.start_timer()
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid date/time format: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def start_timer(self):
        if self.timer_thread and self.timer_thread.is_alive():
            return
            
        self.timer_thread = threading.Thread(target=self.update_timer, daemon=True)
        self.timer_thread.start()
    
    def update_timer(self):
        while self.timer_running and self.pickup_datetime:
            current_time = datetime.now()
            elapsed_time = current_time - self.pickup_datetime
            
            # Calculate hours and minutes
            total_minutes = int(elapsed_time.total_seconds() / 60)
            hours = total_minutes // 60
            minutes = total_minutes % 60
            
            # Update the display in the main thread
            self.root.after(0, self.update_timer_display, hours, minutes, current_time)
            
            time.sleep(60)  # Update every minute
    
    def update_timer_display(self, hours, minutes, current_time):
        if not self.timer_running:
            return
            
        # Find the timer section and update it
        content = self.results_text.get(1.0, tk.END)
        lines = content.split('\n')
        
        # Remove old timer info if it exists
        new_lines = []
        skip_timer = False
        for line in lines:
            if line.startswith("CURRENT STATUS"):
                skip_timer = True
            elif skip_timer and line.strip() == "":
                skip_timer = False
                continue
            elif not skip_timer:
                new_lines.append(line)
        
        # Add current timer info
        timer_info = f"CURRENT STATUS\n"
        timer_info += f"Current Time: {current_time.strftime('%Y-%m-%d %I:%M %p')}\n"
        timer_info += f"Elapsed Time: {hours} hours, {minutes} minutes\n"
        
        if hours >= 4:
            timer_info += f"Status: Past minimum rental period\n"
        else:
            remaining_hours = 4 - hours
            remaining_minutes = 60 - minutes if minutes > 0 else 0
            if remaining_minutes == 60:
                remaining_minutes = 0
                remaining_hours -= 1
            timer_info += f"Status: {remaining_hours} hours, {remaining_minutes} minutes until minimum\n"
        
        timer_info += "\n"
        
        # Update the text widget
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, '\n'.join(new_lines[:-1]))  # Remove last empty line
        self.results_text.insert(tk.END, timer_info)
        
        # Scroll to bottom
        self.results_text.see(tk.END)
    
    def return_tool(self):
        if not self.pickup_datetime:
            messagebox.showerror("Error", "No active rental found. Please start a rental first.")
            return
        
        self.timer_running = False
        self.return_datetime = datetime.now()
        
        # Calculate total rental time
        total_time = self.return_datetime - self.pickup_datetime
        total_hours = total_time.total_seconds() / 3600
        
        # Calculate billable time (minimum 4 hours)
        billable_hours = max(4, total_hours)
        
        # Add return information
        self.results_text.insert(tk.END, f"\nTOOL RETURNED\n")
        self.results_text.insert(tk.END, f"{'='*50}\n")
        self.results_text.insert(tk.END, f"Return Time: {self.return_datetime.strftime('%Y-%m-%d %I:%M %p')}\n")
        self.results_text.insert(tk.END, f"Total Rental Time: {total_hours:.2f} hours\n")
        self.results_text.insert(tk.END, f"Billable Time: {billable_hours:.2f} hours\n")
        
        if total_hours < 4:
            self.results_text.insert(tk.END, f"Note: Minimum 4-hour charge applied\n")
        
        # Scroll to bottom
        self.results_text.see(tk.END)
        
        messagebox.showinfo("Rental Complete", f"Tool returned successfully!\nBillable time: {billable_hours:.2f} hours")
    
    def clear_form(self):
        self.timer_running = False
        self.pickup_datetime = None
        self.return_datetime = None
        
        self.customer_name.set("")
        self.tool_name.set("")
        self.pickup_date.set(datetime.now().strftime("%Y-%m-%d"))
        self.pickup_hour.set(str(datetime.now().hour))
        self.pickup_minute.set(str(datetime.now().minute))
        self.results_text.delete(1.0, tk.END)

def main():
    root = tk.Tk()
    app = RentalTimeSheet(root)
    root.mainloop()

if __name__ == "__main__":
    main()

#need to change layout
