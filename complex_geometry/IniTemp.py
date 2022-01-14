#!/usr/bin/env python3
def func(X):
    from numpy import (amax, amin, append, array, asarray, clip, cos, exp,
                       linspace, mgrid, pi, sin, sqrt)
    from numpy.linalg import norm
    from numpy.random import default_rng
    from scipy.interpolate import griddata, interpn
    from scipy.optimize import root
    from scipy.special import erf
    from Constants import (d, domainDim, k, kappa, mantTemp, oceAge,
                           rhoH0, stepLoc, stepWidth, surfTemp)

    def solvStep(var, dist2shall, Z, width, surfTemp, mantTemp, kappa, oceAge,
                 k1, k2, rhoH0, d):
        T, zCON, zOCE = var
        return ((erf(dist2shall / width * 4. - 2.) + 1.) / 2.
                * (zCON - zOCE) + zOCE - Z,
                T - surfTemp - (mantTemp - surfTemp)
                * erf(zOCE / 2. / sqrt(kappa * oceAge)),
                T - (k1 * zCON + k2 - rhoH0 * d ** 2. * exp(-zCON / d)) / 3.)

    depth = clip(domainDim[2] - X[2], 0., domainDim[2])
    x = linspace(-pi, pi, 100)
    y = cos(3 * x + pi / 6) * sin(x / 2 - pi / 3) + x / 2
    y -= amin(y)
    y /= amax(y)
    gridY, gridX = mgrid[stepLoc[1][0]:stepLoc[1][1]:100j,
                         stepLoc[0][0]:stepLoc[0][1]:100j]
    conDepth = (1.2e5 + 6e4 * (gridY - stepLoc[1][0]) / 1.5e6 + 6e4 / sqrt(2)
                * y * sqrt(((gridX - stepLoc[0][0]) / 1.5e6) ** 2
                           + ((gridY - stepLoc[1][0]) / 1.5e6) ** 2))
    randPoints = default_rng(0).integers(0, 100, size=(1000, 2))
    randPoints = append(randPoints, [[0, 0], [0, -1], [-1, 0], [-1, -1]],
                        axis=0)
    data2Int = conDepth[randPoints[:, 0], randPoints[:, 1]]
    firstTrough = asarray(
        (gridX[randPoints[:, 0], randPoints[:, 1]] > stepLoc[0][0] + 7e5)
        & (gridX[randPoints[:, 0], randPoints[:, 1]] < stepLoc[0][1] - 5e5)
        & (gridY[randPoints[:, 0], randPoints[:, 1]] > stepLoc[1][1] - 5e5)
        & (gridY[randPoints[:, 0], randPoints[:, 1]]
           < stepLoc[1][1] - 3e5)).nonzero()
    data2Int[firstTrough[0]] = default_rng(0).random() * 2e4 + 65e3
    seconTrough = asarray(
        (gridX[randPoints[:, 0], randPoints[:, 1]] > stepLoc[0][1] - 5e5)
        & (gridX[randPoints[:, 0], randPoints[:, 1]] < stepLoc[0][1] - 3e5)
        & (gridY[randPoints[:, 0], randPoints[:, 1]] > stepLoc[1][0] + 3e5)
        & (gridY[randPoints[:, 0], randPoints[:, 1]]
           < stepLoc[1][0] + 6e5)).nonzero()
    data2Int[seconTrough[0]] = default_rng(0).random() * 2e4 + 65e3
    thirdTrough = asarray(
        (gridX[randPoints[:, 0], randPoints[:, 1]] > stepLoc[0][0] + 4e5)
        & (gridX[randPoints[:, 0], randPoints[:, 1]] < stepLoc[0][0] + 6e5)
        & (gridY[randPoints[:, 0], randPoints[:, 1]] > stepLoc[1][0] + 5e5)
        & (gridY[randPoints[:, 0], randPoints[:, 1]]
           < stepLoc[1][0] + 7e5)).nonzero()
    data2Int[thirdTrough[0]] = 2.2e5
    iDepth = griddata((gridX[randPoints[:, 0], randPoints[:, 1]],
                       gridY[randPoints[:, 0], randPoints[:, 1]]),
                      data2Int, (gridX, gridY), method='cubic')
    conDepth = interpn((gridY[:, 0], gridX[0, :]), iDepth,
                       (clip(X[1], stepLoc[1][0] + stepWidth / 2,
                             stepLoc[1][1] - stepWidth / 2),
                        clip(X[0], stepLoc[0][0] + stepWidth / 2,
                             stepLoc[0][1] - stepWidth / 2)),
                       method='linear')[0]
    conDepth = clip(conDepth, 6e4, None)
    k2 = k * surfTemp + rhoH0 * d ** 2
    k1 = (k * mantTemp + rhoH0 * d ** 2 * exp(-conDepth / d) - k2) / conDepth
    conTemp = (k1 * depth + k2 - rhoH0 * d ** 2. * exp(-depth / d)) / k
    oceTemp = surfTemp + (mantTemp - surfTemp) * erf(depth / 2.
                                                     / sqrt(kappa * oceAge))
    if depth > amax(iDepth):
        return mantTemp
    elif (X[0] <= stepLoc[0][0] - stepWidth / 2
          or X[0] >= stepLoc[0][1] + stepWidth / 2
          or X[1] <= stepLoc[1][0] - stepWidth / 2
          or X[1] >= stepLoc[1][1] + stepWidth / 2):
        return oceTemp
    elif (X[1] < stepLoc[1][0] + stepWidth / 2
          and X[0] >= stepLoc[0][0] + stepWidth / 2
          and X[0] <= stepLoc[0][1] - stepWidth / 2):
        res = root(solvStep, x0=(900., 8e4, 4e4),
                   args=(X[1] - stepLoc[1][0] + stepWidth / 2, depth,
                         stepWidth, surfTemp, mantTemp, kappa, oceAge, k1,
                         k2, rhoH0, d))
        return res.x[0]
    elif (X[1] > stepLoc[1][1] - stepWidth / 2
          and X[0] >= stepLoc[0][0] + stepWidth / 2
          and X[0] <= stepLoc[0][1] - stepWidth / 2):
        res = root(solvStep, x0=(900., 8e4, 4e4),
                   args=(stepLoc[1][1] + stepWidth / 2 - X[1], depth,
                         stepWidth, surfTemp, mantTemp, kappa, oceAge, k1, k2,
                         rhoH0, d))
        return res.x[0]
    elif (X[0] < stepLoc[0][0] + stepWidth / 2
          and X[1] >= stepLoc[1][0] + stepWidth / 2
          and X[1] <= stepLoc[1][1] - stepWidth / 2):
        res = root(solvStep, x0=(900., 8e4, 4e4),
                   args=(X[0] - stepLoc[0][0] + stepWidth / 2, depth,
                         stepWidth, surfTemp, mantTemp, kappa, oceAge, k1, k2,
                         rhoH0, d))
        return res.x[0]
    elif (X[0] > stepLoc[0][1] - stepWidth / 2
          and X[1] >= stepLoc[1][0] + stepWidth / 2
          and X[1] <= stepLoc[1][1] - stepWidth / 2):
        res = root(solvStep, x0=(900., 8e4, 4e4),
                   args=(stepLoc[0][1] + stepWidth / 2 - X[0], depth,
                         stepWidth, surfTemp, mantTemp, kappa, oceAge, k1, k2,
                         rhoH0, d))
        return res.x[0]
    elif (X[0] < stepLoc[0][0] + stepWidth / 2
          and X[1] < stepLoc[1][0] + stepWidth / 2):
        dist = norm(array(X[:-1]) - array([stepLoc[0][0] + stepWidth / 2,
                                           stepLoc[1][0] + stepWidth / 2]))
        if dist > stepWidth:
            return oceTemp
        res = root(solvStep, x0=(900., 8e4, 4e4),
                   args=(stepWidth - dist, depth,
                         stepWidth, surfTemp, mantTemp, kappa, oceAge,
                         k1, k2, rhoH0, d))
        return res.x[0]
    elif (X[0] < stepLoc[0][0] + stepWidth / 2
          and X[1] > stepLoc[1][1] - stepWidth / 2):
        dist = norm(array(X[:-1]) - array([stepLoc[0][0] + stepWidth / 2,
                                           stepLoc[1][1] - stepWidth / 2]))
        if dist > stepWidth:
            return oceTemp
        else:
            res = root(solvStep, x0=(900., 8e4, 4e4),
                       args=(stepWidth - dist, depth,
                             stepWidth, surfTemp, mantTemp, kappa, oceAge,
                             k1, k2, rhoH0, d))
            return res.x[0]
    elif (X[0] > stepLoc[0][1] - stepWidth / 2
          and X[1] < stepLoc[1][0] + stepWidth / 2):
        dist = norm(array(X[:-1]) - array([stepLoc[0][1] - stepWidth / 2,
                                           stepLoc[1][0] + stepWidth / 2]))
        if dist > stepWidth:
            return oceTemp
        else:
            res = root(solvStep, x0=(900., 8e4, 4e4),
                       args=(stepWidth - dist, depth,
                             stepWidth, surfTemp, mantTemp, kappa, oceAge,
                             k1, k2, rhoH0, d))
            return res.x[0]
    elif (X[0] > stepLoc[0][1] - stepWidth / 2
          and X[1] > stepLoc[1][1] - stepWidth / 2):
        dist = norm(array(X[:-1]) - array([stepLoc[0][1] - stepWidth / 2,
                                           stepLoc[1][1] - stepWidth / 2]))
        if dist > stepWidth:
            return oceTemp
        else:
            res = root(solvStep, x0=(900., 8e4, 4e4),
                       args=(stepWidth - dist, depth,
                             stepWidth, surfTemp, mantTemp, kappa, oceAge,
                             k1, k2, rhoH0, d))
            return res.x[0]
    elif depth >= conDepth:
        return mantTemp
    else:
        return conTemp
