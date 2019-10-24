
import os

class GpConfig:
    
    def __init__(self):
        self.show           = False
        self.save           = True
        self.interactive    = False
        self.title          = "GenoPheno - Studie (Debug)"
        self.plotmode       = "umap"            # [tsne|umap|clustermap]

        # data setup
        self.lineage        = "all"             # default: all    [B|T|My|all]
        self.categoryName   = "groups"           # [category|group|majorSubtype|lineage|mutations]
        self.nanValue       = -.1               # default: float('NaN')

    @staticmethod
    def resultDir():
        return os.path.dirname(os.path.realpath(__file__)) + "/../img/"
