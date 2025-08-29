import tkinter as tk
from tkinter import ttk
import subprocess

def update_stats():
    try:
        output = subprocess.check_output(["./resource-monitor"]).decode()
        lines = output.strip().split("\n")

        cpu = next((line for line in lines if "CPU Usage" in line), "CPU Usage: N/A")
        used = next((line for line in lines if "Used Memory" in line), "Used Memory: N/A")
        free = next((line for line in lines if "Free Memory" in line), "Free Memory: N/A")
        total = next((line for line in lines if "Total Memory" in line), "Total Memory: N/A")
        memory_label.config(text=f"{used}\n{free}\n{total}")
        gpu = next((line for line in lines if "GPU Usage" in line), "GPU Usage: N/A")

        cpu_label.config(text=cpu)
        gpu_label.config(text=gpu)

    except Exception as e:
        cpu_label.config(text="Failure Reading CPU")
        memory_label.config(text=str(e))
        gpu_label.config(text="Failure Reading GPU")

    root.after(1000, update_stats)

root = tk.Tk()
root.title("Resource Monitor")

cpu_label = tk.Label(root, font=("Helvetica", 14))
cpu_label.pack(pady=5)

memory_label = tk.Label(root, font=("Helvetica", 14))
memory_label.pack(pady=5)

gpu_label = tk.Label(root, font=("Helvetica", 14))
gpu_label.pack(pady=5)

update_stats()
root.mainloop()