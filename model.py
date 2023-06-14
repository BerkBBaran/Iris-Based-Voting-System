from os import listdir
from datetime import time
from os import listdir
import os
import scipy.io
from matplotlib import pyplot as plt

from imgutils import *
from multiprocessing import Pool, cpu_count
from itertools import repeat
from fnmatch import filter
import numpy as np
import scipy.io as sio
import os
import warnings
import cv2
import re

import random
import time

warnings.filterwarnings("ignore")

##########################################################################
#  Function which generate the iris template using in the matching
##########################################################################
def encode_iris(arr_polar, arr_noise, minw_length, mult, sigma_f):
    """
    Generate iris template and noise mask from the normalised iris region.
    """
    # convolve with gabor filters
    filterb = gaborconvolve_f(arr_polar, minw_length, mult, sigma_f)
    l = arr_polar.shape[1]
    template = np.zeros([arr_polar.shape[0], 2 * l])
    h = np.arange(arr_polar.shape[0])

    # making the iris template
    mask_noise = np.zeros(template.shape)
    filt = filterb[:, :]

    # quantization and check to se if the phase data is useful
    H1 = np.real(filt) > 0
    H2 = np.imag(filt) > 0

    H3 = np.abs(filt) < 0.0001
    for i in range(l):
        ja = 2 * i

        # biometric template
        template[:, ja] = H1[:, i]
        template[:, ja + 1] = H2[:, i]
        # noise mask_noise
        mask_noise[:, ja] = arr_noise[:, i] | H3[:, i]
        mask_noise[:, ja + 1] = arr_noise[:, i] | H3[:, i]

    return template, mask_noise
def gaborconvolve_f(img, minw_length, mult, sigma_f):
    """
    Convolve each row of an imgage with 1D log-Gabor filters.
    """
    rows, ndata = img.shape
    logGabor_f = np.zeros(ndata)
    filterb = np.zeros([rows, ndata], dtype=complex)

    radius = np.arange(ndata / 2 + 1) / (ndata / 2) / 2
    radius[0] = 1

    # filter wavelength
    wavelength = minw_length

    # radial filter component
    fo = 1 / wavelength
    logGabor_f[0: int(ndata / 2) + 1] = np.exp((-(np.log(radius / fo)) ** 2) /
                                               (2 * np.log(sigma_f) ** 2))
    logGabor_f[0] = 0

    # convolution for each row
    for r in range(rows):
        signal = img[r, 0:ndata]
        imagefft = np.fft.fft(signal)
        filterb[r, :] = np.fft.ifft(imagefft * logGabor_f)

    return filterb


##########################################################################
# Function to extract the feature for the matching process
##########################################################################
def extractFeature(img_filename, eyelashes_threshold=80, multiprocess=True):
    """
    Extract features from an iris image
    """
    # parameters
    eyelashes_threshold = 80
    radial_resolution = 20
    angular_resolution = 240
    minw_length = 18
    mult = 1
    sigma_f = 0.5

    #  segmentation
    im = cv2.imread(img_filename, 0)
    ciriris, cirpupil, imwithnoise = segment(im, eyelashes_threshold,
                                             multiprocess)
    ciriris, cirpupil = read_eye_locations(img_filename)

    if ciriris is None or cirpupil is None:
        return None, None, img_filename
    # normalization
    arr_polar, arr_noise = normalize(imwithnoise, ciriris[1], ciriris[0], ciriris[2],
                                     cirpupil[1], cirpupil[0], cirpupil[2],
                                     radial_resolution, angular_resolution)

    #  feature encoding
    template, mask_noise = encode_iris(arr_polar, arr_noise, minw_length, mult,
                                       sigma_f)

    return template, mask_noise, img_filename

def HammingDistance(template1, mask1, template2, mask2):
    """
    Calculate the Hamming distance between two iris templates.
    """
    hd = np.nan

    # Shifting template left and right, use the lowest Hamming distance
    for shifts in range(-8, 9):
        template1s = shiftbits_ham(template1, shifts)
        mask1s = shiftbits_ham(mask1, shifts)

        mask = np.logical_or(mask1s, mask2)
        nummaskbits = np.sum(mask == 1)
        totalbits = template1s.size - nummaskbits

        C = np.logical_xor(template1s, template2)
        C = np.logical_and(C, np.logical_not(mask))
        bitsdiff = np.sum(C == 1)

        if totalbits == 0:
            hd1 = np.nan
        else:
            hd1 = bitsdiff / totalbits
            if hd1 < hd or np.isnan(hd):
                hd = hd1

    return hd



