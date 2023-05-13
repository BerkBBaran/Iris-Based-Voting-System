import argparse
import os
from glob import glob
from tqdm import tqdm
from time import time
from scipy.io import savemat
from multiprocessing import cpu_count, Pool
from utils.extractandenconding import extractFeature

def pool_func(file_and_template_dir):
    file, template_dir = file_and_template_dir
    template, mask, _ = extractFeature(file, multiprocess=False)
    basename = os.path.basename(file)
    out_file = os.path.join(template_dir, "%s.mat" % (basename))
    savemat(out_file, mdict={'template': template, 'mask': mask})

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_dir", type=str, default="../CASIA4/*",
                        help="Directory of the dataset")
    parser.add_argument("--template_dir", type=str, default="./templates/CASIA4/",
                        help="Destination of the features database")
    parser.add_argument("--number_cores", type=int, default=cpu_count(),
                        help="Number of cores used in the matching.")
    args = parser.parse_args()

    start = time()
    if not os.path.exists(args.template_dir):
        print("makedirs", args.template_dir)
        os.makedirs(args.template_dir)

    files = glob(os.path.join(args.dataset_dir, "S*?.jpg"))
    n_files = len(files)
    print("N# of files which we are extracting features", n_files)
    pools = Pool(processes=args.number_cores)
    for _ in tqdm(pools.imap_unordered(pool_func, [(file, args.template_dir) for file in files]), total=n_files):
        pass
    end = time()
    print('\nTotal time: {} [s]\n'.format(end-start))

if __name__ == '__main__':
    main()
