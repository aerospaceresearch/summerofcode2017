import math
import numpy as np
import random
import matplotlib.pylab as plt
import time
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D

# physical constants
mu = 398600.0

def orbit(true_anomaly):
    eccentricity = 0.90
    semimajoraxis = 6371 + 100 # km
    if eccentricity < 1.0:
        h = (semimajoraxis * mu * (1.0 -eccentricity**2))**0.5
    else:
        h = (semimajoraxis * mu * (eccentricity**2 - 1))**0.5

    #print(h)

    inclination = 40 * math.pi / 180.0
    raan = 0 * math.pi / 180.0
    argument_of_periapsis = 0 * math.pi / 180.0
    #true_anomaly = 30 * math.pi / 180.0

    r = np.array([0.0,0.0,0.0])
    r[0] = h**2 / mu * 1.0 / (1.0 + eccentricity * math.cos(true_anomaly)) * math.cos(true_anomaly)
    r[1] = h**2 / mu * 1.0 / (1.0 + eccentricity * math.cos(true_anomaly)) * math.sin(true_anomaly)

    #print(r)

    v = np.array([0,0,0])
    v[0] = mu/h * -math.sin(true_anomaly)
    v[1] = mu/h * (eccentricity + math.cos(true_anomaly))

    #print(v)

    A1 = np.array([[math.cos(argument_of_periapsis), math.sin(argument_of_periapsis), 0],
      [-math.sin(argument_of_periapsis), math.cos(argument_of_periapsis), 0],
      [0, 0, 1]])

    A2 = np.array([[1, 0, 0],
      [0, math.cos(inclination), math.sin(inclination)],
      [0, -math.sin(inclination), math.cos(inclination)]])

    A3 = np.array([[math.cos(raan), math.sin(raan), 0],
      [-math.sin(raan), math.cos(raan), 0],
      [0, 0, 1]])

    A = np.mat(A1) * np.mat(A2) * np.mat(A3)

    R = np.matmul(A.T, r)
    V = (np.matmul(A.T, v))

    #print("ttt", R[0,0], R[0,1], R[0,2])
    return R


if __name__ == '__main__':
    # this crappy code shell help to generate typical orbits via the Keplerian orbit parameters.
    # jitter can be added with random numbers the user specifies.
    # this is just the first step, because this is in earth centered coordinates. next steps will include
    # earth rotations

    # play here and see, how it will jitter!
    random_range_low = -100.0
    random_range_high = 100.0

    x = []
    y = []
    z = []
    xdif = []
    ydif = []
    zdif = []


    file = open("track" + str(int(time.time())) + ".csv", "w")
    file.write("i\tx\ty\tz\tx+dif\ty+dif\tz+dif\txdif\tydif\tzdif\n")
    for i in range(0, 360):
        true_anomaly = 1.0*i * math.pi / 180.0
        R = orbit(true_anomaly)

        x_dif = random.uniform(random_range_low, random_range_high)
        y_dif = random.uniform(random_range_low, random_range_high)
        z_dif = random.uniform(random_range_low, random_range_high)

        transfer = str(i) + "\t"
        transfer += str(R[0,0]) + "\t"
        transfer += str(R[0,1]) + "\t"
        transfer += str(R[0,2]) + "\t"
        transfer += str(R[0,0] + x_dif) + "\t"
        transfer += str(R[0,1] + y_dif) + "\t"
        transfer += str(R[0,2] + z_dif) + "\t"
        transfer += str(x_dif) + "\t"
        transfer += str(y_dif) + "\t"
        transfer += str(z_dif) + "\n"
        file.write(transfer)

        x.append(R[0,0])
        y.append(R[0,1])
        z.append(R[0,2])
        xdif.append(R[0,0] + x_dif)
        ydif.append(R[0,1] + y_dif)
        zdif.append(R[0,2] + z_dif)
    file.close()

    # plane projecttion
    plt.plot(xdif, ydif, "*")
    plt.plot(0, 0, "o")
    plt.plot(x, y)
    plt.grid()
    plt.show()

    # 3d graph
    mpl.rcParams['legend.fontsize'] = 10

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot(xdif, ydif, zdif, "*", label='orbit jittery')
    ax.plot([0.0], [0.0], [0.0], "o", label='center')
    ax.plot(x, y, z, label='orbit original')
    ax.legend()

    plt.show()
