import os

def main(args):

    if args['filepath']:
        dstpath = load(args['filepath'], "geno-pheno 0-1")
        print(dstpath + " written...")
        dstpath = load(args['filepath'], "geno-pheno 0-2")
        print(dstpath + " written...")
        dstpath = load(args['filepath'], "geno-pheno 0-6")
        print(dstpath + " written...")

def load(filepath: str, sheetname: str):
    import pandas as pd

    xlsx = pd.read_excel(filepath, sheet_name=sheetname, index=0)

    dstpath = os.path.splitext(filepath)[0] + " " + sheetname + ".txt"

    with open(dstpath, 'w+', encoding='utf-8') as dst:

        lines = xlsx.to_csv(
            # header=False, 
            sep='\t',
            index=False).split('\n')

        header = True

        for l in lines:

            l = l.replace(';', ',')
            l = l.replace('\t', ';')

            if header:
                l = '#' + l
                header = False

            dst.write(l)

    if not os.path.isfile(dstpath):
        print("could not export to" + dstpath)

    return dstpath

if __name__ == "__main__":
    
    import argparse
    import sys

    # argument parser
    parser = argparse.ArgumentParser(description='Visualizer for Geno-Pheno data')

    parser.add_argument('--file', dest='filepath', type=str,
                        help='file path to a valid Geno-Pheno csv')

    # get args and make a dict from the namespace
    args = vars(parser.parse_args())

    main(args)
