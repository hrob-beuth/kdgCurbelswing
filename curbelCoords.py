import numpy as np
from numpy import sin, cos, pi
import matplotlib.pyplot as plt
from params import currentDS


# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––
#       Klasse CurbelSwing zur Berechnung der
#       Lagekoordinaten eines Datensatzes
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––

# LAGEKOORINATEN DER GELENKE
class CurbelSwing:
    # TODO: Comments
    def __init__(self, Dataset, origin=None):
        self.l0, self.l1, self.l2, self.l3, self.a, self.b, self.ms, self.Js, self.omega = Dataset
        self.origin = np.array(origin) if origin is not None else np.array([0., 0.])

    # GELENK A = ORIGIN
    # die Koordinaten des Gelenks A sind fest durch origin bestimmt und verändern sich nicht durch phi oder psi
    # damit mit den anderen Genlenk-Koordinaten gut weiter gerechnent werden kann, wird die länge des phi-arrays
    # verwendet, um eine matrix mit der selben länge zu erzeugen
    # der return-Wert hat die shape (2, len(phi)) und ist somit gilt  xA, yA = A
    def A(self, phi):
        if np.iterable(phi):
            return self.origin.repeat(len(phi)).reshape((2, len(phi)))
        return self.origin

    # GELENK D
    # genau wie A, bleibt D über verschieden Winkel konsant, trotzdem kann man mit phi die Länge
    # des return-Wertes steuern, er unterscheidet sich zu D legidlich um l0 in der x-Koordinate
    # der return-Wert hat die shape (2, len(phi)) und ist somit gilt  xD, yD = D
    def D(self, phi):
        if np.iterable(phi):
            return self.A(phi) + np.array([self.l0, 0]).repeat(len(phi)).reshape((2, len(phi)))
        return self.origin + np.array([self.l0, 0])

    # GELENK B
    # B schwingt mit einem Hebel der Länge l1 und Winkel phi um A(origin) herum, psi ist irrelevant
    # B = A + Vektor(l1)
    # der return-Wert hat die shape (2, len(phi)) und ist somit gilt  xC, yC = C
    def B(self, phi):
        return self.A(phi) + self.l1 * np.array([cos(phi), sin(phi)])

    # GELENK C
    # C schwingt mit einem Hebel der Länge l2 und Winkel psi um B herum oder alternativ
    # mit der Länge l3 um D, bei richtigen phi und psi Päärchen ist das das Gleiche
    # sowohl phi als auch psi müssen betrachtet werdnen
    # C = B + Vektor(l2) ( oder C = D + Vektor(l3) )
    # der return-Wert hat die shape (2, len(phi)) und ist somit gilt  xC, yC = C
    def C(self, phi, psi):
        return self.B(phi) + self.l2 * np.array([sin(psi), -cos(psi)])

    # SPTIZE DES KÖRPERS P
    # P ist die Schpitze des Körpers der Kurbelschwinge, dieser ist ein Dreick aus P, B und C
    # seine relative positon wird durch a und b eingestellt, sowohl phi als auch psi müssen betrachtet werdnen
    # P = B + Vektor(a) + Vektor(b)
    # der return-Wert hat die shape (2, len(phi)) und ist somit gilt  xP, yP = P
    def P(self, phi, psi):
        return self.B(phi) + self.a * np.array([sin(psi), -cos(psi)]) + self.b * np.array([cos(psi), sin(psi)])

    # SCHWERPUNKT DES KÖRPERS S
    # S ist der Schwerpunkt des Körpers der Kurbelschwinge, dieser ist ein Dreick aus P, B und C
    # seine relative positon wird durch a und b/2 eingestellt, sowohl phi als auch psi müssen betrachtet werdnen
    # S = B + Vektor(a) + Vektor(b)/2  oder S = P - Vektor(b)/2
    # der return-Wert hat die shape (2, len(phi)) und ist somit gilt  xS, yS = S
    def S(self, phi, psi):
        return self.P(phi, psi) - self.b / 2 * np.array([cos(psi), sin(psi)])

    # KOORDINATEN DER KINEMATISCHEN KETTE
    # fügt die punkte A, B, P, C und D in eine Matrix und gibt dies zurück
    # der Rückgabe wert lässt sich in die Koordinaten der einzelnen Gelenk auf teilen:
    # A, B, P, C, D = coords    und diese wiederum in x und y
    # der return-Wert hat die shape (5, 2, len(phi))
    def coords(self, phi, psi):
        return np.array([self.A(phi), self.B(phi), self.P(phi, psi), self.C(phi, psi), self.D(phi)])

    # KOORDINATEN DER KINEMATISCHEN KETTE plus strecke BC
    # der return-Wert hat die shape (5, 2, len(phi))
    def coordsPlusBC(self, phi, psi):
        return np.array([self.A(phi), self.B(phi), self.P(phi, psi),
                        self.C(phi, psi), self.D(phi), self.C(phi, psi), self.B(phi)])

    # PLOTTING
    # fügt die kinematische Kette in den aktuallen plot ein
    # Achtung: funktioniert nicht für Arrays von phi/psi, verwende dafür die animation in cubelplots
    def plot(self, phi, psi):
        #TODO: Plot könnte schöner sein.
        x, y = self.coords(phi, psi).T
        plt.plot(x, y)

    # ERSTE ABLEITUNG VON S
    # zur Berechnung der Trägheiten und Zusammenhang des Körpers BPC zu phi, sind die 1. und 2. Ableitung benötigt
    # die Herleitung erfolgte analytisch und benötigt phi, phi', psi und psi' als input
    # der return-Wert hat die shape (2, len(phi)) und ist somit gilt  xS', yS' = S'
    def S_(self, phi, phi_, psi, psi_):
        return np.array([
            -self.l1 * sin(phi) * phi_ + self.a * cos(psi) * psi_ - self.b / 2 * sin(psi) * psi_,  # xS'
            self.l1 * cos(phi) * phi_ + self.a * sin(psi) * psi_ + self.b / 2 * cos(psi) * psi_  # yS'
        ])

    # ZWEITE ABLEITUNG VON S
    # zur Berechnung der Trägheiten und Zusammenhang des Körpers BPC zu phi, sind die 1. und 2. Ableitung benötigt
    # die Herleitung erfolgte analytisch und benötigt phi, phi', phi'', psi, psi' und psi' als input
    # der return-Wert hat die shape (2, len(phi)) und ist somit gilt  xS', yS' = S'
    def S__(self, phi, phi_, phi__, psi, psi_, psi__):
        sPhi__, sPhi_2 = sin(phi) * phi__, sin(phi) * phi_ ** 2
        cPhi__, cPhi_2 = cos(phi) * phi__, cos(phi) * phi_ ** 2
        sPsi__, sPsi_2 = sin(psi) * psi__, sin(psi) * psi_ ** 2
        cPsi__, cPsi_2 = cos(psi) * psi__, cos(psi) * psi_ ** 2
        return np.array([
            -self.l1 * (sPhi__ + cPhi_2) + self.a * (cPsi__ - sPsi_2) - self.b / 2 * (sPsi__ + cPsi_2),  # xS''
            self.l1 * (cPhi__ - sPhi_2) + self.a * (sPsi__ + cPsi_2) + self.b / 2 * (cPsi__ - sPsi_2),  # yS''
        ])
