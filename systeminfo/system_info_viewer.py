import platform
import psutil
from datetime import datetime

def get_size(bytes, suffix="B"):
    # Scale bytes to KB, MB, GB, etc.
    factor = 1024
    for unit in ["", "K", "M", "G", "T"]:
        if bytes < factor:
            return f"{bytes:.2f} {unit}{suffix}"
        bytes /= factor

def save_report(info):
    filename = f"system_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, 'w') as f:
        f.write(info)
    print(f"\nReport saved as: {filename}")

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

# Run
if __name__ == "__main__":
    report = get_system_info()
    print(report)
    save_report(report)
