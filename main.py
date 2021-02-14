from animateCurbel import animateCurbel
from curbelswingDGL import simulate


phiArr, phi_Arr, timeArr = simulate(stopTime=5)
animateCurbel(phiArr, timeArr)