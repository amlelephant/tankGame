# create a terminal window using opengl and pygame with a 2d array of characters

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
from PIL import Image  # Required for loading image data

# Vertex shader source code
vertex_shader = """
#version 330 core
layout (location = 0) in vec2 position;
out vec2 texCoord;

void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
    texCoord = (position + 1.0) / 2.0;
}
"""

# Fragment shader source code for the CRT effect
fragment_shader = """
#version 330 core
in vec2 texCoord;
out vec4 fragColor;
uniform sampler2D screenTexture;

void main()
{
    vec2 uv = texCoord;
    vec3 color = texture(screenTexture, uv).rgb;

    // Apply scanlines
    float scanlineStrength = 0.1; // Adjust strength
    float scanline = mod(uv.y * 100.0, 2.0) < 1.0 ? 0.9 : 1.0;
    color *= scanline;

    // Apply phosphor glow
    color = pow(color, vec3(2.2)); // Apply gamma correction
    color = mix(vec3(0.0), color, 0.8); // Add glow

    fragColor = vec4(color, 1.0);

    // Apply barrel distortion
    float barrelStrength = 0.1; // Adjust strength
    vec2 distortion = uv * 2.0 - 1.0;
    float r = dot(distortion, distortion);
    uv = distortion * (1.0 + barrelStrength * r);

    // Apply CRT effect
    float gamma = 2.2; // Adjust gamma
    fragColor.rgb = pow(fragColor.rgb, vec3(1.0 / gamma));

    // Apply color bleed
    float bleedStrength = 0.1; // Adjust strength
    vec2 bleedUV = uv + vec2(0.01, 0.01);
    vec3 bleedColor = texture(screenTexture, bleedUV).rgb;
    fragColor.rgb = mix(fragColor.rgb, bleedColor, bleedStrength);
}
"""

# Initialize Pygame
pygame.init()
pygame.display.set_caption("CRT Effect")
screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)

# Create a shader program with the vertex and fragment shaders
shader = compileProgram(compileShader(vertex_shader, GL_VERTEX_SHADER), compileShader(fragment_shader, GL_FRAGMENT_SHADER))

# Create a texture to render to
texture = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texture)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

# Create a framebuffer object
fbo = glGenFramebuffers(1)
glBindFramebuffer(GL_FRAMEBUFFER, fbo)
glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, texture, 0)

# Create a vertex buffer object with the screen coordinates
vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, np.array([-1, -1, 1, -1, 1, 1, -1, 1], dtype=np.float32), GL_STATIC_DRAW)

# Create an element buffer object
ebo = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32), GL_STATIC_DRAW)

# Get the location of the screenTexture uniform in the shader program
screenTexture = glGetUniformLocation(shader, "screenTexture")

# Use the shader program
glUseProgram(shader)

# Set up the vertex attributes
position = glGetAttribLocation(shader, "position")
glEnableVertexAttribArray(position)
glVertexAttribPointer(position, 2, GL_FLOAT, GL_FALSE, 0, None)

# create a 2d array of characters
rows, cols = 24, 80
chars = [[' ' for _ in range(cols)] for _ in range(rows)]
font = pygame.font.Font(None, 24)

# main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Clear the screen
    

    # Render the characters to the screen
    for i, row in enumerate(chars):
        for j, char in enumerate(row):
            text = font.render(char, True, (255, 255, 255))
            textData = pygame.image.tostring(text, "RGBA", True)
            textTexture = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, textTexture)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text.get_width(), text.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, textData)
            glUniform1i(screenTexture, 0)
            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
            

    # Swap the buffers
    pygame.display.flip()

# Clean up
glDeleteTextures(texture)
glDeleteFramebuffers(fbo)
glDeleteBuffers(1, vbo)
glDeleteBuffers(1, ebo)
pygame.quit()
