from PIL import Image
import numpy as np
# import matplotlib.pyplot as plt

heightmap = Image.open("gc_dem.tif")

heightmap = np.array(heightmap, dtype = np.float)

heightmap = heightmap[2000:3000:2,1000:2000:2] / 10000

out = open("terrain.obj", "w")

out.write("""####
#
# OBJ File Generated by Trainwrexk
#
####
# Object terrain.obj
#
# Vertices: 250000
# Faces: """ + str(499 * 499 * 2) + """
#
####
""")
x = np.linspace(-.1, .1, 500)
y = np.linspace(-.1, .1, 500)
x, y = np.meshgrid(x, y)

def getVector(i, j):
    return np.array([x[i, j], y[i, j], heightmap[i, j]])


normalsx = np.zeros((500, 500))
normalsy = np.zeros((500, 500))
normalsz = np.zeros((500, 500)) + 1

for i in range(1, 499):
    for j in range(1, 499):
        normal = np.cross(getVector(i+1, j) - getVector(i-1, j),
                          getVector(i, j+1) - getVector(i, j-1))
        normal = -normal / np.sqrt(np.dot(normal, normal))
        normalsx[i, j] = normal[0]
        normalsy[i, j] = normal[1]
        normalsz[i, j] = normal[2]

for i in range(500):
    for j in range(500):
        out.write("vn " + str(normalsx[i, j]) + " " + 
                          str(normalsz[i, j]) + " " + 
                          str(normalsy[i, j]) + "\n")
        out.write("v " + str(x[i, j]) + " " + 
                          str(heightmap[i, j]) + " " + 
                          str(y[i, j]) + "\n")
out.write("#250000 magic\n \n")
def vecwrite(i, j):
    r = 500 * i + j + 1
    out.write(" " + str(r) + "//" + str(r))
for i in range(499):
    for j in range(499):
        out.write("f")
        
        vecwrite(i, j)
        vecwrite(i+1, j)
        vecwrite(i, j+1)
        
        out.write("\nf")
        vecwrite(i+1, j)
        vecwrite(i+1, j+1)
        vecwrite(i, j+1)
        out.write("\n")
                          


