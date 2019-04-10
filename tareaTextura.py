'''
Antonio Reyes
carnet> 17273
5/2/2019
Graficas por Computadora
materiales

'''

import struct
import collections
import time
import random
import math
import copy

def char(c):
    return struct.pack("=c", c.encode('ascii'))


def word(c):
    return struct.pack("=h", c)


def dword(c):
    return struct.pack("=l", c)


def color(r, g, b):
    try:
        return bytes([b, g, r])

    except:
        return bytes([255,0,0])

#listas para guardar los valores de los vertices
V2 = collections.namedtuple("Vertex2", ["x", "y"])
V3 = collections.namedtuple("Vertex3", ["x", "y", "z"])

class Texture(object):
    def __init__(self, filename):
        self.path = filename
        self.read()

    def read(self):
        img = open(self.path, "rb")
        img.seek(2 + 4 + 4)
        header_size = struct.unpack("=l", img.read(4))[0]
        img.seek(2 + 4 + 4 + 4 + 4)
        self.width = struct.unpack("=l", img.read(4))[0]
        self.height = struct.unpack("=l", img.read(4))[0]
        self.pixels = []
        img.seek(header_size)

        for y in range(self.height):
            self.pixels.append([])
            for x in range(self.width):
                b = ord(img.read(1))
                g = ord(img.read(1))
                r = ord(img.read(1))
                self.pixels[y].append(color(r,g,b))

        img.close()

    def get_color(self, tx, ty, intensity):
        x = int(tx * self.width) -1
        y = int(ty * self.height) -1
        #print(x)
        #print(y)
        return bytes (
            map(
            lambda b : round(b * intensity) 
            if b * intensity > 0 else 0, 
            self.pixels[y][x] 
            )
        )



class Bitmap(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.framebuffer = []


    '''
    Colorear toda la pantalla de un color, establecido con glClearcolor
    El color eleido se establece por medio del valor de red, green y blue.
    '''
    

    def glClear(self):
        self.framebuffer = [
            [color(r.red, r.green, r.blue) for x in range(self.width)]
            for y in range(self.height)
        ]

        self.zbuffer = [
            [-float('inf') for x in range(self.width)]
            for y in range(self.height)
        ]

    def tipoColor(self, x, y):
        return self.framebuffer[y][x]
        

    '''
    Elegir cual es el color que va a utilizar glClear para colorear la imagen.
    Establece el valor de red, green
    '''

    def glClearColor(self, r, g, b):
        red = int(255 * r)
        green = int(255 * g)
        blue = int(255 * b)

        self.red = red
        self.green = green
        self.blue = blue

    def write(self, filename):
        f = open(filename, 'bw')

        # file header
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        # image header
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width + self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        for x in range(self.height):
            for y in range(self.width):
                f.write(self.framebuffer[x][y])

        f.close()

    '''
    point agrega un punto de un color especifico en el lugar deseado
    '''

    def point(self, x, y, color):
        self.framebuffer[y][x] = color

    '''
    Funcion que modifica el color del punto que se genera en glVertex
    '''

    def glColor(self, r, g, b):
        
        redVertex = int(255 * r)
        greenVertex = int(255 * g)
        blueVertex = int(255 * b)
        
        """
        redVertex = int(r)
        greenVertex = int(g)
        blueVertex = int(b)
        """

        self.redVertex = redVertex
        self.greenVertex = greenVertex
        self.blueVertex = blueVertex

    def glViewPort(self, viewportX, viewportY, viewportWidth, viewportHeight):
        self.viewportX = viewportX
        self.viewportY = viewportY
        self.viewportWidth = viewportWidth
        self.viewportHeight = viewportHeight
        self.glClear()

    def glVertex(self):
        
        #Se establcece el centro del viewport

        centroX = r.viewportX + (int(r.viewportWidth / 2))
        centroY = r.viewportY + (int(r.viewportHeight / 2))

        self.centroX = centroX
        self.centroY = centroY

        arrayX = []
        self.arrayX = arrayX

        arrayY = []
        self.arrayY = arrayY

        arrayLlenar = []
        self.arrayLlenar = arrayLlenar


    def borrarArray(self):
        self.arrayLlenar = []
        self.arrayX = []
        self.arrayY = []

    def glLine(self, x0, y0, x1, y1):
        '''
        Se establece la posición de los puntos en el viewport en base al centro establecido en 
        glVertex
        '''
        #x0 = round(r.centroX + ((r.viewportWidth / 2) * x0))
        #y0 = round(r.centroY + ((r.viewportHeight / 2) * y0))
        #x1 = round(r.centroX + ((r.viewportWidth / 2) * x1))
        #y1 = round(r.centroY + ((r.viewportHeight / 2) * y1))

        r.arrayX.append(x0)
        r.arrayY.append(y0)

        #diferencia entre los valores de "x" y "y"
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        #steep va a definir si se ingresa los puntos sucesivos en "x" o en "y"
        #esto sera defnido por la pendiente que se define entre los puntos.
        steep = dy > dx

        if steep:
            x0,y0 = y0,x0
            x1,y1 = y1,x1

        if x0 > x1:
            x0,x1 = x1,x0
            y0,y1 = y1,y0
        
        dy = abs(y1-y0)
        dx = abs(x1 - x0)

        offset = 0 * 2 * dx
        threshold = 0.5 * 2 * dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                try:
                    r.point(int(y), int(x), color(r.redVertex, r.greenVertex, r.blueVertex))
                except:
                    pass

            else:
                try:
                    r.point(int(x), int(y), color(r.redVertex, r.greenVertex, r.blueVertex))

                except:
                    pass
            
            offset += dy

            #define el patron de pixeles consecutivos
            if offset >= threshold:
                y += 1 if y0 < y1 else -1
                threshold += 1 * dx

    #los tres puntos del triangulo
    def triangle(self, A, B, C, vt0x, vt0y, vt1x, vt1y, vt2x, vt2y, intensidad):
        #print(A, B, C)
        bbox_min, bbox_max = bbox(A, B, C)
        for x in range(bbox_min.x, bbox_max.x + 1):
            for y in range(bbox_min.y, bbox_max.y + 1):

                w,v,u = barycentric(A, B, C, V2(x,y))

                if w < 0 or v < 0 or u < 0:
                    continue

                z = A.z * w + B.z * v + C.z * u

                try:
                    tx = float(vt0x) * w + float(vt1x) * v + float(vt2x) * u
                    ty = float(vt0y) * w + float(vt1y) * v + float(vt2y) * u
                    colores = t.get_color(tx, ty, intensidad)
                    #print(colores)
                    #print("==============")
                    r.glColor(*colores)

                except:
                    r.glColor(1,0,0)


                #Se verifica si se pinta el punto en caso su coordenada en z sea mayor a la anteriormente pintada en el mismo lugar
                if z > self.zbuffer[y][x]:
                    self.point(x,y,color(r.redVertex, r.greenVertex, r.blueVertex))
                    self.zbuffer[y][x] = z



def sumaVector(v0, v1):
    return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)