def shiftbits_ham(template, noshifts):
    """
    Shift the bit-wise iris patterns.
    """
    templatenew = np.zeros(template.shape)
    width = template.shape[1]
    s = 2 * np.abs(noshifts)
    p = width - s

    if noshifts == 0:
        templatenew = template

    elif noshifts < 0:
        x = np.arange(p)
        templatenew[:, x] = template[:, s + x]
        x = np.arange(p, width)
        templatenew[:, x] = template[:, x - p]

    else:
        x = np.arange(s, width)
        templatenew[:, x] = template[:, x - s]
        x = np.arange(s)
        templatenew[:, x] = template[:, p + x]

    return templatenew

def compare_with_multiple_images(image_path, other_image_paths, output_file):
    # Extract features from the input image
    template1, mask1, _ = extractFeature(image_path)

    if template1 is None or mask1 is None:
        print(f"Skipping image {image_path} due to missing .mat file.")
        return  # Return early to avoid the rest of the function

    # Calculate similarity with each other image
    for path in other_image_paths:
        # Extract features from the current image
        template2, mask2, _ = extractFeature(path)

        if template2 is None or mask2 is None:
            print(f"Skipping comparison with image {path} due to missing .mat file.")
            continue  # Continue to the next image

        # Calculate the Hamming distance between the iris templates
        hamming_distance = HammingDistance(template1, mask1, template2, mask2)

        # Calculate similarity as the inverse of the Hamming distance
        similarity = 1.0 - hamming_distance

        output_line = f"Similarity between {image_path} and {path}: {similarity}"
        print(output_line)
        output_file.write(output_line + '\n')
        output_file.flush()  # Flush the buffer to immediately write to the file


def natural_sort_key(s):
    return [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', s)]

def get_image_paths(folder_path):
    image_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]
    return sorted([os.path.join(folder_path, f) for f in image_files])
def find_mat_file(image_path, casia4_locations_dir):
    # Extract the base filename from the path
    base_filename = os.path.basename(image_path)
    # Add '-houghpara.mat' to the end
    mat_filename = base_filename + '-houghpara.mat'
    print("matfilename", mat_filename)
    # Now, search for the file in the casia4_locations directory
    for dirpath, dirnames, filenames in os.walk(casia4_locations_dir):
        for filename in filenames:
            if filename == mat_filename:
                return os.path.join(dirpath, filename)

    # If we got this far, the file wasn't found
    return None
def read_eye_locations(image_name):
    # Find the .mat file path
    mat_file_path = find_mat_file(image_name,"casia4_locations")

    if mat_file_path is None:
        print(f"No .mat file found for image {image_name}")
        return None, None

    # Load .mat file
    mat = scipy.io.loadmat(mat_file_path)

    # Extract variables
    circleiris = mat['circleiris']  # x,y,r locations
    circlepupil = mat['circlepupil']  # x,y,r locations

    circleiris= circleiris.flatten()
    circlepupil=circlepupil.flatten()

    # Return the variables
    return circleiris, circlepupil
def manual_testing_different_person():
    directory_path = 'casia4_images'
    output_file_path = 'different_person_results_casia4.txt'
    all_image_paths = []

    start_time = os.times()

    with open(output_file_path, 'a') as output_file:
        prev_image_path = None
        for folder_name in sorted(os.listdir(directory_path), key=natural_sort_key):
            folder_path = os.path.join(directory_path, folder_name)
            if os.path.isdir(folder_path):
                image_paths = get_image_paths(folder_path)
                all_image_paths.extend(image_paths)  # Add to the list of all image paths
                if len(image_paths) > 0:
                    image_path1 = image_paths[0]
                    # If there's a previous image, compare it with the first image in the current directory
                    if prev_image_path is not None:
                        try:
                            compare_with_multiple_images(prev_image_path, [image_path1], output_file)
                        except FileNotFoundError:
                            print(f"Could not find file for image {image_path1}. Skipping this image.")
                            continue
                    # Update the previous image path for the next iteration
                    prev_image_path = image_path1

    end_time = time.time()
    elapsed_time = end_time - start_time
    elapsed_minutes = elapsed_time / 60  # Convert to minutes

    print("Output written to file:", output_file_path)
    print(f"Elapsed time: {elapsed_minutes} minutes")

    with open(output_file_path, 'a') as output_file:
        output_file.write(f"\nElapsed time: {elapsed_minutes} minutes\n")

