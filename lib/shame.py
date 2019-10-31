

def aml_cmap():
    
    # Gib DS-TMD und M7 die gleiche Farbe, aber belasse verschiedene Symbole.
    cmap = ["#78C044", "#2DAAAC", "#F9A548", "#992063", "#1D4866",
            "#7A9DD2", "#F1696E", "#235934", "#78C044", "#4CA18E"]
    return cmap

def tsne_show_groups(gpd, embedding, c):
    from lib.vis import GpPlotTsne
    
    bt = c.title
    
    # ETV6-RUNX1(rot) versus hyperdiploid(blau) versus alle B-other zusammengenommen(grün), alle anderen grau.
    c.categoryName = "majorSubtype"
    gd = gpd.pdata(categoryNames=c.categoryName)
    gd['x'] = embedding[:, 0]
    gd['y'] = embedding[:, 1]

    cmap = ["#78C044", "#dedede", "#F1696E", "#dedede", "#dedede",
            "#dedede", "#2DAAAC", "#dedede", "#dedede", "#dedede"]
    c.title = bt + " B-other ETV6 TCF3-PBX1"
    ple = GpPlotTsne(gd, c)
    ple.cmap = cmap
    ple.plot()
    ple.render()

    # Nur B-other in sich deutlich voneinander absetzenden Farben, alle anderen grau. (die B/My bei den B-other lassen)
    c.categoryName = "group"
    gd = gpd.pdata(categoryNames=c.categoryName)
    gd['x'] = embedding[:, 0]
    gd['y'] = embedding[:, 1]

    cmap = ["#78C044", "#F9A548", "#2DAAAC", "#992063", "#1D4866",
            "#F1696E", "#235934", "#dedede", "#dedede", "#dedede",
            "#dedede", "#dedede", "#dedede", "#dedede", "#dedede", "#dedede", ]

    c.title = bt + " B-other"
    plb = GpPlotTsne(gd, c)
    plb.cmap = cmap
    plb.plot()
    plb.render()

    # Nur B-BCR-ABL1 bis iAMP21 (siehe unten – aber die KMT2A und KMT2A-AFF1 getrennt) in sich deutlich voneinander absetzenden Farben (sodass die, die nahe liegen deutlich different sind – ev. die Ordnung ändern), alle anderen grau. [0-2]
    c.categoryName = "group"
    gd = gpd.pdata(categoryNames=c.categoryName)
    gd['x'] = embedding[:, 0]
    gd['y'] = embedding[:, 1]

    cmap = ["#dedede", "#dedede", "#dedede", "#dedede", "#dedede",
            "#dedede", "#dedede", "#78C044", "#2DAAAC", "#F9A548",
            "#992063", "#1D4866", "#7A9DD2", "#F1696E", "#235934", "#4CA18E", ]

    c.title = bt + " not B-other"
    plb = GpPlotTsne(gd, c)
    plb.cmap = cmap
    plb.plot()
    plb.render()
