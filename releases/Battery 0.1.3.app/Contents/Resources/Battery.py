import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import subprocess
import threading
import time

class InstallFrame:
    def __init__(self, root):
        self.root = root
        self.root.title("Battery Installation")

        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        root.config(menu=menubar)

        ttk.Style().configure("active.TButton", foreground="white")

        self.label = tk.Label(root, text="Battery management CLI tool is not installed! Click below to copy the installation command:")
        self.label.pack(pady=10,padx=20)

        self.copy_button = ttk.Button(root, text="Copy Installation Command", command=self.copy_install_command,default="active",style="active.TButton")
        self.copy_button.pack()

        self.end = tk.Label(root, text="After running the above command in Terminal, relaunch the app\n\nThe CLI tool is NOT made by me, please see the github repo at actuallymentor/battery")
        self.end.pack(pady=10)

    def copy_install_command(self):
        install_command = "curl -s https://raw.githubusercontent.com/actuallymentor/battery/main/setup.sh | bash"
        self.root.clipboard_clear()
        self.root.clipboard_append(install_command)

class BatteryControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Battery Control")

        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        root.config(menu=menubar)
        

        self.status_label = tk.Label(root, text="Battery Status: Unknown")
        self.status_label.pack(pady=10,padx=10)

        self.charge_label = tk.Label(root, text="Battery Charging: Unknown")
        self.charge_label.pack(padx=10)

        tk.Label(root,text="Output Log").pack()

        self.log_text = tk.Text(root, height=5, width=40,state="disabled")
        self.log_text.pack(pady=10)

        self.clear_log_button = tk.Button(root, text="Clear Log", command=self.clear_log)
        self.clear_log_button.pack()

        self.input_label = tk.Label(root, text="Enter target percentage:")
        self.input_label.pack()

        self.input_field = tk.Entry(root)
        self.input_field.pack()

        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack(pady=10)

        self.charge_button = tk.Button(self.buttons_frame, text="Charge", command=self.charge_battery)
        self.discharge_button = tk.Button(self.buttons_frame, text="Discharge", command=self.discharge_battery)
        self.maintain_button = tk.Button(self.buttons_frame, text="Maintain", command=self.maintain_battery)
        self.stop_button = tk.Button(self.buttons_frame, text="Stop All", command=self.stop_all_processes,state="disabled")

        self.enable_charging_button = tk.Button(self.buttons_frame, text="Enable Charging", command=self.enable_charging)
        self.disable_charging_button = tk.Button(self.buttons_frame, text="Disable Charging", command=self.disable_charging)

        self.charge_button.grid(row=0, column=0)
        self.discharge_button.grid(row=0, column=1)
        self.maintain_button.grid(row=0, column=2)
        self.stop_button.grid(row=0, column=3)

        self.enable_charging_button.grid(row=1, column=0)
        self.disable_charging_button.grid(row=1, column=1)

        self.update_status()

    def isValid(self, P):
        return str.isdigit(P) and 0 < int(P) and int(P) <= 100

    def update_status(self, repeat=True):
        battery_status = self.run_command(["/usr/local/bin/battery", "status"])  # Use a list of arguments
        battery_status = battery_status.split("-")[2].strip().split(", ")
        self.status_label.config(text=f"Battery Status: {battery_status[0]}")
        self.charge_label.config(text=f"Battery Charging: {battery_status[1]}")
        if repeat:self.root.after(5000, self.update_status)

    def run_command(self, command):
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()

    def disable_buttons(self):
        self.charge_button.config(state="disabled")
        self.discharge_button.config(state="disabled")
        self.maintain_button.config(state="disabled")
        self.enable_charging_button.config(state="disabled")
        self.disable_charging_button.config(state="disabled")
        self.stop_button.config(state="normal")

    def enable_buttons(self):
        self.charge_button.config(state="normal")
        self.discharge_button.config(state="normal")
        self.maintain_button.config(state="normal")
        self.enable_charging_button.config(state="normal")
        self.disable_charging_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def charge_battery(self):
        input_value = self.input_field.get()
        if not self.isValid(input_value):
            tkinter.messagebox.showwarning("","Enter a value from 1 to 100")
            return
        self.disable_buttons()
        self.run_continuous_command("/usr/local/bin/battery charge", input_value)

    def discharge_battery(self):
        input_value = self.input_field.get()
        if not self.isValid(input_value):
            tkinter.messagebox.showwarning("","Enter a value from 1 to 100")
            return
        self.disable_buttons()
        self.run_continuous_command("/usr/local/bin/battery discharge", input_value)

    def maintain_battery(self):
        input_value = self.input_field.get()
        if not self.isValid(input_value):
            tkinter.messagebox.showwarning("","Enter a value from 1 to 100")
            return
        self.disable_buttons()
        self.run_continuous_command("/usr/local/bin/battery maintain", input_value)

    def enable_charging(self):
        self.run_command(["/usr/local/bin/battery", "charging", "on"])
        self.update_status(False)

    def disable_charging(self):
        self.run_command(["/usr/local/bin/battery", "charging", "off"])
        self.update_status(False)

    def stop_all_processes(self):
        if hasattr(self, 'process') and self.process:
            self.process.terminate()  # Terminate the subprocess
            self.enable_buttons()  # Enable buttons

    def run_continuous_command(self, command, input_value):
        self.clear_log()
        self.process = subprocess.Popen(
            command.split() + [input_value],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        # Start a thread to continuously check the process status
        self.poll_thread = threading.Thread(target=self.check_process_status)
        self.poll_thread.start()

        # Start a thread to update the log_text
        self.log_thread = threading.Thread(target=self.update_log_text)
        self.log_thread.start()

    def clear_log(self):
        self.log_text.config(state="normal")  # Set state to normal to enable clearing
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state="disabled")

    def update_log_text(self):
        while True:
            line = self.process.stdout.readline()
            if not line:
                break
            self.log_text.config(state="normal")  # Set state to normal to update log
            self.log_text.insert(tk.END, line)
            self.log_text.see(tk.END)
            self.log_text.config(state="disabled")  # Set state back to disabled
            time.sleep(0.1)

    def check_process_status(self):
        while True:
            return_code = self.process.poll()
            if return_code is not None:
                self.enable_buttons()
                tkinter.messagebox.showinfo("","Operation Finished")
                break
            time.sleep(1)  # Check the process status every 1 second

def check_battery_installed():
    try:
        subprocess.check_output(["/usr/local/bin/battery"], stderr=subprocess.STDOUT, text=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

if __name__ == "__main__":
    root = tk.Tk(className="Battery Control")
    if not check_battery_installed():
        install_frame = InstallFrame(root)
    else:
        app = BatteryControlApp(root)
    root.mainloop()
