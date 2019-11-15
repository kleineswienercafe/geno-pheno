
import os

class GpConfig:
    
    def __init__(self):
        self.show           = False
        self.save           = True
        self.interactive    = True
        self.svg            = False
        self.title          = "GenoPheno - Studie (Debug)"
        self.plotmode       = "clustermap"            # [tsne|umap|clustermap]

        # data setup
        self.lineage        = "all"             # default: all    [B|T|My|all]
        self.categoryName   = "fab"           # [category|group|majorSubtype|lineage|mutations|fab]
        self.nanValue       = -1               # default: float('NaN')

    @staticmethod
    def resultDir():
        return os.path.dirname(os.path.realpath(__file__)) + "/../img/"
