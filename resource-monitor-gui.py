import tkinter as tk
from tkinter import ttk
import subprocess
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

fig = None
ax = None
canvas = None

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

        if "CPU Usage" in cpu and "%" in cpu:
            cpu_percent = float(cpu.split(":")[1].strip().replace("%", ""))
            cpu_bar['value'] = cpu_percent
        else:
            cpu_bar['value'] = 0

        if "GPU Usage" in gpu and "%" in gpu:
            gpu_percent = float(gpu.split(":")[1].strip().replace(" %", ""))
            gpu_bar['value'] = gpu_percent
        else:
            gpu_bar['value'] = 0


        used_gb = float(used.split("(")[1].replace("GB)", "").strip())
        free_gb = float(free.split(":")[1].split("GB")[0].strip())
        ax.clear()
        ax.pie([used_gb, free_gb], labels=["Used", "Free"], autopct='%1.1f%%', colors=["#ff6666", "#66b3ff"])
        ax.set_title("Memory Usage", color="white")
        for text in ax.texts:
            text.set_color("white")
        canvas.draw()
        canvas.get_tk_widget().pack()

    except Exception as e:
        cpu_label.config(text="Failure Reading CPU")
        memory_label.config(text=str(e))
        gpu_label.config(text="Failure Reading GPU")

    root.after(1000, update_stats)

root = tk.Tk()
root.configure(bg="#06061b")
label_style = {"bg": "#06061b", "fg": "#ffffff", "font": ("Helvetica", 18)}

root.title("Resource Monitor")

cpu_bar = ttk.Progressbar(root, length=400, height=200, maximum=100)
cpu_bar.pack(pady=10)
cpu_label = tk.Label(root, **label_style)
cpu_label.pack(pady=10)

chart_frame = tk.Frame(root, bg="#06061b")
chart_frame.pack(pady=10)
memory_label = tk.Label(root, **label_style)
memory_label.pack(pady=10)

gpu_bar = ttk.Progressbar(root, length=400, height=200, maximum=100)
gpu_bar.pack(pady=10)
gpu_label = tk.Label(root, **label_style)
gpu_label.pack(pady=10)

fig = Figure(figsize=(5, 5), dpi=100)
fig.patch.set_facecolor('#06061b')
ax = fig.add_subplot(111)
ax.set_facecolor('#06061b')
canvas = FigureCanvasTkAgg(fig, master=chart_frame)
canvas.get_tk_widget().pack()

update_stats()
root.mainloop()