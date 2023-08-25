import subprocess
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from ttkthemes import ThemedStyle

# Default video information
default_video_info = [
    ("video1", "00:00:30", "00:01:00"),
    ("video2", "00:01:30", "00:02:00"),
    ("video3", "00:03:30", "00:05:00")
    # Add more video info tuples as needed
]

def generate_videos():
    input_file = input_file_entry.get()
    video_info_text = video_info_textarea.get("1.0", "end-1c")
    output_folder = "output_videos"

    os.makedirs(output_folder, exist_ok=True)

    video_info_lines = video_info_text.split("\n")
    video_info = [tuple(line.split()) for line in video_info_lines if len(line.split()) >= 3]

    for video_name, start_time, end_time in video_info:
        output_file = os.path.join(output_folder, f"{video_name}.mp4")

        # Remove existing file if it exists
        if os.path.exists(output_file):
            os.remove(output_file)

        cmd = [
            "ffmpeg", "-i", input_file, "-ss", start_time, "-to", end_time,
            "-vf", "scale=1920:1080", "-b:v", "2048k", "-c:v", "libx264",
            "-c:a", "aac", "-b:a", "192k", "-af", "volume=10dB",
            output_file
        ]

        subprocess.run(cmd)

    messagebox.showinfo("Completed", "Video splitting, audio volume adjustment, and quality settings completed.")

def select_input_file():
    global input_file
    input_file = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4")])
    input_file_entry.delete(0, tk.END)
    input_file_entry.insert(0, input_file)

root = tk.Tk()
root.title("Video Generation Tool")

# Apply ttkthemes style
style = ThemedStyle(root)
style.set_theme("equilux")  # Set your preferred theme

# Customize background color
style.configure("TFrame", background="#e0e0e0")  # Change to your preferred color

# Calculate screen center
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - 600) // 2  # Adjust window width as needed
y = (screen_height - 400) // 2  # Adjust window height as needed
root.geometry(f"600x400+{x}+{y}")

input_file_label = ttk.Label(root, text="Input File:")
input_file_label.pack(fill=tk.BOTH, padx=10, pady=(10, 0))

input_file_entry = ttk.Entry(root)
input_file_entry.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

select_button = ttk.Button(root, text="Select", command=select_input_file)
select_button.pack(fill=tk.BOTH, padx=10)

video_info_label = ttk.Label(root, text="Video Info:")
video_info_label.pack(fill=tk.BOTH, padx=10, pady=(10, 0))

video_info_textarea = tk.Text(root, height=10, width=40)
video_info_textarea.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Set default video_info values
default_video_info_text = "\n".join([" ".join(info) for info in default_video_info])
video_info_textarea.insert("1.0", default_video_info_text)

generate_button = ttk.Button(root, text="Generate Videos", command=generate_videos)
generate_button.pack(fill=tk.BOTH, padx=10, pady=(0, 10))

root.mainloop()
