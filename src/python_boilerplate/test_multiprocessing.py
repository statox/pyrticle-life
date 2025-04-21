import numpy as np
from math import sqrt
from multiprocessing import Pool, Process, Lock, Array
from random import random
from time import sleep, time

if __name__ == "__main__":
    nb_counts = 10
    # counts = Array("i", [0 for _ in range(nb_counts)])
    counts = np.zeros((nb_counts, 1))

    print("Start", counts)

    def update_counts(index: int) -> None:
        prev_value = counts[index]
        counts[index] = counts[index] + 1
        print(f"Update count {index} from {prev_value} to {counts[index]}")

    lock = Lock()
    processes: list[Process] = []
    for i in range(nb_counts):
        p = Process(
            target=update_counts,
            args=(i,),
        )
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    print("End", counts)


#
# V3
#
# if __name__ == "__main__":
#     nb_counts = 10
#     counts = Array("i", [0 for _ in range(nb_counts)])

#     print("Start", counts[:])

#     def update_counts(index: int) -> None:
#         prev_value = counts[index]
#         counts[index] = counts[index] + 1
#         print(f"Update count {index} from {prev_value} to {counts[index]}")

#     lock = Lock()
#     processes: list[Process] = []
#     for j in range(5):
#         for i in range(nb_counts):
#             p = Process(
#                 target=update_counts,
#                 args=(i,),
#             )
#             p.start()
#             processes.append(p)

#     for p in processes:
#         p.join()

#     print("End", counts[:])

#
# V2
#
# def f(name: str) -> None:
#     sleep_time = random() * 2
#     sleep(sleep_time)
#     print(f"Run: {name} sleep {sleep_time}")


# def load(id: str) -> None:
#     print(f"Load {id} start")
#     start = time()
#     # for i in range(30_000_000):
#     while True:
#         n = random() * 2_000_000
#         _ = sqrt(n)

#     run_time = time() - start
#     print(f"    Load {id}	run_time {run_time}")


# if __name__ == "__main__":
#     start = time()

#     processes: list[Process] = []
#     for i in range(10):
#         p = Process(target=load, args=(f"{i}",))
#         p.start()
#         processes.append(p)

#     for p in processes:
#         p.join()

#     run_time = time() - start
#     print(f"DONE IN {run_time}")


#
# V1
#
# def f(x: int) -> int:
#     return x * x
# if __name__ == "__main__":
#     with Pool(5) as p:
#         print(p.map(f, [1, 2, 3]))
