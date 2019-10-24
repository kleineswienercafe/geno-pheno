
import numpy as np

def clean(s: str):

    # remove header marker
    s = s.replace("#", "")
    # remove whitespace
    s = s.strip()
    # remove line break
    s = s.replace("\n", "")

    return s

def reduceToKey(str: str, key: str):
    if key in str:
        return key
    
    return str

class GpEntry:
    """ Stores the statistics of an experiment """

    def __init__(self, data: dict, nanValue: int = float('NaN')):
        
        # get all markers
        self.id = data['PAT Nummer'] + "-" + data['EingangsNr']
        self.patientId = data['PAT Nummer']
        self.lineage = data['Lineage']
        self.majorSubtype = data['Major genetic subtype'] if 'Major genetic subtype' in data else ""
        self.group = data['Group']
        self.mutations = data['Mutations'] if 'Mutations' in data else ""
        self.nanValue = nanValue

        self.isBal = True if 'yes' in data['BAL'] else False
        self.isMpal = True if 'yes' in data['MPAL'] else False

        self.lineage = self.lineage.replace(" ", "")    # remove spaces
        self.lineage = self.lineage.replace("Rez", "")  # BRez -> B

        # fix missing labels by propagating down
        if not self.majorSubtype or self.majorSubtype == 'NA' or self.majorSubtype == 'unlabelled':
            self.majorSubtype = self.lineage

        if not self.group:
           self.group = self.majorSubtype

        # get markers of interest
        # self.marker = [m for m in data.keys() if "CD" in m]

        # default
        self.marker = ['CD123', 'CD45', 'CD34', 'CD44', 'CD99', 'CD10', 
        'CD24', 'CD38', 'iCD79a', 'CD22', 'iCD22', 'CD19', 'CD20', 'CD11a', 'CD13', 
        'CD33', 'CD15', 'CD56', 'CD2', 'CD11b', 'CD7', 'CD5', 'CD117', 
        'CD11c', 'CD65', 'iCD3', 'CD64', 'sCD3', 'CD14', 'CRLF2',
        'iIgM', 'ikappa', 'ilambda', 'MPO', 'HLADR', 'NG2', 'CD371']

        # self.marker = ['CD123', 'CD45', 'CD34', 'CD44', 'CD99', 'CD10',
        #                'CD24', 'iCD79a', 'CD22', 'iCD22', 'CD20', 'CD11a', 'CD13',
        #                'CD33', 'CD15', 'CD56', 'CD2', 'CD11b', 'CD7', 'CD5', 'CD117',
        #                'CD65', 'CRLF2',
        #                'iIgM', 'ilambda', 'MPO', 'NG2']

        self.data = list()
        self.nanCnt = 0

        for m in self.marker:
            try:
                v = int(data[m])
                self.data.append(v)
            except ValueError:
                self.data.append(nanValue)
                self.nanCnt += 1

        # TODO: why don't we initialize it as np array?
        self.data = np.array(self.data)
        
        # clean groups w.r.t. dworzak's definition
        if not self.mutations:
            self.cleanGroups()
        else:
            self.groupsToSubtypeAML()

        # check consistentcy
        # if data['BAL'] != 'yes' and data['BAL'] != 'no':
        #     print("[WARNING] " + self.id + " has an illegal BAL value: " + data['BAL'])
        # if data['MPAL'] != 'yes' and data['MPAL'] != 'no':
        #     print("[WARNING] " + self.id +
        #           " has an illegal MPAL value: " + data['BAL'])
        pass

    def groupsToSubtypeAML(self):

        # NOTE: this is my grouping - we should ask MDMD
        self.majorSubtype = self.group

        if 'KMT2A' in self.group:
            self.majorSubtype = 'KMT2A'
        if 'DS' in self.group:
            self.majorSubtype = 'DS'
        if self.group is 'complex':
            self.majorSubtype = 'complex'
        if 'ETV6' in self.group:
            self.majorSubtype = 'ETV6'
        if 'NUP98' in self.group:
            self.majorSubtype = 'NUP98'

        self.lineage = 'My'

    def cleanGroups(self):

        # CRLF2, IGH-CRLF2, P2RY8-CRLF2
        # PAX5, PAX5-ITA, PAX5-ITA-atyp, PAX5_P80R
        if self.majorSubtype == 'B-other':
            self.group = reduceToKey(self.group, 'CRLF2')
            self.group = reduceToKey(self.group, 'PAX5')
        # # KMT2A, KMT2A-AFF1
        # elif 'KMT2A' in self.majorSubtype:
        #     self.majorSubtype = reduceToKey(self.majorSubtype, 'KMT2A')
        #     self.group = reduceToKey(self.group, 'KMT2A')
        # hyperdiploid_PAX5, hyperdiplod_PAX5, hyperdiploi_CRLF2
        elif self.majorSubtype == 'hyperdiploid':
            self.group = self.group.replace('hyperdiplod', 'hyperdiploid')   # fixes a spelling mistake (?!)
            self.group = reduceToKey(self.group, 'hyperdiploid')
        # IAMP21, iAMP21_CRLF2
        elif self.majorSubtype == 'iAMP21':
            self.group = reduceToKey(self.group, 'iAMP21')
        
        # clean lineage
        if self.lineage == 'T/' or self.lineage == 'T/M' or self.lineage == 'T/My':
            self.lineage = 'T'
        if self.lineage == 'B/My' or self.lineage == 'AUL':
            self.lineage = 'B'
        elif self.lineage == 'MBT' or self.lineage == 'My/B':
            self.lineage = 'My'
        
        # clean subtypes
        if self.majorSubtype == 'T/':
            self.majorSubtype = 'T'

        # clean group
        if self.group == 'T/':
            self.group = 'T'

    def dist(self, o):
        import editdistance

        # replace NaN with 0 
        # sd = np.where(self.data == self.nanValue, 0, self.data)
        # od = np.where(o.data == self.nanValue, 0, o.data)

        # neutralize NaNs
        sd = self.data.copy()
        od = o.data.copy()
        sd[sd == self.nanValue] = od[sd == self.nanValue]
        od[od == self.nanValue] = sd[od == self.nanValue]

        return editdistance.distance(str(sd), str(od))

    def checkSelf(self, gpd):

        idx = 0

        for i, e in enumerate(gpd.exps):
            if self.id == e.id:
                idx = i+1
                break

        siblings = gpd.exps[idx:]
        siblings = [x for x in siblings
                    if x.patientId == self.patientId]

        for s in siblings:
            self.checkSibling(s)

    def check(self, gpd):

        siblings = [x for x in gpd.exps if x.id == self.id]

        if not siblings:
            print(str(self) + " has no sibling")

        if len(siblings) > 1:
            print(str(self) + " has more than one sibling:")
            print(siblings)

        for s in siblings:
            self.checkSibling(s)

    def checkSibling(self, s):

        if self.lineage != s.lineage: 
            print("[" + self.id + "] <-> [" + s.id + "] different lineage: " + self.lineage + " != " + s.lineage)
        elif self.majorSubtype != s.majorSubtype: 
            print("[" + self.id + "] <-> [" + s.id + "] different subtype: " + self.majorSubtype + " != " + s.majorSubtype)
        elif self.group != s.group: 
            print("[" + self.id + "] <-> [" + s.id + "] different group: " + self.group + " != " + s.group)
        # else:
        #     # check the data
        #     for idx in range(len(self.data)):
        #         if self.data[idx] == 0 and s.data[idx] != 0:
        #             print("[" + self.id + "] <-> [" + s.id + "] " + str(self.data[idx]) + " != " + str(s.data[idx]) + " " + self.marker[idx])
        #             break

    def observation_label(self, category = "majorSubtype"):

        if category == "mutations":
            return self.group + " - " + self.mutations
        if category == "group":
            return self.lineage + " - " + self.majorSubtype + " - " + self.group
        elif category == "majorSubtype":
            return self.lineage + " - " + self.majorSubtype

        return self.lineage

    def val(self, marker: str):
        return self.data[self.marker.index(marker)]

    def __str__(self):

        return self.__repr__()

    def __repr__(self):
        msg = "| id " + self.id + " | " + self.lineage + " | " + self.majorSubtype + " | " + self.group + " |"

        return msg

