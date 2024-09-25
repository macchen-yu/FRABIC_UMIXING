import numpy as np


def FCLS(M, r1, delta):
    # input M: endmember signatures, size [bands, p]
    # input r1: the signature whose abundance is to be estimated
    # input delta: control parameter for ASC (usually set to 1 / (10 * max(max(A))))
    # output abundance: abundance of each material in r1, size [p, 1]
    # output error_vector: error vector, size [bands, 1]

    A = M
    numloop = A.shape[1]
    e = delta
    eA = e * A
    E = np.vstack((np.ones((1, numloop)), eA))
    EtE = np.dot(E.T, E)
    m = EtE.shape[0]
    One = np.ones((m, 1))
    iEtE = np.linalg.inv(EtE)
    iEtEOne = np.dot(iEtE, One)
    sumiEtEOne = np.sum(iEtEOne)
    weights = np.diag(iEtE)

    sample = r1
    er = e * sample
    f = np.vstack((np.ones((1, 1)), er.reshape(-1, 1)))
    Etf = np.dot(E.T, f)

    tol = 1e-7

    # lamdiv2 calculation
    ls = np.dot(iEtE, Etf)
    lamdiv2 = -(1 - np.dot(ls.T, One)) / sumiEtEOne
    x2 = ls - lamdiv2 * iEtEOne
    x2old = x2.copy()

    if np.any(x2 < -tol):
        Z = np.zeros((m, 1))
        iter = 0
        while np.any(x2 < -tol) and iter < m:
            Z[x2 < -tol] = 1
            zz = np.where(Z)[0]
            x2 = x2old.copy()  # Reset x2
            L = iEtE[zz[:, None], zz]
            ab = zz.shape
            lastrow = ab[0]
            lastcol = lastrow
            L = np.pad(L, ((0, 1), (0, 1)), mode='constant', constant_values=0)
            L[lastrow, :ab[0]] = np.dot(iEtE[:, zz].T, One).flatten()
            L[:ab[0], lastcol] = iEtEOne[zz].flatten()
            L[lastrow, lastcol] = sumiEtEOne
            xerow = x2[zz].flatten()
            xerow = np.append(xerow, 0)
            lagra = np.linalg.solve(L, xerow)

            while np.any(lagra[:ab[0]] > 0):  # Reset Lagrange multipliers
                maxneg = weights[zz] * lagra[:ab[0]]
                iz = np.argmax(maxneg)
                Z[zz[iz]] = 0
                zz = np.where(Z)[0]  # Will always be at least one (prove)
                L = iEtE[zz[:, None], zz]
                ab = zz.shape
                lastrow = ab[0]
                lastcol = lastrow
                L = np.pad(L, ((0, 1), (0, 1)), mode='constant', constant_values=0)
                L[lastrow, :ab[0]] = np.dot(iEtE[:, zz].T, One).flatten()
                L[:ab[0], lastcol] = iEtEOne[zz].flatten()
                L[lastrow, lastcol] = sumiEtEOne
                xerow = x2[zz].flatten()
                xerow = np.append(xerow, 0)
                lagra = np.linalg.solve(L, xerow)

            if zz.size > 0:
                x2 -= np.dot(iEtE[:, zz], lagra[:ab[0]].reshape(-1, 1)) + lagra[lastrow] * iEtEOne

            iter += 1

    abundance = x2
    error_vector = np.dot(A, abundance) - r1

    return abundance.flatten(), error_vector.flatten()


