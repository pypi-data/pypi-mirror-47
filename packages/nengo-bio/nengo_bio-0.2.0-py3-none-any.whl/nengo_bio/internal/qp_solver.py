#   nengo_bio -- Extensions to Nengo for more biological plausibility
#   Copyright (C) 2019  Andreas Stöckel
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import collections
import warnings
import multiprocessing
import os

import cvxopt
import numpy as np
import scipy.optimize

from .env_guard import EnvGuard

DEFAULT_TOL = 1e-6
DEFAULT_REG = 1e-1

class CvxoptParamGuard:
    """
    Class used to set relevant cvxopt parameters and to reset them once
    processing has finished or an exception occurs.
    """

    def __init__(self, tol=1e-24, disp=False):
        self.options = {
            "abstol": tol,
            "feastol": tol,
            "reltol": 10 * tol,
            "show_progress": disp
        }

    def __enter__(self):
        # Set the given options, backup old options
        for key, value in self.options.items():
            if key in cvxopt.solvers.options:
                self.options[key] = cvxopt.solvers.options[key]
            cvxopt.solvers.options[key] = value
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restore the old cvxopt options
        for key, value in self.options.items():
            cvxopt.solvers.options[key] = value
        return self

def _solve_qp(Pqp,
              qqp,
              Gqp=None,
              hqp=None,
              Aqp=None,
              bqp=None,
              tol=1e-12,
              disp=True):
    """
    Solves the given quadtratic programing problem

    min    x^T P x + q^T x
    s.t.   Gx <= h
           Ax  = b

    """

    # Solve the QP problem
    with CvxoptParamGuard(tol=tol, disp=disp) as guard:
        res = cvxopt.solvers.qp(
            P=cvxopt.matrix(Pqp.astype(np.double)),
            q=cvxopt.matrix(qqp.astype(np.double)),
            G=None if Gqp is None else cvxopt.matrix(Gqp.astype(np.double)),
            h=None if hqp is None else cvxopt.matrix(hqp.astype(np.double)),
            A=None if Aqp is None else cvxopt.matrix(Aqp.astype(np.double)),
            b=None if bqp is None else cvxopt.matrix(bqp.astype(np.double)))

        return np.array(res["x"])


def _check_basis_pursuit_params(C, d, A, b, G, h):
    """
    Used internally to make sure that the given arguments have the right
    dimensionality.
    """

    # Replace zero-sized matrices with None
    C = None if (not (C is None)) and C.size == 0 else C
    d = None if (not (d is None)) and d.size == 0 else d
    A = None if (not (A is None)) and A.size == 0 else A
    b = None if (not (b is None)) and b.size == 0 else b
    G = None if (not (G is None)) and G.size == 0 else G
    h = None if (not (h is None)) and h.size == 0 else h

    # Make sure either both of the variables in the pairs G, h and A, b are
    # "None" or both of them are not
    assert not (C is None) and not (d is None), "C, d must not be None"
    assert (G is None) == (h is None), "Both G and h must be None"
    assert (A is None) == (b is None), "Both A and b must be None"

    # Make sure d, b, h are vectors
    assert (d is None) or (d.size == d.shape[0]), "d must be a vector"
    assert (b is None) or (b.size == b.shape[0]), "b must be a vector"
    assert (h is None) or (h.size == h.shape[0]), "h must be a vector"

    # Make sure A, C use the same number of variables
    if not A is None:
        assert A.shape[1] == C.shape[1], \
                "Second dimension of A, C, and G (number of variables in " + \
                "the system) must be the same"

    # Make sure C, d and G, h have the same number of constraints
    assert d.shape[0] == C.shape[0], \
            "First dimension of C, d (number of equality constraints) " + \
            "must be the same"
    if not G is None:
        assert G.shape[0] == h.shape[0], \
                "First dimension of G, h (number of inequality " + \
                " constraints) must be the same"

        # Make sure G and C have the same number of variables
        assert G.shape[1] == C.shape[1], \
                "Second dimension of A, C, and G (number of variables in " + \
                "the system) must be the same"

    return C, d, A, b, G, h


def solve_linearly_constrained_quadratic_loss(C,
                                              d,
                                              A=None,
                                              b=None,
                                              G=None,
                                              h=None,
                                              tol=DEFAULT_TOL,
                                              disp=False):
    """
    Solves a problem similar to the basis pursuit problem, but using the L2
    instead of the L1 norm, thus turning the problem into a quadratic program.

    min    || Cx  - d ||_2
    s.t.      Ax  = b
              Gx <= h

    This function is mainly meant for benchmarking the impact of using the L1
    instead of the L2 norm.
    """

    # Make sure the dimensionalities of the input matrices are correct
    C, d, A, b, G, h = _check_basis_pursuit_params(C, d, A, b, G, h)

    # Compute the matrices for the QP problem
    Pqp = C.T @ C
    qqp = -C.T @ d

    # Solve the QP problem
    return _solve_qp(Pqp, qqp, G, h, A, b, tol=tol, disp=disp)


