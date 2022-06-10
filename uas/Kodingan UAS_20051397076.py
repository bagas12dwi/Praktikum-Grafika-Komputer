import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy

# settings
screen_height = 800
screen_width = 600
line_colour = (0, 0, 0)


class Pyramid:

    # sudut
    vertices = [
        [1, -1, -1],
        [1, -1, 1],
        [-1, -1, 1],
        [-1, -1, -1],
        [0, 1, 0]
    ]

    # tepian
    edges = (
        (0, 1),
        (0, 3),
        (0, 4),
        (1, 4),
        (1, 2),
        (2, 4),
        (2, 3),
        (3, 4)
    )

    # permukaan
    surfaces = (
        (1, 2, 4),
        (0, 1, 2, 3),
        (0, 1, 4),
        (2, 3, 4)
    )

# warna
    colors = (
        (255, 0, 0),
        (127, 102, 255),
        (255, 0, 0),  # warna merah
        (255, 102, 102),
        (255, 255, 51),
        (255, 153, 255),
        (0, 255, 0),
        (127, 102, 255),
        (255, 0, 0),  # warna merah
        (0, 255, 0),
        (255, 153, 153),
        (255, 153, 255))

    # initialisasi
    def __init__(self, scale=1):
        self.edges = Pyramid.edges
        self.vertices = list(numpy.multiply(
            numpy.array(Pyramid.vertices), scale))
        self.surfaces = Pyramid.surfaces

    # Menggambar pyramid
    def draw(self):
        self.fill_sides()
        glLineWidth(5)
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glColor3f(1, 1, 1)
                glVertex3fv(self.vertices[vertex])
        glEnd()

    # untuk pergerakan
    def move(self, x, y, z):
        self.vertices = list(map(lambda vertex: (
            vertex[0] + x, vertex[1] + y, vertex[2] + z), self.vertices))

    # mewarnai sisi sisi
    def fill_sides(self):
        glBegin(GL_QUADS)
        for surface in self.surfaces:
            x = 0
            for vertex in surface:
                x += 1
                glColor3fv(Pyramid.colors[x]),
                glVertex3fv(self.vertices[vertex])
        glEnd()


def main():
    pygame.init()
    display = (screen_height, screen_width)
    # seting pygame untuk 3d grafis
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50)

    # pergerakan untuk z rotasi
    glTranslatef(0, 0, -20)

    # menggambar pyramid untuk object yang solid
    glEnable(GL_DEPTH_TEST)

    # inisialisasi class pyramid
    p = Pyramid(2)

    velocity = 0.1

    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        # perputaran pyramid
        glRotatef(velocity * 10, 0, 1, 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Perputaran saat ditekan tombol di keyboard
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            p.move(-velocity, 0, 0)
        if keys[pygame.K_RIGHT]:
            p.move(velocity, 0, 0)
        if keys[pygame.K_UP]:
            p.move(0, velocity, 0)
        if keys[pygame.K_DOWN]:
            p.move(0, -velocity, 0)
        if keys[pygame.K_w]:
            p.move(0, 0, velocity)
        if keys[pygame.K_s]:
            p.move(0, 0, -velocity)
        if keys[pygame.K_a]:
            glRotatef(-velocity*10, 0, 1, 0)
        if keys[pygame.K_d]:
            glRotatef(velocity*10, 0, 1, 0)

        # untuk clear buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        p.draw()
        pygame.display.flip()


main()
