import sys

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

vertices = [
    [1.0, 1.0, 1.0],
    [-1.0, -1.0, 1.0],
    [-1.0, 1.0, -1.0],
    [1.0, -1.0, -1.0],
]

faces = [
    (0, 1, 2),
    (0, 3, 1),
    (0, 2, 3),
    (1, 3, 2),
]

cores = [
    (0.90, 0.25, 0.25),
    (0.25, 0.75, 0.35),
    (0.25, 0.45, 0.90),
    (0.95, 0.80, 0.20),
]

angulo_rotacao_x = 0.0
angulo_rotacao_y = 0.0
angulo_rotacao_z = 0.0
eixo_rotacao = "y"
velocidade = 0.8
pausado = False


def desenhar_solido(vertices, faces, cores):
    glBegin(GL_TRIANGLES)
    for i, face in enumerate(faces):
        glColor3fv(cores[i % len(cores)])
        for indice in face:
            glVertex3fv(vertices[indice])
    glEnd()


def desenhar_arestas(vertices, faces):
    glColor3f(0.08, 0.08, 0.10)
    glLineWidth(2.0)
    for face in faces:
        glBegin(GL_LINE_LOOP)
        for indice in face:
            glVertex3fv(vertices[indice])
        glEnd()


def escrever_texto(x, y, z, texto):
    glRasterPos3f(x, y, z)
    for caractere in texto:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(caractere))


def desenhar_eixos():
    glLineWidth(1.5)
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-2.2, 0.0, 0.0)
    glVertex3f(2.2, 0.0, 0.0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -2.2, 0.0)
    glVertex3f(0.0, 2.2, 0.0)
    glColor3f(0.0, 0.4, 1.0)
    glVertex3f(0.0, 0.0, -2.2)
    glVertex3f(0.0, 0.0, 2.2)
    glEnd()

    glColor3f(1.0, 0.0, 0.0)
    escrever_texto(2.4, 0.0, 0.0, "X")
    glColor3f(0.0, 1.0, 0.0)
    escrever_texto(0.0, 2.4, 0.0, "Y")
    glColor3f(0.0, 0.4, 1.0)
    escrever_texto(0.0, 0.0, 2.4, "Z")


def desenhar():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(3.5, 2.8, 5.5, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    desenhar_eixos()

    glPushMatrix()
    glRotatef(angulo_rotacao_x, 1.0, 0.0, 0.0)
    glRotatef(angulo_rotacao_y, 0.0, 1.0, 0.0)
    glRotatef(angulo_rotacao_z, 0.0, 0.0, 1.0)
    desenhar_solido(vertices, faces, cores)
    desenhar_arestas(vertices, faces)
    glPopMatrix()

    glutSwapBuffers()


def animar(valor):
    global angulo_rotacao_x, angulo_rotacao_y, angulo_rotacao_z

    if not pausado:
        if eixo_rotacao in ("x", "todos"):
            angulo_rotacao_x = (angulo_rotacao_x + velocidade) % 360.0
        if eixo_rotacao in ("y", "todos"):
            angulo_rotacao_y = (angulo_rotacao_y + velocidade) % 360.0
        if eixo_rotacao in ("z", "todos"):
            angulo_rotacao_z = (angulo_rotacao_z + velocidade) % 360.0

    glutPostRedisplay()
    glutTimerFunc(16, animar, 0)


def teclado(tecla, x, y):
    global eixo_rotacao, velocidade, pausado
    global angulo_rotacao_x, angulo_rotacao_y, angulo_rotacao_z

    tecla = tecla.decode("utf-8").lower()

    if tecla == "x":
        eixo_rotacao = "x"
    elif tecla == "y":
        eixo_rotacao = "y"
    elif tecla == "z":
        eixo_rotacao = "z"
    elif tecla == "a":
        eixo_rotacao = "todos"
    elif tecla == " ":
        pausado = not pausado
    elif tecla == "+":
        velocidade = min(velocidade + 0.2, 6.0)
    elif tecla == "-":
        velocidade = max(velocidade - 0.2, 0.0)
    elif tecla == "r":
        angulo_rotacao_x = 0.0
        angulo_rotacao_y = 0.0
        angulo_rotacao_z = 0.0
    elif tecla == "\x1b" or tecla == "q":
        sys.exit(0)


def redimensionar(largura, altura):
    if altura == 0:
        altura = 1
    glViewport(0, 0, largura, altura)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, largura / altura, 1.0, 50.0)
    glMatrixMode(GL_MODELVIEW)


def inicializar():
    glClearColor(0.95, 0.95, 0.95, 1.0)
    glEnable(GL_DEPTH_TEST)
    glDisable(GL_CULL_FACE)


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Tetraedro - Solidos de Platao")

    inicializar()

    glutDisplayFunc(desenhar)
    glutReshapeFunc(redimensionar)
    glutKeyboardFunc(teclado)
    glutTimerFunc(16, animar, 0)

    glutMainLoop()


if __name__ == "__main__":
    main()
