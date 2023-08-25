import subprocess
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from ttkthemes import ThemedStyle


def generate_videos():
    input_file = input_file_entry.get()
    output_folder = "output_videos"
    os.makedirs(output_folder, exist_ok=True)

    # Get total video duration using ffprobe
    ffprobe_cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", input_file
    ]
    total_duration = float(subprocess.check_output(ffprobe_cmd, universal_newlines=True))

    # Get user-defined values for segment_interval and segment_duration
    segment_interval = int(segment_interval_var.get())
    segment_duration = int(segment_duration_var.get())

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

    # Construct the list of existing segment files for concatenation
    valid_segments = [segment for segment in merged_segments if os.path.exists(segment)]

    # Concatenate all extracted segments
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

    # Clean up temporary segment files and concat list file
    for segment in merged_segments:
        os.remove(segment)
    os.remove(concat_list_path)

    messagebox.showinfo("Completed", "Video extraction and merging completed.")


def select_input_file():
    global input_file
    input_file = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4")])
    input_file_entry.delete(0, tk.END)
    input_file_entry.insert(0, input_file)


root = tk.Tk()
root.title("Video Generation Tool")

style = ThemedStyle(root)
style.set_theme("equilux")
style.configure("TFrame", background="#e0e0e0")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - 300) // 2
y = (screen_height - 350) // 2
root.geometry(f"300x350+{x}+{y}")

input_file_label = ttk.Label(root, text="Input File:")
input_file_label.pack(fill=tk.BOTH, padx=10, pady=(10, 0))

input_file_entry = ttk.Entry(root)
input_file_entry.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

select_button = ttk.Button(root, text="Select", command=select_input_file)
select_button.pack(fill=tk.BOTH, padx=10)

segment_interval_label = ttk.Label(root, text="Segment Interval (seconds):")
segment_interval_label.pack(fill=tk.BOTH, padx=10, pady=(10, 0))

segment_interval_var = tk.StringVar(value="300")  # Default value
segment_interval_entry = ttk.Entry(root, textvariable=segment_interval_var)
segment_interval_entry.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

segment_duration_label = ttk.Label(root, text="Segment Duration (seconds):")
segment_duration_label.pack(fill=tk.BOTH, padx=10, pady=(10, 0))

segment_duration_var = tk.StringVar(value="30")  # Default value
segment_duration_entry = ttk.Entry(root, textvariable=segment_duration_var)
segment_duration_entry.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

generate_button = ttk.Button(root, text="Generate Videos", command=generate_videos)
generate_button.pack(fill=tk.BOTH, padx=10, pady=(10, 0))

root.mainloop()
