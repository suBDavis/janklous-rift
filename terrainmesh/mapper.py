from PIL import Image
import numpy as np
# import matplotlib.pyplot as plt

heightmap = Image.open("gc_dem.tif")

heightmap = np.array(heightmap, dtype = np.float)

heightmap = heightmap[1500:3500:2,500:2500:2] / 10000

out = open("terrain.obj", "w")
DIM = 1000
out.write("""####
#
# OBJ File Generated by Trainwrexk
#
####
# Object terrain.obj
#
# Vertices: 1000000
# Faces: """ + str((DIM - 1) * (DIM - 1) * 2) + """
#
####
""")

x = np.linspace(-.2, .2, DIM)
y = np.linspace(-.2, .2, DIM)
x, y = np.meshgrid(x, y)

def getVector(i, j):
    return np.array([x[i, j], y[i, j], heightmap[i, j]])


normalsx = np.zeros((DIM, DIM))
normalsy = np.zeros((DIM, DIM))
normalsz = np.zeros((DIM, DIM)) + 1

for i in range(1, DIM - 1):
    for j in range(1, DIM - 1):
        normal = np.cross(getVector(i+1, j) - getVector(i-1, j),
                          getVector(i, j+1) - getVector(i, j-1))
        normal = -normal / np.sqrt(np.dot(normal, normal))
        normalsx[i, j] = normal[0]
        normalsy[i, j] = normal[1]
        normalsz[i, j] = normal[2]

for i in range(DIM):
    for j in range(DIM):
        out.write("vn " + str(normalsx[i, j]) + " " + 
                          str(normalsz[i, j]) + " " + 
                          str(normalsy[i, j]) + "\n")
        out.write("v " + str(x[i, j]) + " " + 
                          str(heightmap[i, j]) + " " + 
                          str(y[i, j]) + "\n")
out.write("#250000 magic\n \n")
def vecwrite(i, j):
    r = DIM * i + j + 1
    out.write(" " + str(r) + "//" + str(r))
for i in range(DIM - 1):
    for j in range(DIM - 1):
        out.write("f")
        
        vecwrite(i, j)
        vecwrite(i+1, j)
        vecwrite(i, j+1)
        
        out.write("\nf")
        vecwrite(i+1, j)
        vecwrite(i+1, j+1)
        vecwrite(i, j+1)
        out.write("\n")
                          