class GpExps:

    def __init__(self, exps = list(), nanValue = float('NaN')):
    
        # metadata
        self.nanValue = nanValue
        self.exps = exps

    def __str__(self):
    
        msg = ""

        idx = 0
        for e in self.exps[:42]:
            msg += str(idx) + ": " + str(e) + "\n"
            idx += 1
            
        if len(self.exps) > 42:
            msg += "... and more elements (" + str(len(self.exps)) + " in total)"

        return msg

    def __bool__(self):
        return self.exps != []

    def __gt__(self, o):
        # TODO
        # if self.fscore() > o.fscore():
        #     return True
        # else:
        return False

    def exps_by_label(self, name, category = "majorSubtypes"):
    
        return GpExps([x for x in self.exps if x.observation_label(category) == name], self.nanValue)

    def sort_index(self):

        d = self.data()
        d[np.isnan(d)] = 0.0    # ignore NaNs
        cs = (np.sum(d, 0)+np.sum(abs(d), 0)) / 2  # sum positive values only (no -1)
        si = [x for x in cs.argsort()[::-1]]  # -::1 == sort descending

        return si

    def sort_marker(self, si):

        for e in self.exps:
            e.data = e.data[si]
            e.marker = [e.marker[idx] for idx in si]

    def sort_edit_dist_within_groups(self, categoryName = "majorSubtype"):

        groups = list(set(self.observation_labels(categoryName)))
        groups.sort()

        sexps = []

        for g in groups:
            gexps = self.exps_by_label(g, categoryName)
            gexps.sort_edit_dist()

            sexps += gexps.exps

        self.exps = sexps
    
    def sort_edit_dist(self):

        if not self:
            return

        p = [x.dist(self.exps[0]) for x in self.exps]
        si = sorted(range(len(self.exps)), key=lambda k: p[k])
        self.exps = [self.exps[idx] for idx in si]

    def impaint_nans_within_groups(self):

        groups = list(set(self.observation_labels("group")))
        groups.sort()

        sexps = []

        for g in groups:
            ge = self.exps_by_label(g, "group")
            mm = ge.median_marker()
            mm[mm==self.nanValue] = 0

            for e in ge.exps:
                e.data[e.data==self.nanValue] = mm[e.data==self.nanValue]

            sexps += ge.exps

        self.exps = sexps

    def median_marker(self):

        d = self.data()
        d[np.isnan(d)] = 0.0    # ignore NaNs
        mv = np.median(d, axis=0)

        return mv

    def header(self):
    
        if not self.exps:
            return []

        return self.exps[0].marker

    def observation_labels(self, category="majorSubtype"):
        return [x.observation_label(category) for x in self.exps]

    def len(self):
        return len(self.exps)

    def data(self):

        if not self.exps:
            return np.array(0)

        m = np.ones((len(self.exps), len(self.exps[0].data)))

        for idx, e in enumerate(self.exps):
            m[idx] = e.data

        return m

    def pdata(self, categoryNames="group"):
        import pandas as pd

        df = pd.DataFrame(self.data(), 
                          columns = self.header(), 
                          index = [x.id for x in self.exps])

        df['lineage']         = [x.lineage for x in self.exps]
        df['majorSubtype']    = [x.majorSubtype for x in self.exps]
        df['group']           = [x.group for x in self.exps]
        df['mutations']       = [x.mutations for x in self.exps]
        df['category']        = self.observation_labels(categoryNames)

        return df

    def adata(self):
        import anndata as ad

        data = ad.AnnData(self.data(), var = self.header(), obs = self.observation_labels())
        return data

    def group_changed_index(self, category="majorSubtype"):
    
        gci = []
        gcl = []
        lc = self.exps[0].observation_label(category)

        for idx, exp in enumerate(self.exps):
            cc = exp.observation_label(category)
            if lc != cc:
                gci.append(idx)
                gcl.append(self.exps[idx-1].group)
                lc = cc

        gci.append(len(self.exps)-1)
        gcl.append(self.exps[-1].group)

        return gci, gcl


