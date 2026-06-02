import tkinter as tk
from tkinter import messagebox
import pyautogui
import keyboard
import time
import csv
import os
from datetime import datetime

# ==========================================
# WATERMARK & COPYRIGHT
# Author: [Faizan]
# Date: June 2026
# Description: ModMark Automation Assistant
# ==========================================

class ModMarkAutomator:
    def __init__(self, root):
        self.root = root
        self.root.title("ModMark Automator")
        
        # Increased window size to ensure all UI elements fit comfortably
        self.root.geometry("450x680")
       

        #Keep window on top even upon button click
        #Set the top_window on top of the root window
        self.root.wm_attributes("-topmost", True)
        
        # Intercept the 'X' button to save data before closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # State Variables
        self.coords = {'0_mark': None, '1_mark': None, 'na_mark': None, 'submit': None}
        self.is_running = False
        self.ui_delay = 0.05
        
        # Analytics Variables
        self.marks_completed = 0
        self.session_active_time = 0.0 # Total seconds running from previous start/stops
        self.current_start_time = None

        self.create_widgets()

    def create_widgets(self):
        # --- INSTRUCTIONS ---
        tk.Label(self.root, text="Step 1: Set Coordinates", font=("Helvetica", 11, "bold")).pack(pady=(15, 2))
        tk.Label(self.root, text="Click a button below. You have 3 seconds\nto hover your mouse over the target on ModMark.", font=("Helvetica", 9)).pack()

        # --- COORDINATE SETTERS ---
        self.btn_0 = tk.Button(self.root, text="Set 0 Mark Coord", command=lambda: self.get_coord('0_mark', self.lbl_0))
        self.btn_0.pack(pady=2)
        self.lbl_0 = tk.Label(self.root, text="Not Set", fg="red")
        self.lbl_0.pack()

        self.btn_1 = tk.Button(self.root, text="Set 1 Mark Coord", command=lambda: self.get_coord('1_mark', self.lbl_1))
        self.btn_1.pack(pady=2)
        self.lbl_1 = tk.Label(self.root, text="Not Set", fg="red")
        self.lbl_1.pack()

        self.btn_na = tk.Button(self.root, text="Set N/A Coord", command=lambda: self.get_coord('na_mark', self.lbl_na))
        self.btn_na.pack(pady=2)
        self.lbl_na = tk.Label(self.root, text="Not Set", fg="red")
        self.lbl_na.pack()

        self.btn_sub = tk.Button(self.root, text="Set Submit Coord", command=lambda: self.get_coord('submit', self.lbl_sub))
        self.btn_sub.pack(pady=2)
        self.lbl_sub = tk.Label(self.root, text="Not Set", fg="red")
        self.lbl_sub.pack()

        # --- KEY BINDINGS ---
        tk.Label(self.root, text="Step 2: Set Key Bindings", font=("Helvetica", 11, "bold")).pack(pady=(15, 2))
        
        frame_keys = tk.Frame(self.root)
        frame_keys.pack()

        tk.Label(frame_keys, text="0 Mark Key:").grid(row=0, column=0, padx=5)
        self.entry_key_0 = tk.Entry(frame_keys, width=5)
        self.entry_key_0.insert(0, "0") # Default set to '0'
        self.entry_key_0.grid(row=0, column=1, padx=5)

        tk.Label(frame_keys, text="1 Mark Key:").grid(row=1, column=0, padx=5)
        self.entry_key_1 = tk.Entry(frame_keys, width=5)
        self.entry_key_1.insert(0, "1") # Default set to '1'
        self.entry_key_1.grid(row=1, column=1, padx=5)

        tk.Label(frame_keys, text="N/A Key:").grid(row=2, column=0, padx=5)
        self.entry_key_na = tk.Entry(frame_keys, width=5)
        self.entry_key_na.insert(0, "6") # Default set to '6'
        self.entry_key_na.grid(row=2, column=1, padx=5)

        # --- RUN CONTROLS ---
        tk.Label(self.root, text="Step 3: Run", font=("Helvetica", 11, "bold")).pack(pady=(15, 2))
        self.btn_start = tk.Button(self.root, text="Start Automation", bg="green", fg="white", command=self.start_automation)
        self.btn_start.pack(pady=2)
        
        self.btn_stop = tk.Button(self.root, text="Stop Automation", bg="red", fg="white", command=self.stop_automation, state=tk.DISABLED)
        self.btn_stop.pack(pady=2)

        # --- SESSION STATS ---
        tk.Label(self.root, text="Live Performance", font=("Helvetica", 11, "bold")).pack(pady=(15, 2))
        self.lbl_stats = tk.Label(self.root, text="Answers Marked: 0", font=("Helvetica", 10), fg="blue")
        self.lbl_stats.pack()
        
        # New label for the live rate
        self.lbl_rate = tk.Label(self.root, text="Current Rate: 0.0 / min", font=("Helvetica", 10, "bold"), fg="purple")
        self.lbl_rate.pack()

    def get_coord(self, target, label):
        """Waits 3 seconds, grabs mouse position, and updates UI."""
        self.root.config(cursor="watch")
        self.root.update()
        time.sleep(3)
        x, y = pyautogui.position()
        self.coords[target] = (x, y)
        label.config(text=f"Set: ({x}, {y})", fg="green")
        self.root.config(cursor="")

    def perform_click(self, coord_key):
        """Executes the automated clicking and logs the stat."""
        if not self.is_running: return
        target_coord = self.coords.get(coord_key)
        submit_coord = self.coords.get('submit')
        
        if target_coord and submit_coord:
            pyautogui.click(x=target_coord[0], y=target_coord[1])
            time.sleep(self.ui_delay)
            pyautogui.click(x=submit_coord[0], y=submit_coord[1])
            
            # Increment the counter and update the UI
            self.marks_completed += 1
            self.lbl_stats.config(text=f"Answers Marked: {self.marks_completed}")
            
            # Instantly update the rate display upon a successful click
            self.calculate_live_rate()

    def start_automation(self):
        if None in self.coords.values():
            messagebox.showwarning("Missing Data", "Please set all 4 coordinates first.")
            return

        self.is_running = True
        self.current_start_time = time.time() # Start the timer
        
        self.btn_start.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)

        keyboard.add_hotkey(self.entry_key_0.get(), lambda: self.perform_click('0_mark'))
        keyboard.add_hotkey(self.entry_key_1.get(), lambda: self.perform_click('1_mark'))
        keyboard.add_hotkey(self.entry_key_na.get(), lambda: self.perform_click('na_mark'))
        
        # Kick off the background loop that updates the live rate

        self.update_live_timer()

    def update_live_timer(self):
        """A looping function that updates the live rate every 1 second."""
        if self.is_running:
            self.calculate_live_rate()
            # Schedule this function to run again in 1000 milliseconds
            self.root.after(1000, self.update_live_timer)

    def calculate_live_rate(self):
        """Calculates the current rate per minute based on total active time."""
        if not self.current_start_time: return
        
        # Total time is previously logged time PLUS time in the current active burst
        total_seconds = self.session_active_time + (time.time() - self.current_start_time)
        elapsed_minutes = total_seconds / 60
        
        if elapsed_minutes > 0:
            live_rate = self.marks_completed / elapsed_minutes
        else:
            live_rate = 0.0
            
        self.lbl_rate.config(text=f"Current Rate: {live_rate:.1f} / min")

    def stop_automation(self):
        self.is_running = False
        keyboard.unhook_all()
        
        # Calculate how long it was running and add to total time
        if self.current_start_time:
            self.session_active_time += (time.time() - self.current_start_time)
            self.current_start_time = None
            
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        self.lbl_rate.config(text=f"Current Rate: Paused", fg="grey")
        messagebox.showinfo("Stopped", "Automation paused.")
        

    def export_data(self):
        """Calculates rates and saves to a CSV file."""
        # If they close the app while it is still running, capture the final time
        if self.is_running and self.current_start_time:
            self.session_active_time += (time.time() - self.current_start_time)
            
        # Only export if they actually marked something
        if self.marks_completed == 0 or self.session_active_time == 0:
            return

        elapsed_minutes = self.session_active_time / 60
        elapsed_hours = self.session_active_time / 3600

        rate_per_min = self.marks_completed / elapsed_minutes if elapsed_minutes > 0 else 0
        rate_per_hour = self.marks_completed / elapsed_hours if elapsed_hours > 0 else 0

        filename = "ModMark_Statistics.csv"
        file_exists = os.path.isfile(filename)

        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Date", "Active Duration (Mins)", "Marks Completed", "Rate/Min", "Rate/Hour"])

            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([
                current_date, 
                round(elapsed_minutes, 2), 
                self.marks_completed, 
                round(rate_per_min, 1), 
                round(rate_per_hour, 1)
            ])

    def on_closing(self):
        """Triggered when the user clicks the standard Window 'X'."""
        self.export_data()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ModMarkAutomator(root)
    root.mainloop()
