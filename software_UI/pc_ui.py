import sys, time
import numpy as np
import pygame as pg
import OpenGL.GL as gl
from OpenGL.GL import shaders

vertex_code = """
#version 460
layout(location=0) in vec4 position;
void main() {
    gl_Position = position;
}
"""

frag_code = """
#version 460
layout(location=0) out vec4 color;
uniform vec4 u_color;
void main() {
    color = u_color;
}
"""

def main():
    # create opengl context with pygame
    pg.init()
    clock = pg.time.Clock()
    size = (1000, 500)
    pg.display.set_mode(size, pg.OPENGL | pg.DOUBLEBUF, vsync=1)
    pg.display.set_caption("Waveform Display")
    #print(gl.glGetString(gl.GL_VERSION))

    vertex_shader = shaders.compileShader(vertex_code, gl.GL_VERTEX_SHADER)
    frag_shader = shaders.compileShader(frag_code, gl.GL_FRAGMENT_SHADER)
    shader = shaders.compileProgram(vertex_shader, frag_shader)

    # bind shader
    gl.glUseProgram(shader)
    # retrieve location of "u_color"
    location = gl.glGetUniformLocation(shader, "u_color")
    gl.glUniform4f(location, 0.890, 0.149, 0.752, 1.0)

    try:
        while True:
            clock.tick()
            # white backgroud
            gl.glClearColor(1.0, 1.0, 1.0, 1.0)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            scale, PI = 2, np.pi
            x = np.linspace(-1,1,1000).astype('float32')
            # random noise
            noise = 0.01 * np.random.uniform(-1,1,1000).astype('float32')
            # sine wave + noise(optional)
            y = (1.0/scale) * np.sin(6 * PI * x) #+ noise
            trace = np.vstack((x,y)).T

            vbo = gl.glGenBuffers(1)
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
            gl.glBufferData(gl.GL_ARRAY_BUFFER, trace, gl.GL_STATIC_DRAW)

            gl.glEnableVertexAttribArray(0)
            gl.glVertexAttribPointer(0, 2, gl.GL_FLOAT, gl.GL_FALSE, 0, None)

            gl.glDrawArrays(gl.GL_LINE_STRIP, 0 ,1000)
            #pg.display.set_caption("FPS: {}".format(clock.get_fps()))
            pg.display.flip()

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
