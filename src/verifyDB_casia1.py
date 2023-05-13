import os
import cv2
import argparse
from time import time
from utils.extractandenconding import extractFeature, matchingTemplate

if __name__ == '__main__':
    # args
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", type=str,
                        help="../CASIA1/")
    parser.add_argument("--template_dir", type=str, default="src/templates/CASIA1/",
                        help="./templates/CASIA1/")
    parser.add_argument("--threshold", type=float, default=0.38,
                        help="Threshold for matching.")
    args = parser.parse_args()

    # Check if the input file exists
    if not os.path.isfile(args.filename):
        print("Input file not found. Please check the file path.")
        exit(1)

    # Check if the template directory exists
    if not os.path.isdir(args.template_dir):
        print("Template directory not found. Please check the directory path.")
        exit(1)

    # Read the image
    image = cv2.imread(args.filename, cv2.IMREAD_GRAYSCALE)

    if image is None:
        print("Error reading the image file. Please check the file path and integrity.")
        exit(1)

    # timing
    start = time()
    print('\tStart verifying {}\n'.format(args.filename))
    template, mask, filename = extractFeature(args.filename)
    result = matchingTemplate(template, mask, args.template_dir, args.threshold)

    # results
    if result == -1:
        print('\tNo registered sample.')
    elif result == 0:
        print('\tNo sample found.')
    else:
        print('\tsamples found (desc order of reliability):'.format(len(result)))
        for res in result:
            print("\t", res)
    # total time
    end = time()
    print('\n\tTotal time: {} [s]\n'.format(end - start))