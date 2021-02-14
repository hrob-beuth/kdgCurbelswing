from params import *
import numpy as np


# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––
#       EXPLIZITE BEZIEHUNG VON PHI UND PSI
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––


# EXPLIZITE LÖSUNG VON PSI
# findet psi über den Schnittpunkt von 2 Kreisen
# returned von den zwei Möglichkeiten das 'obere' psi
# TODO: Rechnung übersichtlicher
def solveForPsi(phi):
    g_ = np.array([l0 - l1 * np.cos(phi), -l1 * np.sin(phi)])  # Abstand zwischen B und D
    g = (g_[0] ** 2 + g_[1] ** 2) ** 0.5
    qx = (l2 ** 2 - l3 ** 2 + g ** 2) / (2 * g)
    qy = (l2 ** 2 - qx ** 2) ** .5
    b1 = g_[0] / g * qx - g_[1] / g * qy  # B-Vektor in richitger Basis
    return np.arccos(b1 / l2) + np.pi / 2
