from lib.gploader import GpExperimentSheet
from lib.gputils import GpConfig
from lib.vis import GpPlotTsne
from lib.vis import GpPlotInteractive
from lib.vis import GpClusterMap
from lib.vis import GpPlotRegression
from lib.vis import applytsne
from lib.vis import applyumap

def main(args: dict):

    p = GpConfig()

    if args['plotmode']:
        p.plotmode = args['plotmode']

    if args['filepath']:
        gpd = load(args['filepath'])
        gpd.title = " 0-2"
        analyze(gpd)
        visualize([gpd], p)
    elif args['aml']:
        batchAML(p)
    else:
        batch(p)

def batch(c: GpConfig = GpConfig()):
    import os

    cd = os.path.dirname(
        os.path.realpath(__file__))
    
    msg = ""
    gpds = list()

    s1 = cd + "/data/MM_SS_IMZ Studie_Liste 210319_excluded_050719 Studie 0-1.txt"
    gpd = load(s1)
    gpd.title = msg + " 0-1"
    gpds.append(gpd)

    s2 = cd + "/data/MM_SS_IMZ Studie_Liste 210319_excluded_050719 Studie 0-2.txt"
    gpd = load(s2)
    gpd.title = msg + " 0-2"
    gpds.append(gpd)

    s3 = cd + "/data/MM_SS_IMZ Studie_Liste 210319_excluded_050719 Studie 0-6.txt"
    gpd = load(s3)
    gpd.title = msg + " 0-6"
    gpds.append(gpd)
    
    ## uncomment to check if our data is fine
    # check(gpds)
    visualize(gpds, c)


def batchAML(c: GpConfig = GpConfig()):
    import os

    cd = os.path.dirname(
        os.path.realpath(__file__))

    msg = ""
    gpds = list()

    s1 = cd + "/data/Geno_Pheno AML 291019 geno-pheno 0-1.txt"
    gpd = load(s1)
    gpd.title = msg + " AML 0-1"
    gpds.append(gpd)

    s2 = cd + "/data/Geno_Pheno AML 291019 geno-pheno 0-2.txt"
    gpd = load(s2)
    gpd.title = msg + " AML 0-2"
    gpds.append(gpd)

    s3 = cd + "/data/Geno_Pheno AML 291019 geno-pheno 0-6.txt"
    gpd = load(s3)
    gpd.title = msg + " AML 0-6"
    gpds.append(gpd)

    ## uncomment to check if our data is fine
    # check(gpds)
    visualize(gpds, c)

def load(filePath: str, c: GpConfig = GpConfig()):

    gpd = GpExperimentSheet.fromFile(filePath, nanValue=c.nanValue, lineage=c.lineage)
    # gpd.filterHybridMy()

    return gpd

def visualize(gpds: list, c: GpConfig = GpConfig()):
    from sklearn.manifold import TSNE
    from copy import deepcopy
    import lib.logit as lg
    from lib.shame import aml_cmap


    plotter = []
    si = []

    for gpd in gpds:

        if not si:
            si = gpd.sort_index()

        gpd.sort_marker(si)

        if c.plotmode == "clustermap":
            c.title = "clustermap" + gpd.title
            
            gpd.sort_edit_dist_within_groups(c.categoryName)
            plotter = GpClusterMap(gpd, c)

            # super simple: here we set different colormaps
            if "1" in gpd.title:
                plotter.cmap = ["#ffffff", "#70C3E0", "#911616"]
            elif "2" in gpd.title:
                plotter.cmap = ["#ffffff", "#70C3E0", "#7E7989", "#911616"]
            elif "6" in gpd.title:
                plotter.cmap = ["#ffffff", "#70C3E0", "#7992A6", "#7E7989", "#83606D", "#884750", "#8C2F33", "#911616"]

        elif c.plotmode == "tsne" or c.plotmode == "umap":

            c.title = c.plotmode + gpd.title
            # gpd.impaint_nans_within_groups()

            pd = gpd.pdata(categoryNames=c.categoryName)

            if c.plotmode == "tsne":
                embedding = applytsne(pd, gpd.header())
            elif c.plotmode == "umap":
                embedding = applyumap(pd, gpd.header())

            pd['x'] = embedding[:,0]
            pd['y'] = embedding[:,1]

            # activate to show selected groups by MDMD
            # cc = deepcopy(c)
            # tsne_show_groups(gpd, embedding, cc)

            c.title = c.plotmode + gpd.title + " " + c.categoryName

            # show interactive plot
            if c.interactive:
                pi = GpPlotInteractive(pd, c)
                pi.plot()
                pi.render()

            plotter = GpPlotTsne(pd, c)
            plotter.cmap = aml_cmap()

        elif c.plotmode == "analysis":
            import math
            c.title = "regression coefficients," + gpd.title
            [data, scores] = lg.logit(gpd, analysis = False, onehot = False, ncat = int(gpd.title[len(gpd.title)-1])+1)
            plotter = GpPlotRegression(data, 1,c)#int(gpd.title[len(gpd.title)-1])+1, c)
            print(gpd.title)
            if type(scores) != int:
                print("Average Accuracy: %0.3f , CI (95,45%%): [%0.3f, %0.3f]" % (scores.mean(), scores.mean()-scores.std()*2/math.sqrt(len(scores)), scores.mean()+2*scores.std()/math.sqrt(len(scores))))

        if plotter:
            plotter.plot()
            plotter.render()

def check(gpds: list):

    print("[0-1] SELF reporting ----------------------------")
    for e in gpds[0].exps:
        e.checkSelf(gpds[0])

    print("[0-2] SELF reporting ----------------------------")
    for e in gpds[1].exps:
        e.checkSelf(gpds[1])

    print("[0-6] SELF reporting ----------------------------")
    for e in gpds[2].exps:
        e.checkSelf(gpds[2])

    print("[0-2] reporting ----------------------------")
    for e in gpds[0].exps:
        e.check(gpds[1])
        
    print("[0-6] reporting ----------------------------")
    for e in gpds[0].exps:
        e.check(gpds[2])

def analyze(gpd, c = GpConfig()):
   
    # find all MPAL marked experiments in My/T
    # mpals = [x for x in gpd.exps if x.isMpal]
    # mpalsmy = [x for x in mpals if x.lineage == 'My']
    # mpalst = [x for x in mpals if x.lineage == 'T']

    # print(mpalsmy)
    # print(mpalst)
    pass

if __name__ == "__main__":

    import argparse
    import sys

    # argument parser
    parser = argparse.ArgumentParser(description='Visualizer for Geno-Pheno data')

    parser.add_argument('--file', dest='filepath', type=str,
                        help='file path to a valid Geno-Pheno csv')
    parser.add_argument('--plot-mode', dest='plotmode', type=str,
                        help='plot mode [clustermap|tsne|analysis]')
    parser.add_argument('--aml', action='store_true')

    # get args and make a dict from the namespace
    args = vars(parser.parse_args())

    main(args)
