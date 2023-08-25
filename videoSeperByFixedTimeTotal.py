import subprocess
import os
import tkinter as tk
from tkinter import ttk, filedialog
from ttkthemes import ThemedStyle


def generate_videos(input_file, segment_interval, segment_duration):
    output_folder = "output_videos"
    os.makedirs(output_folder, exist_ok=True)

    ffprobe_cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", input_file
    ]
    total_duration = float(subprocess.check_output(ffprobe_cmd, universal_newlines=True))

    merged_segments = []

    for start_time in range(0, int(total_duration), segment_interval):
        end_time = start_time + segment_duration
        output_segment = os.path.join(output_folder, f"segment_{start_time}-{end_time}.mp4")
        merged_segments.append(output_segment)

        cmd = [
            "ffmpeg", "-i", input_file, "-ss", str(start_time), "-to", str(end_time),
            "-vf", "scale=1920:1080", "-b:v", "2048k", "-c:v", "libx264",
            "-c:a", "aac", "-b:a", "192k", "-af", "volume=10dB",
            output_segment
        ]

        subprocess.run(cmd)

        progress_var.set((end_time / total_duration) * 100)
        root.update_idletasks()  # Update the GUI to show the progress

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
    if input_files:
        for input_file in input_files:
            selected_files_listbox.insert(tk.END, input_file)


def generate_selected_videos():
    segment_interval = int(segment_interval_var.get())
    segment_duration = int(segment_duration_var.get())
    selected_files = selected_files_listbox.get(0, tk.END)

    progress_var.set(0)
    total_videos = len(selected_files)

    status_label.config(text=f"Generating video 1 of {total_videos}")
    root.update_idletasks()

    for index, input_file in enumerate(selected_files, start=1):
        output_file = generate_videos(input_file, segment_interval, segment_duration)

        if index < total_videos:
            status_label.config(text=f"Generating video {index + 1} of {total_videos}")
            root.update_idletasks()

    status_label.config(text="All videos generated. Click OK to continue.")
    ok_button.pack(fill=tk.BOTH, padx=10, pady=(10, 0))

    # 清除之前选择的文件列表
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
x = (screen_width - 300) // 2
y = (screen_height - 600) // 2
root.geometry(f"300x600+{x}+{y}")

select_multiple_button = ttk.Button(root, text="Select Multiple Input Files", command=select_input_files)
select_multiple_button.pack(fill=tk.BOTH, padx=10)

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

generate_selected_button = ttk.Button(root, text="Generate Selected Videos", command=generate_selected_videos)
generate_selected_button.pack(fill=tk.BOTH, padx=10, pady=(10, 0))

selected_files_label = ttk.Label(root, text="Selected Files:")
selected_files_label.pack(fill=tk.BOTH, padx=10, pady=(10, 0))

selected_files_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
selected_files_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(fill=tk.BOTH, padx=10, pady=(0, 10))

status_label = ttk.Label(root, text="")
status_label.pack(fill=tk.BOTH, padx=10, pady=(0, 10))

ok_button = ttk.Button(root, text="OK", command=close_app)

root.mainloop()
