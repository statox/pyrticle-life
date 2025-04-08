# source .venv/bin/activate
# uv run python src/python_boilerplate/main.py
# uv run python -m cProfile -s tottime src/python_boilerplate/main.py

import time

import glfw
import numpy as np
import OpenGL.GL as gl


# Function to handle wrapping
def wrap_around(p: tuple[float, float]) -> tuple[float, float]:
    x = (p[0] + 1) % 2 - 1  # Wrap around horizontally
    y = (p[1] + 1) % 2 - 1  # Wrap around vertically
    return (x, y)


def draw(particles: np.ndarray, fps: int, window: glfw._GLFWwindow) -> None:
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    # Draw white borders
    gl.glColor3f(1, 1, 1)
    gl.glLineWidth(2)
    gl.glBegin(gl.GL_LINE_LOOP)
    gl.glVertex2f(-1, -1)
    gl.glVertex2f(1, -1)
    gl.glVertex2f(1, 1)
    gl.glVertex2f(-1, 1)
    gl.glEnd()

    radius = 0.01
    for p in particles:
        gl.glBegin(gl.GL_TRIANGLE_FAN)
        gl.glColor3f(1, 0, 0)
        gl.glVertex2f(p[0], p[1])  # Center
        for angle in np.linspace(0, 2 * np.pi, 20):
            gl.glVertex2f(p[0] + radius * np.cos(angle), p[1] + radius * np.sin(angle))
        gl.glEnd()

    # Display FPS
    glfw.set_window_title(window, f"{len(particles)} Particles - FPS: {fps}")

    glfw.swap_buffers(window)
    glfw.poll_events()


def main() -> None:
    # Initialize GLFW
    if not glfw.init():
        raise Exception("GLFW can't be initialized")

    window = glfw.create_window(800, 600, "Particles", None, None)
    if not window:
        glfw.terminate()
        raise Exception("GLFW window can't be created")

    glfw.make_context_current(window)

    # Set background color to grey
    gl.glClearColor(0.5, 0.5, 0.5, 1.0)

    # Particle positions (10 circles)
    nb_particles = 1000
    particles = np.random.uniform(-1, 1, (nb_particles, 2))
    velocities = np.random.uniform(-0.01, 0.01, (nb_particles, 2))

    # particles = np.array([[0, y] for y in np.linspace(0, 600, 10)])
    # velocities = np.array([[0.01, 0] for y in np.linspace(0, 600, 10)])

    last_time = time.time()
    frame_count = 0
    fps = 0

    # Main loop
    while not glfw.window_should_close(window):
        current_time = time.time()
        frame_count += 1
        if current_time - last_time >= 1.0:
            fps = frame_count
            frame_count = 0
            last_time = current_time

        # Update particle positions and apply wrapping
        particles += velocities
        particles = np.array([wrap_around(p) for p in particles])

        draw(particles, fps, window)

    glfw.terminate()


main()
