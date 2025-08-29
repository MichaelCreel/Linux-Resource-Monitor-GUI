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
label_style = {"bg": "#06061b", "fg": "#ffffff", "font": ("Helvetica", 12)}

root.title("Resource Monitor")

style = ttk.Style()
style.theme_use('clam')

style.configure("cpu.Horizontal.TProgressbar", troughcolor="#ffffff", background="#FF6200")
style.configure("gpu.Horizontal.TProgressbar", troughcolor="#ffffff", background="#77FF00")

cpu_bar = ttk.Progressbar(root, length=400, maximum=100, style="cpu.Horizontal.TProgressbar")
cpu_bar.pack(pady=5, fill="x", expand=True)
cpu_label = tk.Label(root, **label_style)
cpu_label.pack(pady=5, fill="x", expand=True)

chart_frame = tk.Frame(root, bg="#06061b")
chart_frame.pack(pady=5, fill="x", expand=True)
memory_label = tk.Label(root, **label_style)
memory_label.pack(pady=5, fill="x", expand=True)

gpu_bar = ttk.Progressbar(root, length=400, maximum=100, style="gpu.Horizontal.TProgressbar")
gpu_bar.pack(pady=5, fill="x", expand=True)
gpu_label = tk.Label(root, **label_style)
gpu_label.pack(pady=5, fill="x", expand=True)

fig = Figure(figsize=(3.5, 3.5), dpi=100)
fig.patch.set_facecolor('#06061b')
ax = fig.add_subplot(111)
ax.set_facecolor('#06061b')
canvas = FigureCanvasTkAgg(fig, master=chart_frame)
canvas.get_tk_widget().pack(fill="both", expand=True)

update_stats()
root.mainloop()

def resize_fonts(event):
    new_size = max(12, int(event.width / 40))
    label_style["font"] = ("Helvetica", new_size)
    cpu_label.config(font=label_style["font"])
    memory_label.config(font=label_style["font"])
    gpu_label.config(font=label_style["font"])

root.bind("<Configure>", resize_fonts)
