import os
import shutil
import customtkinter as ctk
from tkinter import filedialog, messagebox

class UltraFileOrganizer(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Ultra File Organizer - Mafaz Tech")
        self.geometry("800x750")
        ctk.set_appearance_mode("dark")

        # Main Title
        self.label = ctk.CTkLabel(self, text="Advanced File Organization System", font=("Segoe UI", 24, "bold"))
        self.label.pack(pady=15)

        # Path Frame
        self.path_frame = ctk.CTkFrame(self)
        self.path_frame.pack(pady=10, padx=20, fill="x")
        self.btn_browse = ctk.CTkButton(self.path_frame, text="Select Folder", command=self.select_folder, width=100)
        self.btn_browse.pack(side="left", padx=10, pady=10)
        self.path_entry = ctk.CTkEntry(self.path_frame, placeholder_text="Folder path...", width=550)
        self.path_entry.pack(side="left", padx=10, pady=10)

        # Scrollable Frame for Checkboxes
        self.scroll_frame = ctk.CTkScrollableFrame(self, label_text="Select Extensions to Organize")
        self.scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Full Extension List
        self.ext_groups = {
            "Documents": ["PDF", "DOCX", "DOC", "XLSX", "XLS", "PPTX", "PPT", "TXT", "RTF", "EPUB", "MOBI"],
            "Images": ["JPG", "JPEG", "PNG", "GIF", "SVG", "TIFF", "WebP", "HEIC", "PSD", "AI"],
            "Videos": ["MP4", "MOV", "AVI", "MKV", "WMV", "FLV"],
            "Audio": ["MP3", "WAV", "M4A", "FLAC", "AAC", "OGG"],
            "System & Apps": ["EXE", "APK", "DMG", "ISO"],
            "Archives": ["ZIP", "RAR", "7Z"],
            "Programming": ["HTML", "CSS", "JS", "JSON", "XML", "PHP", "PY"]
        }

        self.checkbox_vars = {}
        
        for group_name, extensions in self.ext_groups.items():
            group_lbl = ctk.CTkLabel(self.scroll_frame, text=f"--- {group_name} ---", font=("Arial", 14, "bold"), text_color="#1f538d")
            group_lbl.pack(pady=(10, 5), anchor="w")
            
            inner_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
            inner_frame.pack(fill="x", padx=10)
            
            cols = 4
            for i, ext in enumerate(extensions):
                cb = ctk.CTkCheckBox(inner_frame, text=ext)
                cb.grid(row=i//cols, column=i%cols, padx=10, pady=5, sticky="w")
                self.checkbox_vars[ext.lower()] = cb

        # Control Buttons
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=20)

        self.start_btn = ctk.CTkButton(self.button_frame, text="Organize Selected", 
                                      fg_color="#1f538d", hover_color="#14375e",
                                      width=200, height=45, font=("Arial", 14, "bold"),
                                      command=lambda: self.run_organizer(all_files=False))
        self.start_btn.pack(side="left", padx=10)

        self.all_btn = ctk.CTkButton(self.button_frame, text="Organize Everything (All)", 
                                    fg_color="#28a745", hover_color="#218838",
                                    width=200, height=45, font=("Arial", 14, "bold"),
                                    command=lambda: self.run_organizer(all_files=True))
        self.all_btn.pack(side="left", padx=10)

        self.footer = ctk.CTkLabel(self, text="Developed by Mafaz - 2026", font=("Arial", 10))
        self.footer.pack(side="bottom", pady=5)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_entry.delete(0, 'end')
            self.path_entry.insert(0, folder)

    def run_organizer(self, all_files=False):
        target_path = self.path_entry.get()
        if not target_path or not os.path.exists(target_path):
            messagebox.showerror("Error", "Please select a valid folder!")
            return

        selected_exts = [ext for ext, cb in self.checkbox_vars.items() if cb.get()]
        
        if not all_files and not selected_exts:
            messagebox.showwarning("Warning", "Select at least one extension!")
            return

        moved_count = 0
        try:
            for filename in os.listdir(target_path):
                file_path = os.path.join(target_path, filename)
                if os.path.isfile(file_path):
                    # حماية الملف البرمجي والتطبيق من النقل
                    if filename.lower() in ["file organizer.py", "file organizer.exe"]:
                        continue
                    
                    ext = os.path.splitext(filename)[1].replace(".", "").lower()
                    if not ext: ext = "no_extension"

                    if all_files or (ext in selected_exts):
                        dest_folder = os.path.join(target_path, ext.upper() + "_Files")
                        if not os.path.exists(dest_folder): os.mkdir(dest_folder)
                        shutil.move(file_path, os.path.join(dest_folder, filename))
                        moved_count += 1
            
            messagebox.showinfo("Success", f"Done! Moved {moved_count} files.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    app = UltraFileOrganizer()
    app.mainloop()