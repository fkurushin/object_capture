import pygame
from pygame.locals import *
import math
from OpenGL.GL import *
from OpenGL.GLU import *

colors_red = (
    (1, 0, 0),
    (1, 0, 0),
    (1, 0, 0),
    (1, 0, 0),
    (1, 0, 0),
    (1, 0, 0),
    (1, 0, 0),
    (1, 0, 0),
    (1, 0, 0),
    (1, 0, 0),
    (1, 0, 0),
    (1, 0, 0),
)

colors_green = (
    (0, 1, 0),
    (0, 1, 0),
    (0, 1, 0),
    (0, 1, 0),
    (0, 1, 0),
    (0, 1, 0),
    (0, 1, 0),
    (0, 1, 0),
    (0, 1, 0),
    (0, 1, 0),
    (0, 1, 0),
    (0, 1, 0),
)

verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
)

surfaces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)


def Cube(e, v, s, c):
    for i in range(len(s)):
        glBegin(GL_QUADS)
        x = 0
        for vertex in s[i]:
            x += 1
            glColor3fv(c[x])
            glVertex3fv(v[vertex])
        glEnd()

        glBegin(GL_LINES)
        for edge in e:
            for vertex in edge:
                glVertex3fv(v[vertex])
        glEnd()

        # добавляем линии на грани куба
        glBegin(GL_LINES)
        glColor3fv((0, 0, 0))
        glVertex3fv(v[s[i][0]])
        glVertex3fv(v[s[i][1]])
        glVertex3fv(v[s[i][1]])
        glVertex3fv(v[s[i][2]])
        glVertex3fv(v[s[i][2]])
        glVertex3fv(v[s[i][3]])
        glVertex3fv(v[s[i][3]])
        glVertex3fv(v[s[i][0]])
        glEnd()


def main():
    pygame.init()
    display = (800, 800)
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    glTranslatef(-1, 0.0, -10)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # первый куб
        glPushMatrix()
        glTranslatef(-1, 0.0, -15)
        glTranslatef(2 * math.sin(pygame.time.get_ticks() / 1000 - math.pi / 2),
                     2 * math.cos(pygame.time.get_ticks() / 1000 + math.pi / 2), -5)
        glRotatef(pygame.time.get_ticks() / 1000 * 50, 0, 1, 0)
        Cube(edges, verticies, surfaces, colors_red)
        glPopMatrix()

        # второй куб
        glPushMatrix()
        # glTranslatef(2 * math.sin(pygame.time.get_ticks() / 1000), 2 * math.cos(pygame.time.get_ticks() / 1000), -10)
        # glTranslatef(2 * math.sin(pygame.time.get_ticks() / 1000), 2 * math.cos(pygame.time.get_ticks() / 1000), -20)
        glTranslatef(2 * math.sin(pygame.time.get_ticks() / 1000), 2 * math.cos(pygame.time.get_ticks() / 1000), -10)

        glRotatef(pygame.time.get_ticks() / 1000 * 100, 1, 1, 1)
        Cube(edges, verticies, surfaces, colors_green)
        glPopMatrix()

        # if pygame.time.get_ticks() % 100 == 0:
        #     pygame.time.wait(50)  # добавляем задержку в 50 миллисекунд
        # pygame.image.save(screen, f"/Users/fedorkurusin/Documents/HES/zhaba_project/frames"
        #                           f"/image_{pygame.time.get_ticks()}.png")

        size = screen.get_size()
        buffer = glReadPixels(0, 0, *size, GL_RGBA, GL_UNSIGNED_BYTE)
        pygame.display.flip()
        pygame.time.wait(10)

        screen_surf = pygame.image.fromstring(buffer, size, "RGBA")
        pygame.image.save(screen_surf, f"frames/image_{pygame.time.get_ticks()}.jpg")


if __name__ == "__main__":
    main()