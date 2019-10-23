
import os

class GpConfig:
    
    def __init__(self):
        self.show           = False
        self.save           = False
        self.interactive    = True
        self.title          = "GenoPheno - Studie (Debug)"
        self.plotmode       = "tsne"

        # data setup
        self.lineage        = "all"             # default: all    [B|T|My|all]
        self.categoryName   = "lineage"         # [category|group|majorSubtype|lineage]
        self.nanValue       = -1                # default: float('NaN')

    @staticmethod
    def resultDir():
        return os.path.dirname(os.path.realpath(__file__)) + "/../img/"
