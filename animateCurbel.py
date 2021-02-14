from calcMotorMoment import *
from curbelswingDGL import simulate
from params import *
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––
#                ANIMATION DER KURBELSWINGE
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––


# Animiert die Kurbelswinge
# der übergebenen phi- und timeArrays werden mit matplotlib animiert
# TODO: Plot schöner machen, title und annotation ect.
def animateCurbel(phiArr, timeArr, DS=currentDS):
    frames = len(timeArr)
    millisPerFrame = timeArr[-1] / frames * 1e3

    psiArr = solveForPsi(phiArr)
    coords = CurbelSwing(DS).coordsPlusBC(phiArr,psiArr)

    fig = plt.figure(figsize=(15, 10))
    plt.style.use("ggplot")
    plt.xlim([np.min(coords[1,0,:]) - .5, np.max(coords[3,0,:]) + .5])
    plt.ylim([np.min(coords[1,1,:]) - .5, np.max(coords[2,1,:]) + .5])
    x0, y0 = coords[:,:,0].T
    swingPlot, = plt.plot(x0, y0, linewidth="5")

    def animate(i):
        xi, yi = coords[:,:,i].T
        swingPlot.set_data(xi, yi)

    ani = FuncAnimation(fig, animate, frames=frames, interval=millisPerFrame, repeat=False)
    plt.show()