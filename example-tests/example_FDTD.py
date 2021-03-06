import pyHiChi as pfc
import numpy as np
import math as ma

def valueEx(x, y, z):
	Ex = 0
	return Ex
def valueEy(x, y, z):
	Ey = np.cos(z + ma.pi/6)
	return Ey
def valueEz(x, y, z):
	Ez = 0
	return Ez

def valueBx(x, y, z):
	Bx = -np.cos(z+ma.pi/6)
	return Bx
def valueBy(x, y, z):
	By = 0
	return By
def valueBz(x, y, z):
	Bz = 0
	return Bz

def step(minCoords, maxCoords, gridSize):
	steps = pfc.vector3d(1, 1, 1)
	steps.x = (maxCoords.x - minCoords.x)/(gridSize.x)
	steps.y = (maxCoords.y - minCoords.y)/(gridSize.y)
	steps.z = (maxCoords.z - minCoords.z)/(gridSize.z)
	return steps

gridSize = pfc.vector3d(5, 10, 11)
minCoords = pfc.vector3d(0.0, 1.0, 0.0)
maxCoords = pfc.vector3d(3.5, 7.0, 2*ma.pi)
stepsGrid = step(minCoords, maxCoords, gridSize)
timeStep = 1e-16

grid = pfc.YeeGrid(gridSize, timeStep, minCoords, stepsGrid)
grid.setE(valueEx, valueEy, valueEz)
grid.setB(valueBx, valueBy, valueBz)


fieldSolver = pfc.FDTD(grid)

#show
import matplotlib.pyplot as plt
import matplotlib.animation as animation

N = 37
x = np.arange(0, 3.5, 3.5/N)
z = np.arange(0, 2*ma.pi, 2*ma.pi/N)


def getFields():
	global grid, x, z, N
	Ex = np.zeros(shape=(N,N))
	Ey = np.zeros(shape=(N,N))
	Ez = np.zeros(shape=(N,N))
	Bx = np.zeros(shape=(N,N))
	By = np.zeros(shape=(N,N))
	Bz = np.zeros(shape=(N,N))
	for ix in range(N):
		for iy in range(N):
			coordXZ = pfc.vector3d(x[ix], 0.0, z[iy])
			E = grid.getE(coordXZ)
			Ex[ix, iy] = E.x
			Ey[ix, iy] = E.y
			Ez[ix, iy] = E.z
			B = grid.getB(coordXZ)
			Bx[ix, iy] = B.x
			By[ix, iy] = B.y
			Bz[ix, iy] = B.z
	return Ex, Ey, Ez, Bx, By, Bz

def updateData():
	for i in range(10000):
		fieldSolver.updateFields()
	

(Ex, Ey, Ez, Bx, By, Bz) = getFields()

fig, axes = plt.subplots(ncols=3, nrows=2)

im11 = axes[0, 0].imshow(Ex, cmap='RdBu', interpolation='none', extent=(0, 2*ma.pi, 0, 3.5), animated = True)
fig.colorbar(im11, ax=axes[0, 0])

im12 = axes[0, 1].imshow(Ey, cmap='RdBu', interpolation='none', extent=(0, 2*ma.pi, 0, 3.5), animated = True)
fig.colorbar(im12, ax=axes[0, 1])

im13 = axes[0, 2].imshow(Ez, cmap='RdBu', interpolation='none', extent=(0, 2*ma.pi, 0, 3.5), animated = True)
fig.colorbar(im13, ax=axes[0, 2])

im21 = axes[1, 0].imshow(Bx, cmap='RdBu', interpolation='none', extent=(0, 2*ma.pi, 0, 3.5), animated = True)
fig.colorbar(im21, ax=axes[1, 0])

im22 = axes[1, 1].imshow(By, cmap='RdBu', interpolation='none', extent=(0, 2*ma.pi, 0, 3.5), animated = True)
fig.colorbar(im22, ax=axes[1, 1])

im23 = axes[1, 2].imshow(Bz, cmap='RdBu', interpolation='none', extent=(0, 2*ma.pi, 0, 3.5), animated = True)
fig.colorbar(im23, ax=axes[1, 2])


def updatefig(*args):
	updateData()
	(Ex, Ey, Ez, Bx, By, Bz) = getFields()
	im11.set_array(Ex)
	im12.set_array(Ey)
	im13.set_array(Ez)
	im21.set_array(Bx)
	im22.set_array(By)
	im23.set_array(Bz)
	return im11, im12, im13, im21, im22, im23, 
	
ani = animation.FuncAnimation(fig, updatefig, interval=50, blit=True)

plt.show()


