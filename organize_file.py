import os
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

# === File type mapping ===
file_types = {
    '.txt': 'TextFiles',
    '.jpg': 'Images',
    '.jpeg': 'Images',
    '.png': 'Images',
    '.pdf': 'PDFs',
    '.docx': 'WordDocs',
    '.xlsx': 'ExcelSheets',
}

# === Organizer Function ===
def organize_files(source_folder, dry_run=True):
    log_file = os.path.join(source_folder, 'organizer_log.txt')

    def log(message):
        with open(log_file, 'a') as logf:
            logf.write(f"{datetime.now()} - {message}\n")

    with open(log_file, 'w') as f:
        f.write(f"--- Organizer Started at {datetime.now()} ---\n\n")

    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)

        if os.path.isfile(file_path):
            ext = os.path.splitext(filename)[1].lower()
            folder_name = file_types.get(ext, 'Others')
            target_folder = os.path.join(source_folder, folder_name)
            new_path = os.path.join(target_folder, filename)

            log_line = f"{'DRY RUN: ' if dry_run else ''}Moving '{filename}' to '{folder_name}'"
            print(log_line)
            log(log_line)

            if not dry_run:
                os.makedirs(target_folder, exist_ok=True)
                shutil.move(file_path, new_path)

    log("File organization complete.\n")
    if dry_run:
        log("Dry run mode: No files were moved.")

# === GUI Code ===
def browse_folder():
    folder = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder)

def run_organizer():
    folder = folder_entry.get()
    if not folder or not os.path.isdir(folder):
        messagebox.showerror("Error", "Please select a valid folder.")
        return
    dry_run = dry_run_var.get()
    organize_files(folder, dry_run)
    messagebox.showinfo("Done", "File organization completed.")

# === Tkinter UI ===
root = tk.Tk()
root.title("Python File Organizer")

tk.Label(root, text="Select Folder to Organize:").grid(row=0, column=0, padx=10, pady=10)
folder_entry = tk.Entry(root, width=50)
folder_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=browse_folder).grid(row=0, column=2, padx=10)

dry_run_var = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Dry Run (Preview Only)", variable=dry_run_var).grid(row=1, column=1, sticky="w", padx=10)

tk.Button(root, text="Execute", command=run_organizer, width=20, bg="green", fg="white").grid(row=2, column=1, pady=15)

root.mainloop()