def multiEscalar(esc, v0):
    return V3(esc * v0.x, esc * v0.y, esc * v0.z)

def pPunto(v0, v1):
    return (v0.x * v1.x + v0.y * v1.y + v0.z * v1.z)

def cross(v0,v1):
    return V3( (v0.y * v1.z - v1.y * v0.z), (v0.z * v1.x - v1.z * v0.x), (v0.x * v1.y - v1.x * v0.y)      )

def restaVector(v0,v1):
    return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)


newmtl = []
mtlCOLOR = []
vertices = [["0", "0", "0", "0"]]
verticeT = [["0", "0", "0", "0"]]

def leerMTL(archivo):
    with open(archivo) as mtl:
        lines = mtl.read()

    arregloLineas = lines.split("\n")
    
    for x in arregloLineas:
        if x.startswith("newmtl"):
            a = x.split()
            if a[1] not in newmtl:
                newmtl.append(a[1])

        if x.startswith("Kd"):
            colorMTL = []
            a = x.split()
            colorMTL.append(a[1])
            colorMTL.append(a[2])
            colorMTL.append(a[3])
            if colorMTL not in mtlCOLOR:
                mtlCOLOR.append(colorMTL)

def dataObj(archivo):
    with open(archivo) as a:
        lines = a.read()

    arregloLineas = lines.split("\n")
    
    for x in arregloLineas:

        if x.startswith("v "):
            nuevoVertice = []
            a = x.split()

            contador = 1

            while contador < 4:
                nuevoVertice.append(a[contador])
                contador += 1

            vertices.append(nuevoVertice)   

        if x.startswith("vt "):
            nuevoVT = []
            a = x.split()
            contador = 1
            while contador < 3:
                nuevoVT.append(a[contador])
                contador += 1

            #print(nuevoVT)
            verticeT.append(nuevoVT)


    for x in arregloLineas:
        

        if x.startswith("f "):
            serieCaras1 = []
            serieVT = []
            serieCaras3 = []
            a = x.split(" ")
            del a[0]

            for i in a:
                q = i.split("/")
                serieCaras1.append(q[0])
                serieVT.append(q[1])
                serieCaras3.append(q[2])

            #print (serieCaras1)
            #print (serieVT)
            #print (serieCaras3)    
            #print("************************")
            
            
            #print(serieCaras)
            x0 = float(vertices[int(serieCaras1[0])][0])
            y0 = float(vertices[int(serieCaras1[0])][1])
            z0 = float(vertices[int(serieCaras1[0])][2])

            x1 = float(vertices[int(serieCaras1[1])][0])
            y1 = float(vertices[int(serieCaras1[1])][1])
            z1 = float(vertices[int(serieCaras1[1])][2])

            x2 = float(vertices[int(serieCaras1[2])][0])
            y2 = float(vertices[int(serieCaras1[2])][1])
            z2 = float(vertices[int(serieCaras1[2])][2])

            x0 = round(r.centroX + ((r.viewportWidth / 2) * x0))
            y0 = round(r.centroY + ((r.viewportHeight / 2) * y0))
            x1 = round(r.centroX + ((r.viewportWidth / 2) * x1))
            y1 = round(r.centroY + ((r.viewportHeight / 2) * y1))
            x2 = round(r.centroX + ((r.viewportWidth / 2) * x2))
            y2 = round(r.centroY + ((r.viewportHeight / 2) * y2))
        
            z0 = round(r.centroX + ((r.viewportWidth / 2) * z0))
            z1 = round(r.centroX + ((r.viewportWidth / 2) * z1))
            z2 = round(r.centroX + ((r.viewportWidth / 2) * z2))

            luz = V3(0.1,0.2,0.6)
            ba = restaVector(V3(x1, y1, z1), V3(x0, y0, z0))
            ca = restaVector(V3(x2, y2, z2), V3(x0, y0, z0))

            cruz = cross( V3(ba.x, ba.y, ba.z), V3(ca.x, ca.y, ca.z))

            normal = (math.sqrt(cruz.x**2 + cruz.y**2 + cruz.z**2))

            try:
                nuevoVector = V3((cruz.x / normal), (cruz.y/normal), (cruz.z/normal))
            except:
                nuevoVector = V3(1,1,1)

            intensidad = pPunto(nuevoVector, luz)
            if intensidad > 1:
                intensidad = 1

            if intensidad < 0:
                intensidad = 0

            #a = copy.deepcopy(rojo)
            #g = copy.deepcopy(verde)
            #b = copy.deepcopy(azul)


            #red = round(a * intensidad)
            #green = round(g * intensidad)
            #blue = round(b * intensidad)

            

            vt0x = verticeT[int(serieVT[0])][0]
            vt0y = verticeT[int(serieVT[0])][1]

            vt1x = verticeT[int(serieVT[1])][0]
            vt1y = verticeT[int(serieVT[1])][1]

            vt2x = verticeT[int(serieVT[2])][0]
            vt2y = verticeT[int(serieVT[2])][1]
            #print(vt0x, vt0y)
            #print(vt1x, vt1y)
            #print(vt2x, vt2y)

            r.triangle(V3(x0,y0,z0), V3(x1,y1,z1), V3(x2,y2,z2), vt0x, vt0y, vt1x, vt1y, vt2x, vt2y, intensidad)
        
            

#A son las dos coordenadas de punto 1 de trinagulo
def bbox(A, B, C):
    xs = sorted([A.x, B.x, C.x])
    ys = sorted([A.y, B.y, C.y])

    return V2(xs[0], ys[0]), V2(xs[2], ys[2])


def barycentric(A, B, C, Punto):
    cx, cy, cz = cross(

        V3(B.x - A.x, C.x - A.x, A.x - Punto.x),
        
        V3(B.y - A.y, C.y - A.y, A.y - Punto.y)
    )

    #cz no puede ser < 1
    if cz == 0:
        return -1, -1, -1
        
    u = cx/cz
    v = cy/cz
    w = 1 - (u + v)
    return w, v, u


t = Texture("rojo.bmp")
r = Bitmap(600, 400)
r.glClearColor(0, 0, 0)
r.glClear()
r.glColor(1, 1, 1)
r.glViewPort(0, 0, 600, 400)
r.glVertex()


#leerMTL("porygonTextura.mtl")
dataObj("porygonTextura.obj")


r.write("sr5.bmp")