class GpExperimentSheet(GpExps):
    """ Stores all geno-pheno data. """

    def __init__(self, data=[], path: str = "", nanValue = float('NaN'), lineage = 'all'):
        
        GpExps.__init__(self, nanValue = nanValue)

        # metadata
        self.title = ""

        self.path = path
        self.rawHeader = []

        self.readHeader(data)
        exps = self.parse(data)

        # get filename (independent to dir separators)
        self.fname = path.split("/")[-1]
        self.fname = self.fname.split("\\")[-1]

        # filter experiments
        if lineage is not "all":
            exps = [x for x in exps if x.lineage == lineage]              # filter lineage
        exps = [x for x in exps if x.lineage]                             # non-empty lineage
        exps = [x for x in exps if x.patientId != '40956']                # this patient has illegal values
        exps = [x for x in exps if x.group != 'NA']                       # remove unknown subtypes

        # sort w.r.t genes
        exps.sort(key=lambda x: (x.lineage, x.majorSubtype, x.group, x.id))

        self.exps = list(exps)

        print(str(len(self.exps)) + " experiments are considered")

    # @depricated?!
    def filterHybridMy(self):
        self.exps = [x for x in self.exps 
            if  x.majorSubtype != 'T/My'    and
                x.majorSubtype != 'T/M'     and
                x.majorSubtype != 'B/My'    and
                x.majorSubtype != 'My/B'    and
                x.majorSubtype != 'MBT'
                ]

        print(str(len(self.exps)) + " experiments after filtering hybrid")

    def dir(self):
        import os
        return os.path.dirname(self.path)

    def readHeader(self, data):

        for cnt, line in enumerate(data):
            if line.startswith("#"):
                self.rawHeader = [(lambda s: clean(s))(s)
                               for s in line.split(";")]
                self.dataStart = cnt
                return

        print("WARNING: no header found...")

    def parse(self, data):

        exps = []

        for line in data:

            d = dict()
            df = [(lambda s: clean(s))(s) for s in line.split(";")]

            # remove empty entries
            # df = [s for s in df if s]

            for cnt, s in enumerate(df):
                # ignore empty columns at the end
                if cnt < len(self.rawHeader):
                    d[self.rawHeader[cnt]] = s

            # ignore empty rows
            if d:
                gpe = GpEntry(d, nanValue=self.nanValue)

                # only append non-empty entries
                if gpe.id and gpe.nanCnt < 12:
                    exps.append(gpe)
                # elif gpe.nanCnt >= 10:
                #     print(str(gpe.id) + " removed because it has " + str(gpe.nanCnt) + " NaNs")

        print(str(len(exps)) + " experiments found")
        
        return exps

    @staticmethod
    def fromFile(filePath: str, nanValue = float('NaN'), lineage = 'all'):
        import io

        with open(filePath, 'r', encoding='utf-8') as infile:
            buf = io.StringIO(str(infile.read()))
            return GpExperimentSheet(buf, filePath, nanValue, lineage)

        return GpExperimentSheet()
