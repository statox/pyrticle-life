import concurrent
import math
import random
import time
from concurrent.futures.process import ProcessPoolExecutor
from multiprocessing import shared_memory

import numpy as np

NP_DATA_TYPE = np.float64


def create_shared_memory_nparray(name: str, data):  # type: ignore[no-untyped-def]
    data_shape = np.shape(data)
    d_size = np.dtype(NP_DATA_TYPE).itemsize * np.prod(data_shape)

    shm = shared_memory.SharedMemory(create=True, size=d_size, name=name)

    dst = np.ndarray(shape=data_shape, dtype=NP_DATA_TYPE, buffer=shm.buf)
    dst[:] = data[:]
    return shm


class Simulation:
    def __init__(self) -> None:
        initial_data = [0 for _ in range(10)]
        # self.nb_workers = multiprocessing.cpu_count() // 2
        self.nb_workers = 2
        self.data_shape = np.shape(initial_data)
        self.positions_shm = create_shared_memory_nparray("positions", initial_data)

    def release(self) -> None:
        # Free and release the shared memory block
        self.positions_shm.close()
        self.positions_shm.unlink()

    def print_positions(self) -> None:
        positions = np.ndarray(
            self.data_shape, dtype=NP_DATA_TYPE, buffer=self.positions_shm.buf
        )
        print(positions)

    def update_at_index(self, index: int) -> None:
        print("Start update at index", index)
        positions = np.ndarray(
            self.data_shape, dtype=NP_DATA_TYPE, buffer=self.positions_shm.buf
        )
        while positions[index] < 10_000_000:
            positions[index] += 1
            math.sqrt(random.random() * 1_000_000)
        print("End update at index", index)

    def run(self) -> None:
        start = time.time()
        futures = []
        with ProcessPoolExecutor(max_workers=self.nb_workers) as executor:
            for i in range(self.data_shape[0]):
                future = executor.submit(self.update_at_index, i)
                futures.append(future)

        futures, _ = concurrent.futures.wait(futures)

        print(f"run time {time.time() - start}")


if __name__ == "__main__":
    sim = Simulation()
    sim.print_positions()
    sim.run()
    sim.print_positions()
    sim.release()
