import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import numpy as np


def scatter(X, labels=None, cell_types=None, title=None, s=1, fg_kwargs=dict(),
            size=1.0, lg_kwargs=dict()):
    if fg_kwargs == dict():
        fg_kwargs = {'dpi': 200}
    if lg_kwargs == dict():
        lg_kwargs = {'markerscale': 2, 'fontsize': 'xx-small'}

    N = X.shape[0]
    if labels is None:
        labels = np.zeros(N)
    N_sub = size if isinstance(size, int) else int(N * size)
    if N_sub != N:
        ind_sub = np.random.permutation(N)[: N_sub]
        X = X[ind_sub]
        labels = labels[ind_sub]
    label_unique = np.unique(labels)
    if cell_types is not None:
        assert len(cell_types) == len(label_unique), \
            'Labels do not correspond to cell types.'
    jet = plt.get_cmap('jet')  # 'nipy_spectral'
    cNorm = colors.Normalize(vmin=0, vmax=range(len(label_unique))[-1])
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
    plt.figure(**fg_kwargs)
    for il, ll in enumerate(label_unique):
        XX = X[labels == ll, :]
        if cell_types is not None:
            plt.scatter(XX[:, 0], XX[:, 1], s=s, color=scalarMap.to_rgba(il),
                        label=cell_types[ll])
        else:
            plt.scatter(XX[:, 0], XX[:, 1], s=s, color=scalarMap.to_rgba(il),
                        label=str(ll))
    if len(label_unique) != 1:
        plt.legend(**lg_kwargs)
    plt.axis('off')
    if title is not None:
        plt.title(title)
    plt.tight_layout()


def scatter_without_outlier(X, n_outlier=1000, s=0.0001,
                            fg_kwargs={'figsize': [10, 10]},
                            labels=None, cell_types=None, lg_kwargs=dict()):
    median = np.median(X, axis=0)
    X_reduce = X - median
    d2 = (X_reduce ** 2).sum(axis=1)
    ind_remain = d2.argsort()[:: -1][n_outlier:]
    X_reduce = X_reduce[ind_remain]
    if labels is not None:
        labels = labels[ind_remain]
    scatter(X_reduce, s=s, fg_kwargs=fg_kwargs, labels=labels,
            cell_types=cell_types, lg_kwargs=lg_kwargs)


def scatter_with_colorbar(X, labels=None, cell_types=None, title=None, s=1,
                          fg_kwargs=dict(), size=1.0):
    if cell_types is not None:
        assert len(cell_types) == 2, \
            'It only supports polarizable cell types'
    if fg_kwargs == dict():
        fg_kwargs = {'dpi': 200}

    N = X.shape[0]
    N_sub = size if isinstance(size, int) else int(N * size)
    if N_sub != N:
        ind_sub = np.random.permutation(N)[: N_sub]
        X = X[ind_sub]
        labels = labels[ind_sub]
    plt.figure(**fg_kwargs)
    plt.scatter(X[:, 0], X[:, 1], s=s, c=labels)

    if cell_types is not None:
        cbar = plt.colorbar(orientation='horizontal', fraction=0.046, pad=0.04)
        maxl = labels.max()
        minl = labels.min()
        ticks = [minl + (maxl - minl) * 0.1, (minl + maxl) / 2,
                 minl + (maxl - minl) * 0.9]
        cbar.set_ticks(ticks)
        cbar.set_ticklabels([cell_types[0], 'Other', cell_types[1]])

    plt.axis('off')
    if title is not None:
        plt.title(title)
    plt.tight_layout()
