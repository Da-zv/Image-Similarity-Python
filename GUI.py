# gui.py

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path
from image_comparison import process_single_image_comparison, process_folder_comparison, sort_folder_to_folders


class ImageComparisonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Comparison App")

        self.mode_var = tk.StringVar(value="compare")  # Set default mode to "compare"
        self.method_var = tk.StringVar(value="histogram")  # Set default method to "histogram"

        self.create_widgets()
        self.show_image_selection()  # Show image selection widgets by default

    def create_widgets(self):
        # Mode selection
        mode_label = ttk.Label(self.root, text="Select Mode:")
        mode_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        modes = [("Single Image Comparison", "compare"),
                 ("Folder Comparison", "compare-folder"),
                 ("Process to Multiple Folders", "process-folder")]

        for i, (text, mode) in enumerate(modes):
            mode_radio = ttk.Radiobutton(self.root, text=text, variable=self.mode_var, value=mode,
                                         command=self.on_mode_change)
            mode_radio.grid(row=i + 1, column=0, padx=10, pady=2, sticky="w")

        # Comparison method selection
        method_label = ttk.Label(self.root, text="Select Comparison Method:")
        method_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        methods = [("Histogram", "histogram"),
                   ("pHash", "phash")]

        for i, (text, method) in enumerate(methods):
            method_radio = ttk.Radiobutton(self.root, text=text, variable=self.method_var, value=method)
            method_radio.grid(row=i + 1, column=1, padx=10, pady=2, sticky="w")

        # Input fields and buttons
        self.image1_entry = ttk.Entry(self.root, width=50)
        self.image1_entry.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        self.image2_entry = ttk.Entry(self.root, width=50)
        self.image2_entry.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        self.select_image1_button = ttk.Button(self.root, text="Select Image 1", command=self.select_image1)
        self.select_image1_button.grid(row=4, column=2, padx=5, pady=5)

        self.select_image2_button = ttk.Button(self.root, text="Select Image 2", command=self.select_image2)
        self.select_image2_button.grid(row=5, column=2, padx=5, pady=5)

        self.reference_image_label = ttk.Label(self.root, text="Reference Image:")
        self.reference_image_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.reference_image_entry = ttk.Entry(self.root, width=50)
        self.reference_image_entry.grid(row=6, column=1, columnspan=2, padx=10, pady=5)

        self.select_reference_image_button = ttk.Button(self.root, text="Select Reference Image",
                                                        command=self.select_reference_image)
        self.select_reference_image_button.grid(row=6, column=3, padx=5, pady=5)

        self.folder_label = ttk.Label(self.root, text="Folder Path:")
        self.folder_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")
        self.folder_entry = ttk.Entry(self.root, width=50)
        self.folder_entry.grid(row=7, column=1, columnspan=2, padx=10, pady=5)

        self.select_folder_button = ttk.Button(self.root, text="Select Folder", command=self.select_folder)
        self.select_folder_button.grid(row=7, column=3, padx=5, pady=5)

        self.threshold_label = ttk.Label(self.root, text="Threshold:")
        self.threshold_label.grid(row=8, column=0, padx=10, pady=5, sticky="w")
        self.threshold_entry = ttk.Entry(self.root)
        self.threshold_entry.grid(row=8, column=1, padx=10, pady=5)

        # Run button
        ttk.Button(self.root, text="Run", command=self.run_comparison).grid(row=9, column=1, columnspan=2, pady=10)

        # Initially hide input widgets
        self.hide_input_widgets()

    def on_mode_change(self):
        mode = self.mode_var.get()
        if mode == "compare":
            self.show_image_selection()
        elif mode == "compare-folder":
            self.show_reference_image_selection()
        elif mode == "process-folder":
            self.show_folder_selection()
        else:
            self.hide_input_widgets()

    def hide_input_widgets(self):
        self.image1_entry.grid_remove()
        self.image2_entry.grid_remove()
        self.select_image1_button.grid_remove()
        self.select_image2_button.grid_remove()
        self.reference_image_label.grid_remove()
        self.reference_image_entry.grid_remove()
        self.select_reference_image_button.grid_remove()
        self.folder_label.grid_remove()
        self.folder_entry.grid_remove()
        self.select_folder_button.grid_remove()
        self.threshold_label.grid_remove()
        self.threshold_entry.grid_remove()

    def show_image_selection(self):
        self.hide_input_widgets()
        self.image1_entry.grid()
        self.image2_entry.grid()
        self.select_image1_button.grid()
        self.select_image2_button.grid()

    def show_reference_image_selection(self):
        self.hide_input_widgets()
        self.reference_image_label.grid()
        self.reference_image_entry.grid()
        self.select_reference_image_button.grid()
        self.folder_label.grid()
        self.folder_entry.grid()
        self.select_folder_button.grid()
        self.threshold_label.grid()
        self.threshold_entry.grid()

    def show_folder_selection(self):
        self.hide_input_widgets()
        self.folder_label.grid()
        self.folder_entry.grid()
        self.select_folder_button.grid()
        self.threshold_label.grid()
        self.threshold_entry.grid()

    def select_image1(self):
        image_path = filedialog.askopenfilename(title="Select Image 1")
        if image_path:
            self.image1_entry.delete(0, tk.END)
            self.image1_entry.insert(0, image_path)

    def select_image2(self):
        image_path = filedialog.askopenfilename(title="Select Image 2")
        if image_path:
            self.image2_entry.delete(0, tk.END)
            self.image2_entry.insert(0, image_path)

    def select_reference_image(self):
        image_path = filedialog.askopenfilename(title="Select Reference Image")
        if image_path:
            self.reference_image_entry.delete(0, tk.END)
            self.reference_image_entry.insert(0, image_path)

    def select_folder(self):
        folder_path = filedialog.askdirectory(title="Select Folder")
        if folder_path:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder_path)

    def run_comparison(self):
        mode = self.mode_var.get()
        method = self.method_var.get()
        if mode == "compare":
            image1_path = self.image1_entry.get()
            image2_path = self.image2_entry.get()
            results = process_single_image_comparison(Path(image1_path), Path(image2_path), method)
            self.show_results(results)
        elif mode == "compare-folder":
            reference_image_path = self.reference_image_entry.get()
            folder_path = self.folder_entry.get()
            threshold = float(self.threshold_entry.get())
            process_folder_comparison(Path(reference_image_path), Path(folder_path), threshold, method)
        elif mode == "process-folder":
            folder_path = self.folder_entry.get()
            threshold = float(self.threshold_entry.get())
            sort_folder_to_folders(Path(folder_path), threshold, method)

    def show_results(self, results):
        results_window = tk.Toplevel(self.root)
        results_window.title("Comparison Results")

        results_label = ttk.Label(results_window, text="Comparison Results")
        results_label.pack(pady=10)

        for method, value in results.items():
            ttk.Label(results_window, text=f"{method}: {value}%").pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageComparisonApp(root)
    root.mainloop()