def solve_weights_qp(A,
                     b,
                     valid=None,
                     iTh=0.0,
                     nonneg=True,
                     reg=DEFAULT_REG,
                     tol=DEFAULT_TOL):
    """
    Same as np.linalg.lstsq but uses cvxopt and adds regularisation.
    Additionally allows to solve for negative target values using an
    inequality condition instead of an "equals" condition by marking positive
    samples as "valid".
    """

    #
    # Step 1: Count stuff and setup indices used to partition the matrices
    #         into smaller parts.
    #

    # Compute the number of slack variables required to solve this problem
    n_cstr, n_vars = A.shape
    n_cstr_valid = int(np.sum(valid))
    n_cstr_invalid = n_cstr - int(np.sum(valid))
    n_slack = n_cstr_invalid
    n_vars_total = n_vars + n_slack

    # Variables
    v0 = 0
    v1 = n_vars
    v2 = v1 + n_slack

    # Quadratic constraints
    a0 = 0
    a1 = a0 + n_cstr_valid
    a2 = a1 + n_vars
    a3 = a2 + n_slack

    # Inequality constraints
    g0 = 0
    g1 = g0 + n_cstr_invalid
    g2 = g1 + (n_vars if nonneg else 0)

    #
    # Step 2: Assemble the QP matrices
    #

    # We need balance the re-weight error for the super- (valid) and
    # sub-threshold (invalid) constraints. This is done by dividing by the
    # number of valid/invalid constraints. We need to multiply with the number
    # of constraints since the regularisation factor has been chosen in such a
    # way that the errors are implicitly divided by the number of constraints.
    m1 = np.sqrt(n_cstr / max(1, n_cstr_valid))
    m2 = np.sqrt(n_cstr / max(1, n_cstr_invalid))

    # Copy the valid constraints to Aext
    Aext = np.zeros((a3, n_vars_total))
    bext = np.zeros(a3)
    Aext[a0:a1, v0:v1] = A[valid] * m1
    bext[a0:a1] = b[valid] * m1

    # Regularise the weights
    Aext[a1:a2, v0:v1] = np.eye(n_vars) * np.sqrt(reg)

    # Penalise slack variables
    Aext[a2:a3, v1:v2] = np.eye(n_slack) * m2

    # Form the inequality constraints for the matrices G and h
    G = np.zeros((g2, n_vars_total))
    G[g0:g1, v0:v1] = A[~valid]
    G[g0:g1, v1:v2] = -np.eye(n_slack)
    G[g1:g2, v0:v1] = -np.eye(n_vars) if nonneg else 0.0
    h = np.zeros(G.shape[0])
    h[g0:g1] = iTh

    #
    # Step 3: Solve the QP
    #

    x = solve_linearly_constrained_quadratic_loss(
        Aext, bext, None, None, G, h, tol=tol)
    return x[:n_vars, 0]

class SolverTask(collections.namedtuple('SolverTask', [
        'Apre', 'Jpost', 'w', 'connectivity', 'iTh', 'nonneg', 'renormalise',
        'tol', 'reg', 'use_lstsq', 'valid', 'i', 'n_samples'
    ])):
    pass

