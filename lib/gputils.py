
import os

class GpConfig:
    
    def __init__(self):
        self.show           = False
        self.save           = True
        self.interactive    = False
        self.svg            = False
        self.title          = "GenoPheno - Studie (Debug)"
        self.plotmode       = "umap"            # [tsne|umap|clustermap]
        self.dataset        = "AML"             # [ALL | AML]

        # data setup
        self.lineage        = "all"             # default: all    [B|T|My|all]
        self.categoryName   = "majorSubtype"           # [category|group|majorSubtype|lineage|mutations|fab]
        self.nanValue       = -.1               # default: float('NaN')

        # fix of fix: ignore MDMD categorization
        self.ignoreMutation = True

    @staticmethod
    def resultDir():
        return os.path.dirname(os.path.realpath(__file__)) + "/../img/"
