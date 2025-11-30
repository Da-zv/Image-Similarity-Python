# image_comparison.py

import shutil
from pathlib import Path
from image_processing import load_image, calculate_histogram, calculate_phash
from comparison import compare_histograms, compare_phash

def process_single_image_comparison(image_path1, image_path2, method):
    if method == 'histogram':
        hist1 = calculate_histogram(load_image(image_path1))
        hist2 = calculate_histogram(load_image(image_path2))
        results = compare_histograms(hist1, hist2)
        print_comparison_results(results)
    elif method == 'phash':
        phash1 = calculate_phash(image_path1)
        phash2 = calculate_phash(image_path2)
        results = {'pHash': compare_phash(phash1, phash2)}
        print_comparison_results(results)

    return results

def process_folder_comparison(reference_image_path, folder_path, threshold, method):
    if method == 'histogram':
        hist1 = calculate_histogram(load_image(reference_image_path))
    elif method == 'phash':
        phash1 = calculate_phash(reference_image_path)

    folder_path = Path(folder_path)
    destination_folder = folder_path / reference_image_path.stem

    create_directory(destination_folder)

    for image_path in folder_path.glob('*'):
        if image_path.suffix.lower() in ['.jpg', '.png', '.jpeg', '.bmp']:
            if method == 'histogram':
                hist2 = calculate_histogram(load_image(image_path))
                results = compare_histograms(hist1, hist2)
            elif method == 'phash':
                phash2 = calculate_phash(image_path)
                results = {'pHash': compare_phash(phash1, phash2)}

            score = sum(results.values()) / len(results)
            if score > threshold:
                copy_file(image_path, destination_folder / image_path.name)

def sort_folder_to_folders(folder_path, threshold, method):
    folder_path = Path(folder_path)
    images_to_process = [image_path for image_path in folder_path.glob('*') if image_path.suffix.lower() in ['.jpg', '.png', '.jpeg', '.bmp']]

    while images_to_process:
        image_path = images_to_process.pop(0)
        if not image_path.exists():
            continue  # Skip if the image has already been moved

        if method == 'histogram':
            hist1 = calculate_histogram(load_image(image_path))
        elif method == 'phash':
            phash1 = calculate_phash(image_path)

        destination_folder = folder_path / image_path.stem
        create_directory(destination_folder)

        current_images_to_process = [p for p in folder_path.glob('*') if p.suffix.lower() in ['.jpg', '.png', '.jpeg', '.bmp'] and p != image_path]

        for other_image_path in current_images_to_process:
            if method == 'histogram':
                hist2 = calculate_histogram(load_image(other_image_path))
                results = compare_histograms(hist1, hist2)
            elif method == 'phash':
                phash2 = calculate_phash(other_image_path)
                results = {'pHash': compare_phash(phash1, phash2)}

            score = sum(results.values()) / len(results)
            if score > threshold:
                try:
                    shutil.move(str(other_image_path), str(destination_folder / other_image_path.name))
                except Exception as e:
                    print(f"Failed to move file: {e}")

    print("Processing complete.")

def create_directory(directory):
    Path(directory).mkdir(parents=True, exist_ok=True)

def copy_file(src, dst):
    try:
        shutil.copy(src, dst)
        print(f"File copied: {src} -> {dst}")
    except IOError as e:
        print(f"Error copying file: {e}")

def print_comparison_results(results):
    print("Comparison Results:")
    for method, value in results.items():
        print(f"{method}: {value}%")