def _solve_single(t):
    # Fetch the excitatory and inhibitory pre-neurons
    exc, inh = t.connectivity
    Npre_exc = np.sum(exc)
    Npre_inh = np.sum(inh)
    Npre_tot = Npre_exc + Npre_inh

    # Just abort if there ist nothing to do
    if Npre_tot == 0:
        return t.i, np.zeros((2, 0))

    # Renormalise the target currents to a maximum magnitude of one and adapt
    # the model weights accordingly. Since it holds
    #
    #             w[0] + w[1] * gE + w[2] * gI
    # J(gE, gI) = ---------------------------- ≈ Jpost
    #             w[3] + w[4] * gE + w[5] * gI
    #
    # scaling the first three or last three weight vector components will scale
    # the predicted target current. Scaling w[1], w[2], w[4], w[5] will re-scale
    # the magnitude of the synaptic weights

    # Determine the current scaling factor. This should be about 1e9 / A.
    if t.renormalise:
        # Determine all scaling factors
        Wscale = 1.0e-9
        Λscale = 1.0 / (t.w[1]**2
                        )  # Need to scale the regularisation factor as well

        # Compute synaptic weights in nS
        t.w[[1, 2, 4, 5]] *= Wscale

        # Set w[1]=1 for better numerical stability/conditioning
        t.w[...] /= t.w[1]
    else:
        Wscale, Λscale = 1.0, 1.0

    # Account for the number of samples
    Λscale *= t.n_samples

    # Demangle the model weight vector
    a0, a1, a2, b0, b1, b2 = t.w

    # Clip Jtar to the valid range.
    warning_msgs = []
    if np.abs(b2) > 0 and np.abs(b1) > 0:
        if (a1 / b1) < np.max(t.Jpost):
            warning_msgs.append(
                ("Target currents for neuron {} cannot be reached! {:.3g} ∉ [" +
                 "{:.3g}, {:.3g}]")
            .format(t.i, np.max(t.Jpost), a2 / b2, a1 / b1))
        t.Jpost[...] = t.Jpost.clip(0.975 * a2 / b2, 0.975 * a1 / b1)

    # Split the pre activities into neurons marked as excitatory,
    # as well as neurons marked as inhibitory
    Apre_exc, Apre_inh = t.Apre[:, exc], t.Apre[:, inh]

    # Assemble the "A" and "b" matrices
    A = np.concatenate((
        np.diag(a1 - b1 * t.Jpost) @ Apre_exc,
        np.diag(a2 - b2 * t.Jpost) @ Apre_inh,
    ),  axis=1)
    b = t.Jpost * b0 - a0

    # Solve the least-squares problem, either using QP (including the
    # sub-threshold inequality/"mask_negative") or the lstsq/nnls functions.
    if not t.use_lstsq:
        fws = solve_weights_qp(
            A,
            b,
            valid=t.valid,
            nonneg=t.nonneg,
            iTh=t.iTh * b0 - a0,  # Transform iTh in the same way as the target currents
            reg=t.reg * Λscale,
            tol=t.tol)
    else:
        # Compute Γ and Υ
        Γ = A.T @ A + t.reg * Λscale * np.eye(A.shape[1])
        Υ = A.T @ b

        # Solve for weights using NNLS
        if t.nonneg:
            fws = scipy.optimize.nnls(Γ, Υ, maxiter=10*t.n_samples)[0]
        else:
            fws = np.linalg.lstsq(Γ, Υ, rcond=None)[0]

    return t.i, fws[:Npre_exc] * Wscale, fws[Npre_exc:] * Wscale, warning_msgs


def solve(Apre,
          Jpost,
          ws,
          connectivity=None,
          iTh=None,
          nonneg=True,
          renormalise=True,
          tol=None,
          reg=None,
          use_lstsq=False):
    # Set some default values
    if tol is None:
        tol = DEFAULT_TOL
    if reg is None:
        reg = DEFAULT_REG

    # Fetch some counts
    assert Apre.shape[0] == Jpost.shape[0]
    m = Apre.shape[0]
    Npre = Apre.shape[1]
    Npost = Jpost.shape[1]

    # Use an all-to-all connection if connectivity is set to None
    if connectivity is None:
        connectivity = np.ones((2, Npre, Npost), dtype=np.bool)

    # Create a neuron model parameter vector for each neuron, if the parameters
    # are not already in this format
    assert ws.size == 6 or ws.ndim == 2, "Model weight vector must either be 6-element one-dimensional or a 2D matrix"
    if (ws.size == 6):
        ws = np.repeat(ws.reshape(1, -1), Npost, axis=0)
    else:
        assert ws.shape[0] == Npost and ws.shape[1] == 6, "Invalid model weight matrix shape"

    # Mark all samples as "valid" if valid is None, otherwise select those where
    # the post-current is larger than the threshold current
    if iTh is None:
        valid = np.ones((m, Npost), dtype=np.bool)
        iTh = 0.0
    else:
        valid = Jpost >= iTh

    # Iterate over each post-neuron individually and solve for weights. Do so
    # in parallel.
    tasks = [SolverTask(
        Apre, Jpost[:, i], ws[i], connectivity[:, :, i], iTh,
        nonneg, renormalise, tol, reg, use_lstsq,
        valid[:, i], i, m) for i in range(Npost)]
    WE, WI = np.zeros((2, Npre, Npost))
    with EnvGuard({"OMP_NUM_THREADS": "1"}) as env:
        ctx = multiprocessing.get_context("spawn")
        with ctx.Pool() as pool:
            for i, we, wi, warning_msgs in pool.imap_unordered(_solve_single, tasks):
                for msg in warning_msgs:
                    print('Warning: {}'.format(msg))
                exc, inh = connectivity[:, :, i]
                WE[exc, i], WI[inh, i] = we, wi

    return WE, WI

