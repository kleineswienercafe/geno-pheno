from lib.gploader import GpEntry
from lib.gputils import GpConfig
from sklearn.manifold import TSNE

import matplotlib.pyplot as plt
import seaborn as sns


def applytsne(pd, header):

    tsne = TSNE(
        # n_iter=1000,
        # learning_rate=30,
        # early_exaggeration=5,
        perplexity=10,
        random_state=42,
        # method="exact",
        init="pca"
    )

    embedding = tsne.fit_transform(pd[header])
    return embedding

def applyumap(pd, header):
    import umap

    reducer = umap.UMAP(
        n_neighbors=5,
        # min_dist=0.25,
        random_state=42,
        metric='hamming'
    )
    embedding = reducer.fit_transform(pd[header])

    return embedding

class GpPlot:

    def __init__(self, c: GpConfig = GpConfig()):

        self.config = c
        self.fig = None
        self.scp = None

        self.extra_artists = list()

    def ax(self):
        return plt.gca()

    @classmethod
    def plot(self):
        pass

    """
    save and/or show the plot
    """
    def render(self):

        fs = self.fig.suptitle(self.config.title, fontsize=16)
        self.extra_artists.append(fs)

        # save or show what we got
        if self.config.show:
            plt.show()

        if self.config.save:

            if self.config.svg:
                fps = self.config.resultDir() + self.config.title + ".svg"
                plt.savefig(fps, bbox_extra_artists=self.extra_artists, bbox_inches='tight')

            fpp = self.config.resultDir() + self.config.title + ".png"
            plt.savefig(fpp, dpi=300, bbox_extra_artists=self.extra_artists,
                        bbox_inches='tight')
            print("figure saved to: " + fpp)

class GpPlotTsne(GpPlot):

    def __init__(self, data, c: GpConfig = GpConfig()):

        GpPlot.__init__(self, c)

        self.data = data

        self.markers = ('o', 'v',  '8', 's', '<',
                        'p', 'h', '^', '>', 'D', 'd', 'H', '*')

        # custom colormap
        self.cmap = None
        self.bgdcol = "#dedede"

    def num_classes(self):
        return len(set(self.data[self.config.categoryName]))

    def plot(self):

        self.fig = plt.figure(figsize=(7, 7))

        self.data = self.data[self.data.visible]

        classes = list(set(self.data['category']))
        classes.sort()

        for idx, cc in enumerate(classes):
            cg = self.data[self.data['category'] == cc]
            col = self.cmap[idx % len(self.cmap)] if self.cmap else None
            m = self.markers[idx % len(self.markers)] if self.markers else None

            ccna = cc if cc else 'unknown'

            self.scp = self.ax().scatter(
                cg['x'], cg['y'],
                s = 35 if col == self.bgdcol else 70,
                c = col,
                label = ccna,
                marker = m,
                edgecolors = 'white', linewidth = 0.5,
                zorder = 0 if col == self.bgdcol else 1
                # ax = self.ax()
            )

        self.ax().get_xaxis().set_visible(False)
        self.ax().get_yaxis().set_visible(False)

        # move legend outside
        lgd = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        self.extra_artists.append(lgd)


class GpPlotInteractive(GpPlotTsne):

    def __init__(self, data, c: GpConfig = GpConfig()):
        GpPlotTsne.__init__(self, data, c)

        self.annotation = None
        self.hoverdata = data

    def plot(self):

        self.data = self.data[self.data.visible]

        ylabels = self.data[self.config.categoryName]

        yls = sorted(list(set(ylabels)))
        lut = dict(zip(yls, sns.color_palette("Set2", len(yls))))
        rc = [lut[x] for x in ylabels]

        # draw
        self.fig = plt.figure(figsize=(7, 7))

        self.scp = plt.scatter(
            self.data['x'], self.data['y'],
            c = rc,
            label = yls,
        )

    """
    show exp ID and labels if the mouse is moved over a dot
    """
    def hover(self, event):

        vis = self.annotation.get_visible()

        if event.inaxes == self.ax():

            c, ind = self.scp.contains(event)
            if c:
                if len(ind["ind"]) > 0:
                    self.update_annotation(ind)
                    self.annotation.set_visible(True)
                    self.fig.canvas.draw_idle()
            elif vis:
                self.annotation.set_visible(False)
                self.fig.canvas.draw_idle()

    def update_annotation(self, ind):

        idx = ind["ind"][0]

        if idx > len(self.hoverdata):
            print("index out of bounds sorry...")
            return

        pos = self.scp.get_offsets()[idx]
        self.annotation.xy = pos

        text = self.get_text(pos)

        self.annotation.set_text(text)
        self.annotation.get_bbox_patch().set_alpha(0.7)

    def get_text(self, pos):

        df = self.hoverdata
        cp = df.loc[df['x'] == pos[0]].loc[df['y'] == pos[1]]

        text = cp.index[0] + " | " + cp["fab"][0] # cp["lineage"][0] + " - " + cp["majorSubtype"][0] + " - " + cp["group"][0]

        return text

    """
    show exp ID and labels if a dot is clicked
    this annotation is persistant in contrast to hover annotations
    """
    def clicked(self, event):

        if event.inaxes == self.ax():

            c, ind = self.scp.contains(event)

            if c:

                if len(ind["ind"]) > 0:
                    idx = ind["ind"][0]
                    pos = self.scp.get_offsets()[idx]
                    txt = self.get_text(pos)
                    self.ax().annotate(txt, xy=pos, xytext=pos + (20, 20), textcoords="offset points",
                                       bbox=dict(boxstyle="round", fc="w"),
                                       arrowprops=dict(arrowstyle="->"))

    """
    we only support live rendering here...
    """
    def render(self):

        self.fig.suptitle(self.config.title, fontsize=16)

        self.annotation = self.ax().annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                                             bbox=dict(boxstyle="round", fc="w"),
                                             arrowprops=dict(arrowstyle="->"))

        self.annotation.set_visible(False)

        self.fig.canvas.mpl_connect("motion_notify_event", self.hover)
        self.fig.canvas.mpl_connect("button_press_event", self.clicked)

        plt.show()

