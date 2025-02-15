import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import zipfile
from pathlib import Path
import os

class ZipExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Code File Extractor")
        self.root.geometry("600x400")
        
        # Set app icon
        try:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app_icon.png')
            if os.path.exists(icon_path):
                self.root.iconphoto(True, tk.PhotoImage(file=icon_path))
        except Exception:
            pass  # Skip icon if not found
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Variables
        self.zip_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.status = tk.StringVar(value="Ready")
        self.extensions = tk.StringVar(value=".c,.cpp")
        
        # Zip File Selection
        ttk.Label(main_frame, text="Zip File:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.zip_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_zip).grid(row=0, column=2)
        
        # Output File Selection
        ttk.Label(main_frame, text="Output File:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_path, width=50).grid(row=1, column=1, padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_output).grid(row=1, column=2)
        
        # Extensions
        ttk.Label(main_frame, text="Extensions:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.extensions, width=50).grid(row=2, column=1, padx=5)
        ttk.Label(main_frame, text="(comma-separated)").grid(row=2, column=2)
        
        # Extract Button
        ttk.Button(main_frame, text="Extract Files", command=self.extract_files).grid(row=3, column=0, columnspan=3, pady=20)
        
        # Status Bar
        status_frame = ttk.Frame(main_frame, relief=tk.SUNKEN)
        status_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E))
        ttk.Label(status_frame, textvariable=self.status).grid(row=0, column=0, sticky=tk.W)
        
        # Progress Bar
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

    def browse_zip(self):
        filename = filedialog.askopenfilename(
            title="Select Zip File",
            filetypes=[("Zip files", "*.zip"), ("All files", "*.*")]
        )
        if filename:
            self.zip_path.set(filename)
            # Auto-set output path
            output_path = os.path.splitext(filename)[0] + "_extracted.txt"
            self.output_path.set(output_path)

    def browse_output(self):
        filename = filedialog.asksaveasfilename(
            title="Save Output File",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.output_path.set(filename)

    def extract_files(self):
        zip_path = self.zip_path.get()
        output_path = self.output_path.get()
        extensions = [ext.strip() for ext in self.extensions.get().split(",")]
        
        # Validate inputs
        if not zip_path or not output_path:
            messagebox.showerror("Error", "Please select both zip and output files")
            return
        
        # Ensure extensions start with dot
        extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]
        
        try:
            self.status.set("Extracting files...")
            self.progress['value'] = 0
            self.root.update_idletasks()
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Get list of all files in zip
                files = zip_ref.namelist()
                matching_files = [f for f in files if Path(f).suffix.lower() in extensions]
                total_files = len(matching_files)
                
                if total_files == 0:
                    messagebox.showinfo("Info", "No matching files found in the zip archive")
                    self.status.set("Ready")
                    return
                
                with open(output_path, 'w', encoding='utf-8') as outfile:
                    for i, file in enumerate(matching_files, 1):
                        try:
                            # Extract and read the file content
                            with zip_ref.open(file) as code_file:
                                content = code_file.read().decode('utf-8')
                                
                                # Write file header
                                outfile.write(f'\n{"="*50}\n')
                                outfile.write(f'File: {file}\n')
                                outfile.write(f'{"="*50}\n\n')
                                
                                # Write file content
                                outfile.write(content)
                                outfile.write('\n')
                            
                            # Update progress
                            progress = (i / total_files) * 100
                            self.progress['value'] = progress
                            self.status.set(f"Processing file {i} of {total_files}")
                            self.root.update_idletasks()
                            
                        except UnicodeDecodeError:
                            print(f"Warning: Could not decode {file}. Skipping...")
                        except Exception as e:
                            print(f"Error processing {file}: {str(e)}")
                
            self.status.set(f"Complete! Extracted {total_files} files")
            messagebox.showinfo("Success", f"Successfully extracted {total_files} files to {output_path}")
            
        except Exception as e:
            self.status.set("Error occurred")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        self.progress['value'] = 0

def main():
    root = tk.Tk()
    app = ZipExtractorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()