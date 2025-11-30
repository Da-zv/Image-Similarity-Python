# comparison.py

import cv2
import numpy as np

def compare_histograms(hist1, hist2):
    results = {}

    chi_squared = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CHISQR)
    results['CHI-Squared'] = 100 - (chi_squared / 26510.8) * 100

    hellinger = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)
    if hellinger < 0.05:
        results['Hellinger'] = 100 - (hellinger / 0.05) * 100
    else:
        results['Hellinger'] = 0

    correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    results['Correlation'] = ((correlation - 0.955) * 100) / (1 - 0.955)

    intersection = cv2.compareHist(hist1, hist2, cv2.HISTCMP_INTERSECT)
    results['Intersection'] = ((intersection - 52000) * 100) / (65536 - 52000)

    return {k: np.trunc(v) for k, v in results.items()}

def compare_phash(phash1, phash2):
    distance = phash1 - phash2
    max_distance = len(phash1.hash) ** 2
    similarity = 100 - (distance / max_distance) * 100
    return similarity
