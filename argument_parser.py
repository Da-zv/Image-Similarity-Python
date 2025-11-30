# argument_parser.py

import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Image Comparison Program")

    subparsers = parser.add_subparsers(dest="mode", required=True, help="Mode of operation")

    # Subparser for single image comparison
    single_compare_parser = subparsers.add_parser("compare", help="Compare two images")
    single_compare_parser.add_argument("image1", type=str, help="Path to the first image")
    single_compare_parser.add_argument("image2", type=str, help="Path to the second image")
    single_compare_parser.add_argument("method", choices=['histogram', 'phash'], help="Comparison method to use")

    # Subparser for folder comparison
    folder_compare_parser = subparsers.add_parser("compare-folder", help="Compare one image against all images in a folder")
    folder_compare_parser.add_argument("reference_image", type=str, help="Path to the reference image")
    folder_compare_parser.add_argument("folder", type=str, help="Path to the folder containing images to compare")
    folder_compare_parser.add_argument("threshold", type=float, help="Threshold for comparison")
    folder_compare_parser.add_argument("method", choices=['histogram', 'phash'], help="Comparison method to use")

    # Subparser for multiple folder processing
    multiple_folder_parser = subparsers.add_parser("process-folder", help="Process all images in a folder and organize similar images into subfolders")
    multiple_folder_parser.add_argument("folder", type=str, help="Path to the folder containing images to process")
    multiple_folder_parser.add_argument("threshold", type=float, help="Threshold for comparison")
    multiple_folder_parser.add_argument("method", choices=['histogram', 'phash'], help="Comparison method to use")

    parser.add_argument("--pause", action="store_true", help="Pause at the end of execution")

    return parser.parse_args()
