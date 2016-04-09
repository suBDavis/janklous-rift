import OpenGL.GL as GL
import OpenGL.GLUT as GLUT
import OpenGL.GLU as GLU

from threading import Thread

from OpenGL.arrays import vbo

import OpenGL.arrays as arrays

import sys

import numpy as np

import operator
import ctypes

import time
print "type y to use VBO, n to use immediate rendering"

def mulmat3(m):
   GL.glMultMatrixf([m[0, 0], m[1, 0], m[2, 0], 0, 
                   m[0, 1], m[1, 1], m[2, 1], 0, 
                   m[0, 2], m[1, 2], m[2, 2], 0, 
                   0,      0,          0,      1])

useVBO = True

position = [0.1, -27, -1.5]
 
orientation = np.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype = np.float)
 
def interpretLine(string):
    return map(float, string.split()[1:])
    
with open("/home/hastings/cpp/jankulous-rift/terrainmesh/terrain.obj", "r") as file:
    for _ in range(7):
        file.readline()

    numverts =  int(file.readline().split()[-1])
    numtris =  int(file.readline().split()[-1])
    
    file.readline()
    file.readline()

    verts = [[69, 69, 69]]
    norms = [[69, 69, 69]]
    tris = []

    for _ in range(numverts):
        norms += [interpretLine(file.readline())]
        verts += [interpretLine(file.readline())]
    file.readline()
    file.readline()
    for _ in range(numtris):
        tris += [[int(a.split("//")[0]) for a in file.readline().split()[1:]]]
        
        
        
GLUT.glutInit(sys.argv)

GLUT.glutInitWindowSize(1512,800)


GLUT.glutCreateWindow("BUNNY")


GLUT.glutInitDisplayMode(GLUT.GLUT_RGBA)


GL.glEnable(GL.GL_DEPTH_TEST)

GL.glEnable(GL.GL_LIGHTING)
GL.glEnable(GL.GL_LIGHT0)
GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, [1, 1, 1, 0])

GL.glLightfv(GL.GL_LIGHT0, GL.GL_AMBIENT, [.2, .2, .2, 1])

GL.glLightfv(GL.GL_LIGHT0, GL.GL_DIFFUSE, [1, 1, 1, 1])
GL.glEnable(GL.GL_NORMALIZE)


#GL.glEnable(GL.GL_CULL_FACE)
#GL.glCullFace(GL.GL_BACK)



vertsa = np.array(verts, dtype=np.float32)
trisa = np.array(tris, dtype = np.int32).flatten()
vertexVBO = vbo.VBO(vertsa)

normsa = np.array(norms, dtype=np.float32)
normVBO = vbo.VBO(normsa)
triBuffer = vbo.VBO(trisa, target=GL.GL_ELEMENT_ARRAY_BUFFER)
angle = 0
def draw():
   global orientation
   GL.glEnable(GL.GL_DEPTH_TEST)
   GL.glDepthFunc(GL.GL_LEQUAL)

   GL.glMatrixMode(GL.GL_PROJECTION)
   GL.glLoadIdentity()
   
   #GLU.gluLookAt(position[0], position[1], position[2], 
   #              position[0]  , position[1], position[2]  -  1,
   #              0, 1, 0)
   GLU.gluLookAt(0,0,0,0,0,-  1,
                 0, 1, 0)
   GL.glFrustum(-.2, .2, -.1, .1, .1, 1000)
   GL.glViewport(0, 0, 1512, 800)
   
   GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
      

   
   
   GL.glMatrixMode(GL.GL_MODELVIEW)
   GL.glLoadIdentity()
   
   
   mulmat3(orientation)
   
   GL.glTranslatef(position[0], position[1], position[2])
   
   
   GL.glScalef(1000, 100, 1000)
   GL.glEnableClientState(GL.GL_VERTEX_ARRAY);
   vertexVBO.bind()
   # when GL_ARRAY_BUFFER is bound to vertex buffer
   triBuffer.bind()
   GL.glVertexPointer(3, GL.GL_FLOAT, 0, None);
   
   normVBO.bind()
   # when GL_ARRAY_BUFFER is bound to normal buffer
   GL.glEnableClientState(GL.GL_NORMAL_ARRAY);
   GL.glNormalPointer(GL.GL_FLOAT, 0, None);
   
   GL.glColor4f(1,0,1,1)
   if useVBO:
       GL.glDrawElements(GL.GL_TRIANGLES, numtris*3, GL.GL_UNSIGNED_INT, None)
   else:
       for tri in tris:
           GL.glColor3f(1, 1, 1)
           GL.glBegin(GL.GL_TRIANGLES)
           for vert in tri:
               norm = norms[vert]
               vert = verts[vert]
               GL.glNormal3f(norm[0], norm[1], norm[2])
               
               
               GL.glVertex3f(vert[0], vert[1], vert[2])
           GL.glEnd()
   
   
   GL.glFlush()
   
   
def mousemoved(x, y):
    
    global orientation
    print orientation
    if x != 500 or y != 500:
       xrot = (x-500.) / 1000
       yrot = (y - 500.) / 1000
       print "orientation: \n:"
       print orientation
       print xrot, yrot
       rotator = np.matrix([[np.cos(xrot), np.sin(xrot), 0],
                                 [-np.sin(xrot),np.cos(xrot), 0],
                                 [0,           0,             1]])
       rotator *= np.matrix([[1, 0, 0],
                            [0,np.cos(yrot), np.sin(yrot)],
                            [0,-np.sin(yrot),np.cos(yrot)]])
       print rotator
       orientation = rotator * orientation
       print "orientation: \n:"
       print orientation
       GLUT.glutWarpPointer(500, 500)

                            
GLUT.glutPassiveMotionFunc(mousemoved)
GLUT.glutDisplayFunc(draw)
print len(norms)

def update():
    t0 = time.time()
    go = np.array((orientation** -1) * np.matrix([[0], [0], [.05]])).flatten()
    print go
    position[0] += go[0] 
    position[1] += go[1]
    position[2] += go[2]
    draw()
    t1 = time.time()
    GLUT.glutSetWindowTitle(str(1 / (t1 - t0)))
GLUT.glutIdleFunc(update)
GLUT.glutMainLoop()

