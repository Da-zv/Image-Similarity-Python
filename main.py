import sys
from pathlib import Path
from argument_parser import parse_arguments
from image_comparison import process_single_image_comparison, process_folder_comparison, sort_folder_to_folders

def main():
    args = parse_arguments()

    if args.mode == "compare":
        process_single_image_comparison(Path(args.image1), Path(args.image2), args.method)

    elif args.mode == "compare-folder":
        process_folder_comparison(Path(args.reference_image), Path(args.folder), args.threshold, args.method)

    elif args.mode == "process-folder":
        sort_folder_to_folders(Path(args.folder), args.threshold, args.method)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main()
    else:
        import tkinter as tk
        from GUI import ImageComparisonApp

        root = tk.Tk()
        app = ImageComparisonApp(root)
        root.mainloop()
