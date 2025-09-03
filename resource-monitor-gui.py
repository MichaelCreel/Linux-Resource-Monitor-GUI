import tkinter as tk
from tkinter import ttk
import subprocess
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.font as tkFont

fig = None
ax = None
canvas = None
chart_font_size = 12

def update_stats():
    try:
        output = subprocess.check_output(["./resource-monitor"]).decode()
        lines = output.strip().split("\n")

        cpu = next((line for line in lines if "CPU Usage" in line), "CPU Usage: N/A")
        used = next((line for line in lines if "Used Memory" in line), "Used Memory: N/A")
        free = next((line for line in lines if "Free Memory" in line), "Free Memory: N/A")
        total = next((line for line in lines if "Total Memory" in line), "Total Memory: N/A")
        memory_label.config(text=f"{used}\n{free}\n{total}", font=shared_font)
        gpu = next((line for line in lines if "GPU Usage" in line), "GPU Usage: N/A")

        cpu_label.config(text=cpu, font=shared_font)
        gpu_label.config(text=gpu, font=shared_font)

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
        ax.set_title("", color="white", fontsize=chart_font_size)
        for text in ax.texts:
            text.set_color("white")
            text.set_fontsize(chart_font_size)
        canvas.draw()

    except Exception as e:
        cpu_label.config(text="Failure Reading CPU", font=shared_font)
        memory_label.config(text=str(e), font=shared_font)
        gpu_label.config(text="Failure Reading GPU", font=shared_font)

    root.after(1000, update_stats)

root = tk.Tk()
root.configure(bg="#06061b")
label_style = {"bg": "#06061b", "fg": "#ffffff"}

shared_font = tkFont.Font(family="Helvetica", size=12)

root.title("Resource Monitor")

style = ttk.Style()
style.theme_use('clam')

style.configure("cpu.Horizontal.TProgressbar", troughcolor="#ffffff", background="#FF6200")
style.configure("gpu.Horizontal.TProgressbar", troughcolor="#ffffff", background="#77FF00")

cpu_bar = ttk.Progressbar(root, length=400, maximum=100, style="cpu.Horizontal.TProgressbar")
cpu_bar.pack(pady=5, fill="both", expand=True)
cpu_label = tk.Label(root, font=shared_font, **label_style)
cpu_label.pack(pady=5, fill="both", expand=True)

chart_frame = tk.Frame(root, bg="#06061b")
chart_frame.pack(pady=5, fill="both", expand=True)
memory_label = tk.Label(root, font=shared_font, **label_style)
memory_label.pack(pady=5, fill="both", expand=True)

gpu_bar = ttk.Progressbar(root, length=400, maximum=100, style="gpu.Horizontal.TProgressbar")
gpu_bar.pack(pady=5, fill="both", expand=True)
gpu_label = tk.Label(root, font=shared_font, **label_style)
gpu_label.pack(pady=5, fill="both", expand=True)

fig = Figure(figsize=(4.5, 4.5), dpi=100)
fig.patch.set_facecolor('#06061b')
ax = fig.add_subplot(111)
ax.set_facecolor('#06061b')
canvas = FigureCanvasTkAgg(fig, master=chart_frame)
canvas.get_tk_widget().pack(fill="both", expand=True)

labels = [cpu_label, memory_label, gpu_label]

def resize_chart(event):
    global resize_timer
    if resize_timer:
        root.after_cancel(resize_timer)
    resize_timer = root.after(100, lambda: _resize_chart(event))

def _resize_chart(event):
    global chart_font_size
    width_in = event.width / fig.get_dpi()
    height_in = event.height / fig.get_dpi()
    chart_font_size = max(8, int(min(event.width, event.height) / 50))
    fig.set_size_inches(width_in, height_in)
    canvas.draw_idle()


def resize_fonts(event):
    new_size = max(12, int(min(event.width, event.height) / 50))
    shared_font.configure(size=new_size)

root.bind("<Configure>", resize_fonts)
chart_frame.bind("<Configure>", resize_chart)

resize_timer = None

update_stats()
root.mainloop()
