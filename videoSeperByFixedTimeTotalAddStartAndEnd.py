import subprocess
import os
import tkinter as tk
from tkinter import ttk, filedialog
from ttkthemes import ThemedStyle


def generate_videos(input_file, segment_interval, segment_duration, start_time, end_time):
    output_folder = "output_videos"
    os.makedirs(output_folder, exist_ok=True)

    ffprobe_cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", input_file
    ]
    total_duration = float(subprocess.check_output(ffprobe_cmd, universal_newlines=True))

    merged_segments = []

    for index, start_time in enumerate(range(start_time, int(total_duration), segment_interval), start=1):
        end_time = start_time + segment_duration
        output_segment = os.path.join(output_folder, f"segment_{index}.mp4")
        merged_segments.append(output_segment)

        cmd = [
            "ffmpeg", "-ss", str(start_time), "-i", input_file, "-t", str(segment_duration),
            "-vf", "scale=1920:1080", "-b:v", "2048k", "-c:v", "libx264",
            "-c:a", "aac", "-b:a", "192k", "-af", "volume=10dB",
            output_segment
        ]

        subprocess.run(cmd)

    # Construct the list of existing segment files for concatenation
    valid_segments = [segment for segment in merged_segments if os.path.exists(segment)]

    concat_list_path = os.path.join(output_folder, "concat_list.txt")
    with open(concat_list_path, "w") as f:
        for segment in valid_segments:
            f.write(f"file '{os.path.basename(segment)}'\n")

    merged_output_base = "merged_output"
    index = 1
    merged_output = os.path.join(output_folder, f"{merged_output_base}.mp4")
    while os.path.exists(merged_output):
        merged_output = os.path.join(output_folder, f"{merged_output_base}{index}.mp4")
        index += 1

    concat_cmd = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", concat_list_path, "-c", "copy", merged_output]
    subprocess.run(concat_cmd)

    for segment in merged_segments:
        os.remove(segment)
    os.remove(concat_list_path)

    return merged_output


def select_input_files():
    input_files = filedialog.askopenfilenames(filetypes=[("Video files", "*.mp4")])
    selected_files_listbox.delete(0, tk.END)
    for file in input_files:
        selected_files_listbox.insert(tk.END, file)


def generate_selected_videos():
    segment_interval = int(segment_interval_var.get())
    segment_duration = int(segment_duration_var.get())
    start_time = int(start_time_var.get())
    end_time = int(end_time_var.get())
    selected_files = selected_files_listbox.get(0, tk.END)
    total_videos = len(selected_files)

    for index, input_file in enumerate(selected_files, start=1):
        status_label.config(text=f"Generating video {index} of {total_videos}")
        root.update_idletasks()
        output_file = generate_videos(input_file, segment_interval, segment_duration, start_time, end_time)
        status_label.config(text=f"Generating video {index + 1} of {total_videos}")
        root.update_idletasks()

    status_label.config(text="All videos generated. Click OK to continue.")
    ok_button.pack(fill=tk.BOTH, padx=10, pady=(10, 0))
    selected_files_listbox.delete(0, tk.END)


def close_app():
    root.destroy()


root = tk.Tk()
root.title("Video Generation Tool")

style = ThemedStyle(root)
style.set_theme("equilux")
style.configure("TFrame", background="#e0e0e0")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 400
window_height = 700
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

select_multiple_button = ttk.Button(root, text="Select Multiple Input Files", command=select_input_files)
select_multiple_button.pack(fill=tk.BOTH, padx=10)

selected_files_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
selected_files_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

segment_interval_label = ttk.Label(root, text="Segment Interval (seconds):")
segment_interval_label.pack(fill=tk.BOTH, padx=10, pady=(10, 0))

segment_interval_var = tk.StringVar(value="300")
segment_interval_entry = ttk.Entry(root, textvariable=segment_interval_var)
segment_interval_entry.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

segment_duration_label = ttk.Label(root, text="Segment Duration (seconds):")
segment_duration_label.pack(fill=tk.BOTH, padx=10, pady=(10, 0))

segment_duration_var = tk.StringVar(value="30")
segment_duration_entry = ttk.Entry(root, textvariable=segment_duration_var)
segment_duration_entry.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

start_time_label = ttk.Label(root, text="trimming video duration from the start (seconds):")
start_time_label.pack(fill=tk.BOTH, padx=10, pady=(10, 0))

start_time_var = tk.StringVar(value="0")
start_time_entry = ttk.Entry(root, textvariable=start_time_var)
start_time_entry.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

end_time_label = ttk.Label(root, text="trimming video duration from the end (seconds):")
end_time_label.pack(fill=tk.BOTH, padx=10, pady=(10, 0))

end_time_var = tk.StringVar(value="0")
end_time_entry = ttk.Entry(root, textvariable=end_time_var)
end_time_entry.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

generate_selected_button = ttk.Button(root, text="Generate Selected Videos", command=generate_selected_videos)
generate_selected_button.pack(fill=tk.BOTH, padx=10, pady=(10, 0))

status_label = ttk.Label(root, text="", foreground="blue")
status_label.pack(fill=tk.BOTH, padx=10, pady=10)

ok_button = ttk.Button(root, text="OK", command=close_app)
root.protocol("WM_DELETE_WINDOW", close_app)

root.mainloop()
