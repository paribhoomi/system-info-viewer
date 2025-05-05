import platform
import psutil
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T"]:
        if bytes < factor:
            return f"{bytes:.2f} {unit}{suffix}"
        bytes /= factor

def get_system_info():
    info = []
    info.append(f"System: {platform.system()} {platform.release()}")
    info.append(f"Processor: {platform.processor()}")
    info.append(f"CPU Cores: {psutil.cpu_count(logical=False)} physical, {psutil.cpu_count()} logical")
    info.append(f"CPU Usage: {psutil.cpu_percent()}%")
    info.append(f"RAM: {get_size(psutil.virtual_memory().total)} total")
    info.append(f"Used RAM: {get_size(psutil.virtual_memory().used)}")
    info.append(f"Disk: {get_size(psutil.disk_usage('/').total)} total, {psutil.disk_usage('/').percent}% used")
    info.append("\nTop 5 Processes by Memory:\n")
    
    for proc in sorted(psutil.process_iter(['pid', 'name', 'memory_info']), key=lambda p: p.info['memory_info'].rss, reverse=True)[:5]:
        mem = get_size(proc.info['memory_info'].rss)
        info.append(f"PID {proc.info['pid']}: {proc.info['name']} – {mem}")
    
    return "\n".join(info)

def show_info():
    output = get_system_info()
    text_area.delete('1.0', tk.END)
    text_area.insert(tk.INSERT, output)

def save_info():
    report = text_area.get('1.0', tk.END)
    filename = f"system_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, 'w') as f:
        f.write(report)
    status_label.config(text=f"Saved as {filename}")

# GUI setup
root = tk.Tk()
root.title("System Info Viewer")
root.geometry("600x500")

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=25)
text_area.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack()

tk.Button(button_frame, text="Show Info", command=show_info).pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Save Report", command=save_info).pack(side=tk.LEFT, padx=10)

status_label = tk.Label(root, text="", fg="green")
status_label.pack()

root.mainloop()