def manual_testing_same_person():
    directory_path = 'casia4_images'
    output_file_path = 'same_person_results_casia4.txt'
    all_image_paths = []

    start_time = os.times()

    with open(output_file_path, 'a') as output_file:
        for folder_name in sorted(os.listdir(directory_path), key=natural_sort_key):
            folder_path = os.path.join(directory_path, folder_name)
            if os.path.isdir(folder_path):
                image_paths = get_image_paths(folder_path)
                all_image_paths.extend(image_paths)  # Add to the list of all image paths
                if len(image_paths) > 1:
                    image_path1 = image_paths[0]
                    other_image_paths = image_paths[1:]
                    try:
                        compare_with_multiple_images(image_path1, other_image_paths, output_file)
                    except FileNotFoundError:
                        print(f"Could not find file for one or more images in {folder_path}. Skipping this folder.")
                        continue

        # Randomly compare images from different folders
        for _ in range(100):
            # Randomly select two different image paths
            image_path1, image_path2 = random.sample(all_image_paths, 2)
            # Compare the two images
            compare_with_multiple_images(image_path1, [image_path2], output_file)

    end_time = time.time()
    elapsed_time = end_time - start_time
    elapsed_minutes = elapsed_time / 60  # Convert to minutes

    print("Output written to file:", output_file_path)
    print(f"Elapsed time: {elapsed_minutes} minutes")

    with open(output_file_path, 'a') as output_file:
        output_file.write(f"\nElapsed time: {elapsed_minutes} minutes\n")


def manual_testing_same_person_cas1():
    directory_path = 'CASIA1'
    output_file_path = 'output4.txt'
    all_image_paths = []

    start_time = time.time()

    with open(output_file_path, 'a') as output_file:
        for folder_name in sorted(os.listdir(directory_path), key=natural_sort_key):
            folder_path = os.path.join(directory_path, folder_name)
            if os.path.isdir(folder_path):
                image_paths = get_image_paths(folder_path)
                all_image_paths.extend(image_paths)  # Add to the list of all image paths
                if len(image_paths) > 1:
                    image_path1 = image_paths[0]
                    other_image_paths = image_paths[1:]
                    compare_with_multiple_images(image_path1, other_image_paths, output_file)

        # Randomly compare images from different folders
        for _ in range(100):
            # Randomly select two different image paths
            image_path1, image_path2 = random.sample(all_image_paths, 2)
            # Compare the two images
            compare_with_multiple_images(image_path1, [image_path2], output_file)

    end_time = time.time()
    elapsed_time = end_time - start_time
    elapsed_minutes = elapsed_time / 60  # Convert to minutes

    print("Output written to file:", output_file_path)
    print(f"Elapsed time: {elapsed_minutes} minutes")

    with open(output_file_path, 'a') as output_file:
        output_file.write(f"\nElapsed time: {elapsed_minutes} minutes\n")
def manual_testing_different_person_cas1():
    directory_path = 'CASIA1'
    output_file_path = 'output4.txt'
    all_image_paths = []

    start_time = time.time()

    with open(output_file_path, 'a') as output_file:
        prev_image_path = None
        for folder_name in sorted(os.listdir(directory_path), key=natural_sort_key):
            folder_path = os.path.join(directory_path, folder_name)
            if os.path.isdir(folder_path):
                image_paths = get_image_paths(folder_path)
                all_image_paths.extend(image_paths)  # Add to the list of all image paths
                if len(image_paths) > 0:
                    image_path1 = image_paths[0]
                    # If there's a previous image, compare it with the first image in the current directory
                    if prev_image_path is not None:
                        compare_with_multiple_images(prev_image_path, [image_path1], output_file)
                    # Update the previous image path for the next iteration
                    prev_image_path = image_path1

    end_time = time.time()
    elapsed_time = end_time - start_time
    elapsed_minutes = elapsed_time / 60  # Convert to minutes

    print("Output written to file:", output_file_path)
    print(f"Elapsed time: {elapsed_minutes} minutes")

    with open(output_file_path, 'a') as output_file:
        output_file.write(f"\nElapsed time: {elapsed_minutes} minutes\n")

def get_highest_similarity(image_path, other_image_paths):
    # Extract features from the input image
    template1, mask1, _ = extractFeature(image_path)

    highest_similarity = 0
    highest_similarity_image = None

    # Calculate similarity with each other image
    for path in other_image_paths:
        # Extract features from the current image
        template2, mask2, _ = extractFeature(path)

        # Calculate the Hamming distance between the iris templates
        hamming_distance = HammingDistance(template1, mask1, template2, mask2)

        # Calculate similarity as the inverse of the Hamming distance
        similarity = 1.0 - hamming_distance

        # Check if this similarity is higher than the highest found so far
        if similarity > highest_similarity:
            highest_similarity = similarity
            highest_similarity_image = path

    return highest_similarity, highest_similarity_image


def search_single_folder(desired_folder):
    directory_path = 'CASIA1'
    all_image_paths = []

    folder_path = os.path.join(directory_path, desired_folder)
    if os.path.isdir(folder_path):
        image_paths = get_image_paths(folder_path)
        all_image_paths.extend(image_paths)  # Add to the list of all image paths
        if len(image_paths) > 1:
            image_path1 = image_paths[0]
            other_image_paths = image_paths[1:]
            highest_similarity, highest_similarity_image = get_highest_similarity(image_path1, other_image_paths)

            print(f"Highest similarity is {highest_similarity} found in image {highest_similarity_image}")

            return highest_similarity, highest_similarity_image

if __name__ == '__main__':
    manual_testing_same_person()