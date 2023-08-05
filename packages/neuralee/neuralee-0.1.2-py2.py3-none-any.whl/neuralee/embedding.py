import time
import copy
import sys
import os
from tqdm import trange

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

from ._aux import error_ee, error_ee_cpu, error_ee_cuda, ls_ee, eloss
from torch.utils.data import DataLoader, TensorDataset


class FCLayers(nn.Module):
    def __init__(self, di, do):
        super(FCLayers, self).__init__()

        self.net = nn.Sequential(

            nn.Linear(di, 50),
            nn.BatchNorm1d(50),
            nn.ReLU(),
            nn.Linear(50, 50),
            nn.BatchNorm1d(50),
            nn.ReLU(),
            nn.Linear(50, do),
        )
        for m in self.net.modules():
            if isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, mean=0, std=0.1)
                nn.init.constant_(m.bias, val=0)

    def forward(self, y):
        return self.net(y)


class NeuralEE(object):
    """NeuralEE method.

    Attributes:
    ----------
    dataset : GeneExpressionDataset
        main attribute Y of dataset is N x D training matrix.
        N is dataset size, D is high original feature dimension.
    d : scalar, int, optional
        low embedded dimension. Default: 2.
    lam : scalar, optional
        lambda value for elastic embedding function. Default: 10.
    device : torch.device, optional
        device chosen to compute. Default: torch.device('cpu').

    """
    def __init__(self, dataset, d=2, lam=10, device=None):
        self.dataset = dataset
        self.d = d
        self.lam = lam
        self.device = device if device is not None else torch.device('cpu')
        self.Y = torch.from_numpy(self.dataset.Y)
        self.Y_splits = torch.from_numpy(self.dataset.Y_splits) \
            if hasattr(self.dataset, 'Y_splits') else None
        self.Wp = torch.from_numpy(self.dataset.Wp) \
            if hasattr(self.dataset, 'Wp') else None
        self.Wn = torch.from_numpy(self.dataset.Wn) \
            if hasattr(self.dataset, 'Wn') else None
        self.Lps = torch.from_numpy(self.dataset.Lps) \
            if hasattr(self.dataset, 'Lps') else None
        self.Wns = torch.from_numpy(self.dataset.Wns) \
            if hasattr(self.dataset, 'Wns') else None

    def __len__(self):
        return len(self.dataset)

    @property
    def D(self):
        return self.Y.shape[1]

    @property
    def labels(self):
        return self.dataset.labels.squeeze()

    @staticmethod
    def _loss(Y, Wp, Wn, lam, net, device, calculate_error):
        results = dict()
        with torch.no_grad():
            net.eval()
            net.to(device)
            X = net(Y.to(device))
        results['X'] = X.cpu()
        if calculate_error is not None:
            assert calculate_error in ['cpu', 'cuda']
            if calculate_error == 'cpu':
                e = error_ee_cpu(X.cpu().numpy(), Wp, Wn, lam)
                results['e'] = e
            else:
                e = error_ee_cuda(X, Wp, Wn, lam)
                results['e'] = e.item()

        return results

    def _loss_entire(self, calculate_error=None):
        return self._loss(
            self.Y, self.Wp, self.Wn, self.lam, self.net, self.device,
            calculate_error=calculate_error)

    def EE(self, size=1., maxit=200, tol=1e-5, frequence=None, aff='ea',
           perplexity=20.0):
        """Free Elastic embedding (no mapping).

        Fast training of nonlinear embeddings using the spectral direction for
        the Elastic Embedding (EE) algorithm.

        Reference:
            Partial-Hessian Strategies for Fast Learning of Nonlinear
            Embeddings.
            http://faculty.ucmerced.edu/mcarreira-perpinan/papers/icml12.pdf

        Parameters
        -----------
        size : scalar, int or float in [0, 1], optional
            subsample of entire dataset to embed. Default: 1.0, not subsample.
            If subsample, the affinity will be recalculated on subsmaples.
        maxit : scalar, int, optional
            max number of iterations for EE. Default: 200.
        tol : scalar, optional
            minimum relative distance between consecutive X. Default: 1e-5.
        frequence : None or int, scalar, optional
            frequence to display iterating results. Defualt: None, not display.
        aff : {'ea', 'x2p'}, optional
            affinity used to calculate attractive weights if subsampled.
            Default: 'ea'.
        perplexity : scalar, optional
            perplexity defined in elastic embedding function if subsampled.
            Default: 20.0.

        Returns
        ----------
        results : dict
            X : embedding results.
            e : embedding loss.
            sub_samples : subsamples information if subsampled.
                Y : original feature on subsamples.
                labels : labels on subsamples.
                Wp : attractive weights on subsamples.
                Wn : repulsive weights on subsamples.
        """

        since = time.time()
        N = len(self)
        results = dict()
        N_sub = size if isinstance(size, int) else int(N * size)
        assert N_sub <= 15000, \
            'Number of samples is too huge for free EE.'
        X0 = 1e-5 * torch.randn(N_sub, self.d)
        if N_sub == N:
            assert self.Wp is not None, \
                'affinity on entire dataset is needed.'
            Wp = self.Wp
            Wn = self.Wn
        else:
            ind_sub = torch.randperm(N)[: N_sub].tolist()
            Y = self.dataset.Y[ind_sub]
            labels = self.lamabels[ind_sub].squeeze()
            print('Compute affinity on downsample')
            Wp, Wn = self.dataset._affinity(Y, aff, perplexity)
            Wp = torch.from_numpy(Wp)
            Wn = torch.from_numpy(Wn)
            sub_samples = {'Y': torch.from_numpy(Y),
                           'labels': labels,
                           'Wp': Wp,
                           'Wn': Wn}
            results['sub_samples'] = sub_samples

        Wp = Wp.to(self.device)
        Wn = Wn.to(self.device)
        Dp = Wp.sum(dim=1).diagflat()
        Lp4 = 4 * (-Wp + Dp)
        R = torch.cholesky(
            Lp4 + 1e-6 * torch.eye(N_sub, N_sub, device=self.device),
            upper=True)
        invR = R.inverse()
        S = torch.eye(N_sub, N_sub, device=self.device)
        P0 = -S @ invR @ invR.t() @ S.t()
        del R, S, invR, Dp
        torch.cuda.empty_cache()
        Xold = X0.to(self.device)
        e, ker = error_ee(Xold, Wp, Wn, self.lam)
        j = 1
        a = 1
        convcrit = maxit >= 1
        while convcrit:
            WWn = self.lam * Wn * ker
            DDn = WWn.sum(dim=1).diagflat()
            # gradient
            G = (Lp4 - 4 * (-WWn + DDn)) @ Xold
            P = P0 @ G  # spectral direction
            # line search
            X, e, ker, a = ls_ee(Xold, Wp, Wn, self.lam, P, e, G, a)

            convcrit = (j < maxit) and \
                (torch.norm(X - Xold) > tol * torch.norm(Xold))

            Xold = X
            if frequence is not None and j % frequence == 0:
                print('Epoch {}, EE loss is {:.6f}'.format(j, e))
            j += 1
        print('Elastic Embedding, lambda={}, completed in {:.2f}s, '
              'EE loss is {:.6f}'.format(
                self.lam, time.time() - since, e.item()))

        results['X'] = X.cpu()
        results['e'] = e.item()
        torch.cuda.empty_cache()
        return results

    def collate_fn(self, batch):
        y, Lp, Wn = batch[0]
        return y.to(self.device), Lp.to(self.device), Wn.to(self.device)

    def fine_tune(self, optimizer=None, size=1., net=None, frequence=50,
                  verbose=False, maxit=500, calculate_error='cuda',
                  pin_memory=True, aff='ea', perplexity=20.0,
                  save_embedding=None):
        """

        Parameters
        -----------
        optimizer : torch.optim, optional
            optimization for traning neural networks.
            Default: torch.optim.Adam(lr=0.01).
        size : scalar, int or float in [0, 1], optional
            subsample of entire dataset to embed.
            Default: 1.0, not subsample.
            If subsample, the affinity will be recalculated on subsmaples.
        net : torch.nn.Module, optional
            neural networks module as embedding function. Default: FCLayers.
        frequence : None or int, scalar, optional
            frequence to compare and save iterating results. Defualt: 50.
        verbose : bool, optional
            whether to show verbose training loss. Default: False.
        maxit : scalar, int, optional
            max number of iterations for fine tune. Default: 500.
        calculate_error:  {None, 'cuda', 'cpu'}
            device to compute error.
            if None, not compute and frequence ignored. Default: 'cuda'
        pin_memory : bool, optional
            whether to pin data on GPU memory to save time of transfer,
            which depends on your GPU memory. Default: True.
        aff : {'ea', 'x2p'}, optional
            affinity used to calculate attractive weights if subsampled.
            Default: 'ea'.
        perplexity : scalar, optional
            perplexity defined in elastic embedding function if subsampled.
            Default: 20.0.
        save_embedding: bool, optional
            whether to save iterating results accoring to frequence.
            Default: False.

        Returns
        ----------
        results : dict
            X : embedding results.
            e : embedding loss.
            sub_samples : subsamples information if subsampled.
                Y : original feature on subsamples.
                labels : labels on subsamples.
                Wp : attractive weights on subsamples.
                Wn : repulsive weights on subsamples.
        """
        since = time.time()
        results = dict()
        N = len(self)
        N_sub = size if isinstance(size, int) else int(N * size)

        if N_sub != N:
            print('Compute affinity on downsample')
            ind_sub = torch.randperm(N)[: N_sub].tolist()
            Y = self.dataset.Y[ind_sub]
            Wp, Wn = self.dataset._affinity(Y, aff, perplexity)
            Y, = torch.from_numpy(Y)
            Wp = torch.from_numpy(Wp)
            Wn = torch.from_numpy(Wn)
            labels = self.lamabels[ind_sub].squeeze()
            sub_samples = {'Y': Y,
                           'labels': labels,
                           'Wp': Wp,
                           'Wn': Wn}
            results['sub_samples'] = sub_samples
            Y_splits = Y.unsqueeze(0).to(self.device)
            Wp = Wp.to(self.device)
            Lps = (Wp.sum(dim=1).diagflat() - Wp).unsqueeze(0)
            Wns = Wn.unsqueeze(0).to(self.device)
        else:
            assert calculate_error is None or self.Wp is not None, \
                'affinity on entire dataset is needed.'
            assert self.Lps is not None, \
                'affinity is needed.'
            Lps = self.Lps.to(self.device) if pin_memory else self.Lps
            Wns = self.Wns.to(self.device) if pin_memory else self.Wns
            Y_splits = self.Y_splits.to(self.device) \
                if pin_memory else self.Y_splits

        dataset = TensorDataset(Y_splits, Lps, Wns)
        # for speed, only batch_size = 1
        if N_sub != N or pin_memory:
            dataloader = DataLoader(dataset, collate_fn=lambda batch: batch[0])
        else:
            dataloader = DataLoader(dataset, collate_fn=self.collate_fn)

        if save_embedding is not None:
            path = save_embedding + self.dataset.__class__.__name__ + '/'
            if not os.path.exists(path):
                os.makedirs(path)

        flag_pbar = calculate_error is None and verbose

        if net is not None:
            self.net = net
        elif hasattr(self, 'net'):
            pass
        else:
            self.net = FCLayers(self.D, self.d)

        if optimizer is None:
            optimizer = optim.Adam(self.net.parameters(), lr=0.01)

        if calculate_error is not None and frequence is not None:
            best_model_wts = copy.deepcopy(self.net.state_dict())
            best_loss = float('inf')

        self.net.train()
        self.net.to(self.device)
        with trange(maxit, desc="NeuralEE", file=sys.stdout,
                    disable=not flag_pbar) as pbar:
            for epoch in range(1, maxit + 1):
                for inputs, Lp_batch, Wn_batch in dataloader:
                    optimizer.zero_grad()
                    outputs = self.net(inputs)
                    loss = eloss(outputs, Lp_batch, Wn_batch, self.lam)
                    loss.backward()
                    optimizer.step()
                if frequence is not None and epoch % frequence == 0:
                    if calculate_error is not None:
                        if N_sub == N:
                            e = self._loss_entire(
                                calculate_error=calculate_error)['e']
                        else:
                            e = self._loss(
                                Y_splits[0], Wp, Wns[0], self.lam, self.net,
                                self.device, calculate_error)['e']
                        if verbose:
                            print(
                                'Epoch {}, EE loss is {:.6f}'.format(epoch, e))
                        if e < best_loss:
                            best_loss = e
                            best_model_wts = copy.deepcopy(
                                self.net.state_dict())
                    if save_embedding is not None:
                        X = self._loss_entire(
                            calculate_error=None)['X'].numpy()
                        np.save(
                            path + self.dataset.__class__.__name__ +
                            str(epoch), X)
                pbar.update(1)

        if calculate_error is not None and frequence is not None:
            self.net.load_state_dict(best_model_wts)
        if N_sub == N:
            results.update(self._loss_entire(calculate_error=calculate_error))
        else:
            results.update(self._loss(Y_splits[0], Wp, Wns[0], self.lam,
                           self.net, self.device, calculate_error))
        if calculate_error is not None:
            print('Neural Elastic Embedding, lambda={}, completed in {:.2f}s, '
                  'EE loss is {:.6f}'.format(
                    self.lam, time.time() - since, results['e']))
        else:
            print('Neural Elastic Embedding, lambda={}, completed in {:.2f}s.'
                  .format(self.lam, time.time() - since))
        torch.cuda.empty_cache()
        return results

    def map(self, samples=dict(), calculate_error='cuda'):
        """

        Parameters
        -----------
        samples : dict, optional
            Y : samples to map into low-dimensional coordinate.
            labels : samples labels. None is acceptable.
            Wp : attractive weights on samples.
                 None if error need not be calculated.
            Wn : repulsive weights on samples.
                 None if error need not be calculated.
            Default: dict(), mapping on training data.

        calculate_error:  {None, 'cuda', 'cpu'}
            device to compute error.
            if None, not compute and frequence ignored. Default: 'cuda'

        Returns
        ----------
        results : dict
            X : embedding results.
            e : embedding loss.
        """

        if samples == dict():
            assert calculate_error is None or hasattr(self.dataset, 'Wp'), \
                'affinity on entire dataset is needed.'
            samples = {'Y': torch.from_numpy(self.dataset.Y),
                       'labels': self.lamabels,
                       'Wp': None
                       if calculate_error is None else self.dataset.Wp,
                       'Wn': None
                       if calculate_error is None else self.dataset.Wn}
        results = self._loss(
            samples['Y'], samples['Wp'], samples['Wn'], self.lam, self.net,
            self.device, calculate_error)
        if calculate_error is not None:
            print('EE loss is {:.6f}'.format(results['e']))
        torch.cuda.empty_cache()
        return results
