import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import threading

class VideoDownloaderApp:
    def __init__(self, master):
        self.master = master
        master.title("🎥 Video Downloader (m3u8)")
        master.geometry("520x380")
        master.resizable(False, False)

        # URL entry
        tk.Label(master, text="Enter the .m3u8 URL:").pack(pady=(15, 5))
        self.entry_url = tk.Entry(master, width=70)
        self.entry_url.pack()

        # Folder for storage
        tk.Label(master, text="Choose a folder where the video will be stored:").pack(pady=(10, 5))
        self.button_folder = tk.Button(master, text="📂 Choose folder", command=self.browse_folder)
        self.button_folder.pack()
        self.label_folder = tk.Label(master, text="", fg="gray")
        self.label_folder.pack()
        self.folder_path = ""

        # File name
        tk.Label(master, text="Enter the file name (without .mp4):").pack(pady=(10, 5))
        self.entry_filename = tk.Entry(master, width=40)
        self.entry_filename.pack()

        # Download label
        self.label_loading = tk.Label(master, text="", font=("Arial", 10), fg="blue")
        self.label_loading.pack(pady=(15, 2))

        # Progress bar
        self.progress = ttk.Progressbar(master, mode="indeterminate", length=300)
        self.progress.pack()

        # Button for download
        self.button_download = tk.Button(
            master,
            text="⬇️ Download video",
            command=self.start_download_thread,
            bg="green",
            fg="white",
            font=("Arial", 12, "bold")
        )
        self.button_download.pack(pady=20)

    def browse_folder(self):
        self.folder_path = filedialog.askdirectory()
        self.label_folder.config(text=self.folder_path)

    def start_download_thread(self):
        thread = threading.Thread(target=self.download_video)
        thread.start()

    def download_video(self):
        url = self.entry_url.get().strip()
        filename = self.entry_filename.get().strip() or "video"
        folder = self.folder_path

        if not url or not url.startswith("http") or ".m3u8" not in url:
            messagebox.showerror("Error", "Enter a valid .m3u8 URL.")
            return
        if not folder:
            messagebox.showerror("Error", "You didn't choose a folder.")
            return

        output_path = os.path.join(folder, f"{filename}.mp4")

        # Show bar and label
        self.label_loading.config(text="Dowloading...")
        self.progress.start()

        try:
            # Hide terminal (Only on Windows)
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            result = subprocess.run(
                ["streamlink", url, "best", "-o", output_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                startupinfo=si
            )
            self.progress.stop()
            self.label_loading.config(text="")

            if result.returncode == 0:
                messagebox.showinfo("Success", f"✅ The video has been downloaded!:\n{output_path}")
            else:
                messagebox.showerror("Error", f"❌ Download failed:\n{result.stderr}")

        except FileNotFoundError:
            self.progress.stop()
            self.label_loading.config(text="")
            messagebox.showerror("Error", "Missing 'streamlink'")

# Start GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloaderApp(root)
    root.mainloop()