# source .venv/bin/activate
# uv run python src/python_boilerplate/torch.py
# uv run python -m cProfile -s tottime src/python_boilerplate/main.py

# On Ubuntu 24.04 install
# apt install libgl1 libgl1-mesa-dev

import time
import math

import glfw
import moderngl
import numpy as np
from numpy.typing import NDArray

# Window setup
glfw.init()
glfw.window_hint(glfw.VISIBLE, glfw.FALSE)  # Start hidden until context is ready
window = glfw.create_window(1600, 1000, "Particles", None, None)
glfw.make_context_current(window)
glfw.show_window(window)

# Moderngl context
ctx = moderngl.create_context()
ctx.enable(moderngl.BLEND)

# Shader program
prog = ctx.program(
    vertex_shader="""
    #version 330
    in vec2 in_position;
    void main() {
        gl_Position = vec4(in_position, 0.0, 1.0);
        gl_PointSize = 2.0;
    }
    """,
    fragment_shader="""
    #version 330
    out vec4 fragColor;
    void main() {
        fragColor = vec4(1.0);  // White
    }
    """,
)

# nb_particles = 1_000_000
nb_particles = 1000

# Buffer and Vertex Array
vbo = ctx.buffer(reserve=nb_particles * 2 * 4)  # float32 = 4 bytes
vao = ctx.simple_vertex_array(prog, vbo, "in_position")


def draw(particles: NDArray[np.float32]) -> None:
    ctx.clear(0.0, 0.0, 0.0)  # Black background
    vbo.write(particles.astype("f4").tobytes())
    vao.render(mode=moderngl.POINTS)
    glfw.swap_buffers(window)
    glfw.poll_events()


class Simulation:
    def __init__(self, nb_particles: int) -> None:
        self.particles = np.random.uniform(-1, 1, (nb_particles, 2)).astype(np.float32)
        # self.velocities = np.random.uniform(-0.001, 0.001, (nb_particles, 2)).astype(
        #     np.float32
        # )
        self.velocities = np.zeros((nb_particles, 2))

    def update_velocities(self) -> None:
        for i, p in enumerate(self.particles):
            for j, q in enumerate(self.particles):
                if i == j:
                    continue

                dx = p[0] - q[0]
                dy = p[1] - q[1]
                dist_sq = dx * dx + dy * dy

                if dist_sq < 0.1:
                    force = 0.0001 / max(dist_sq, 1e-6)
                    self.velocities[i] += [dx, dy] * force
                    self.velocities[j] -= [dx, dy] * force

    def update_particles(self) -> None:
        self.update_velocities()
        self.particles += self.velocities
        # Wrap around
        self.particles = (self.particles + 1) % 2 - 1


def main() -> None:
    last_time = time.time()
    frame_count = 0
    fps = 0

    sim = Simulation(nb_particles)
    while not glfw.window_should_close(window):
        current_time = time.time()
        frame_count += 1
        if current_time - last_time >= 1.0:
            fps = frame_count
            frame_count = 0
            last_time = current_time

        sim.update_particles()

        draw(sim.particles)
        glfw.set_window_title(window, f"{len(sim.particles)} Particles - FPS: {fps}")

    glfw.terminate()


if __name__ == "__main__":
    main()
