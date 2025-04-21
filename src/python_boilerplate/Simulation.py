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
        # initial_data = [0 for _ in range(10)]
        initial_data = [9, 10]
        # self.nb_workers = multiprocessing.cpu_count() // 2
        self.nb_workers = 2
        self.data_shape = np.shape(initial_data)
        self.positions_shm = create_shared_memory_nparray("positions", initial_data)
        self.positions_next_shm = create_shared_memory_nparray(
            "positions_next", initial_data
        )

    def release(self) -> None:
        # Free and release the shared memory block
        self.positions_shm.close()
        self.positions_shm.unlink()

        self.positions_next_shm.close()
        self.positions_next_shm.unlink()

    def print_array(self, array: shared_memory.SharedMemory) -> None:
        array = np.ndarray(self.data_shape, dtype=NP_DATA_TYPE, buffer=array.buf)
        print(array)

    def print_positions(self) -> None:
        self.print_array(self.positions_shm)

    def print_positions_next(self) -> None:
        self.print_array(self.positions_next_shm)

    def update_at_index(self, index: int) -> None:
        print("Update at index", index)
        positions = np.ndarray(
            self.data_shape, dtype=NP_DATA_TYPE, buffer=self.positions_shm.buf
        )
        positions_next = np.ndarray(
            self.data_shape, dtype=NP_DATA_TYPE, buffer=self.positions_next_shm.buf
        )
        curr = positions[index]
        displacement = 0
        for i, other in enumerate(positions):
            if i == index:
                continue

            dist = math.sqrt((other - curr) * (other - curr))
            print(f"Between {curr} and {other} dist is {dist}")

            if dist < 4:
                displacement += curr - other

            positions_next[index] = curr + displacement

    def run(self) -> None:
        print("Start run ========")
        sim.print_positions()
        sim.print_positions_next()

        start = time.time()
        futures = []
        with ProcessPoolExecutor(max_workers=self.nb_workers) as executor:
            for i in range(self.data_shape[0]):
                future = executor.submit(self.update_at_index, i)
                futures.append(future)

        futures, _ = concurrent.futures.wait(futures)

        (self.positions_shm, self.positions_next_shm) = (
            self.positions_next_shm,
            self.positions_shm,
        )

        sim.print_positions()
        sim.print_positions_next()

        print(f"run time {time.time() - start}")


if __name__ == "__main__":
    sim = Simulation()
    sim.run()
    sim.run()
    sim.run()
    sim.release()
