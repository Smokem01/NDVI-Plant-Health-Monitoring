import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import schedule
import time
from datetime import datetime
import os
from PIL import Image, ImageTk
import cv2
from daily_checker import schedule_capture

class NDVIMonitoringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NDVI Plant Health Monitoring")
        self.root.geometry("800x600")
        
        self.monitoring_thread = None
        self.is_monitoring = False

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")        
        self.control = ttk.Frame(self.notebook)
        self.res = ttk.Frame(self.notebook)
        self.notebook.add(self.control, text="Control Panel")
        self.notebook.add(self.res, text="Latest Results")
        
        self.setup_control()
        self.setup_res()

    def setup_control(self):
        self.status_label = ttk.Label(self.control, text="Status: Not Monitoring")
        self.status_label.pack(pady=20)
        self.toggle_button = ttk.Button(self.control, text="Start Monitoring",command=self.on_off_monitor)
        self.toggle_button.pack(pady=10)
        self.schedule_label = ttk.Label(self.control, text="Next scheduled run: Not set")
        self.schedule_label.pack(pady=20)
        self.log = scrolledtext.ScrolledText(self.control, height=10)
        self.log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def setup_res(self):
        img_frame = ttk.Frame(self.res)
        img_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        txt_frame = ttk.Frame(self.res)
        txt_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.img_label = ttk.Label(img_frame)
        self.img_label.pack()
        
        self.res_txt = scrolledtext.ScrolledText(txt_frame, height=20)
        self.res_txt.pack(fill=tk.BOTH, expand=True)
        
        refresh_button = ttk.Button(self.res, text="Refresh Results",command=self.refresh_results)
        refresh_button.pack(pady=10)

    def on_off_monitor(self):
        if self.is_monitoring:
            self.monitor_off()
        else:
            self.monitor_on()

    def monitor_on(self):
        self.is_monitoring = True
        self.toggle_button.config(text="Stop Monitoring")
        self.status_label.config(text="Status: Monitoring Active")
        self.log_message("Monitoring started")
        self.monitoring_thread = threading.Thread(target=self.monitoring)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()

    def monitor_off(self):
        self.is_monitoring = False
        self.toggle_button.config(text="Start Monitoring")
        self.status_label.config(text="Status: Not Monitoring")
        self.log_message("Monitoring stopped")

    def monitoring(self):
        while self.is_monitoring:
            schedule_capture()
            schedule.run_pending()
            next_run = schedule.next_run()
            if next_run:
                self.root.after(0, self.update_schedule_label, next_run)
            time.sleep(1)

    def update_schedule_label(self, next_run):
        self.schedule_label.config(text=f"Next scheduled run: {next_run}")

    def log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log.see(tk.END)

    def refresh_results(self):
        results_dir = 'results'
        if not os.path.exists(results_dir):
            self.log_message("No results directory found")
            return
        
        vis_files = [f for f in os.listdir(results_dir) if f.startswith('result-vis-')]
        if vis_files:
            latest_vis = max(vis_files)
            image_path = os.path.join(results_dir, latest_vis)
            self.display_image(image_path)

        txt_files = [f for f in os.listdir(results_dir) if f.startswith('result-') and f.endswith('.txt')]
        if txt_files:
            latest_txt = max(txt_files)
            self.display_analysis(os.path.join(results_dir, latest_txt))

    def display_image(self, image_path):
        try:
            img = Image.open(image_path)
            img = img.resize((400, 300), Image.LANCZOS)
            display = ImageTk.PhotoImage(img)
            self.img_label.config(image=display)
            self.img_label.image = display
        except Exception as e:
            self.log_message(f"Error loading image: {str(e)}")

    def display_analysis(self, text_path):
        try:
            with open(text_path, 'r') as f:
                analysis_text = f.read()
            self.res_txt.delete(1.0, tk.END)
            self.res_txt.insert(tk.END, analysis_text)
        except Exception as e:
            self.log_message(f"Error loading analysis text: {str(e)}")

def main():
    root = tk.Tk()
    app = NDVIMonitoringApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()