class GpClusterMap(GpPlot):

    def __init__(self, gpd, c: GpConfig = GpConfig()):

        GpPlot.__init__(self, c)

        self.gpd = gpd
        self.cmap = None

    def plot(self):

        data = self.gpd.data()
        xlabels = self.gpd.header()
        ylabels = self.gpd.observation_labels(self.config.categoryName)
        ylabels = [y if y else 'NA' for y in ylabels]

        # colorize the rows
        yls = sorted(list(set(ylabels)))
        lut = dict(zip(yls, sns.hls_palette(len(yls), l=0.5, s=0.8)))
        rc = [lut[x] for x in ylabels]

        if not self.cmap:
            self.cmap = "coolwarm"
        else:
            self.cmap = sns.color_palette(self.cmap).as_hex()

        patientnames = self.gpd.observation_labels("id")

        # self.fig = plt.figure()
        g = sns.clustermap(data,
                           xticklabels=xlabels,
                           yticklabels=patientnames,
                           row_colors=rc,
                           col_cluster=False,
                           row_cluster=False,
                           cmap=self.cmap)

        self.fig = g.fig

        # https://xkcd.com/833/
        ax = g.ax_heatmap

        # add group names
        gci, sparse_ylabels = self.gpd.group_changed_index(self.config.categoryName)
        ax.set_yticks(gci)
        ax.set_yticklabels(sparse_ylabels, fontsize=6)

        ax.set_xlabel("Marker")
        ax.set_ylabel("Patients")

        # label colorbar
        cbar = g.fig.colorbar(ax.collections[0])
        cbar.set_ticks([-1, 0, int(data.max())])
        cbar.set_ticklabels(["NA", "neg", "pos"])
        g.cax.remove()    # hide default colorbar

        # create legend
        for label in yls:
            g.ax_col_dendrogram.bar(0, 0,
                                    color=lut[label],
                                    label=label, linewidth=0)
        g.ax_col_dendrogram.legend(loc="center", ncol=3, fontsize=8)

        # add black lines
        gci, _ = self.gpd.group_changed_index(self.config.categoryName)    # do it again
        ax.hlines(gci,
                  *ax.get_xlim(),
                  linewidth=0.5
                  # colors=[0, 0, 0, .5]
                  )
        # ax.axhline(linewidth=5)

class GpPlotRegression(GpPlot):

    def __init__(self, data, ncat = 1, c: GpConfig = GpConfig()):
        GpPlot.__init__(self, c)

        self.ncat = ncat
        self.data = data

    def plot(self):
        import numpy as np
        self.fig = plt.figure()
        g = sns.heatmap(self.data,
                        # square = True, # fixed aspect ratio of elements
                        cmap=sns.diverging_palette(220, 20, n=99),
                        center=0, vmax=2.5, vmin=-2.5,
                        yticklabels=1,
                        xticklabels=self.ncat,
                        )
        g.set_xticklabels(g.get_xmajorticklabels(), fontsize=6)
        # workaround https://github.com/matplotlib/matplotlib/issues/14675
        g.set_ylim([0, self.data.shape[0]])
        # add black lines
        g.vlines(np.arange(start=0, stop=self.data.shape[1], step=self.ncat),
                 *g.get_ylim(),
                 linewidth=0.5,
                 colors=[0, 0, 0, .5]
                 )

        # move colorbar
        # g.cax.set_position((0.92,0.12,0.03,0.1))
        #self.fig = g
