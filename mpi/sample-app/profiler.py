import os
import subprocess
import psutil as ps
from mpi4py import MPI

def process_memory():
    process = ps.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss

def __exec(command: str):
    # print(f'Executing command:> {command}')
    subprocess.Popen(command, shell=True)

def start_monitoring(rank):
    process = ps.Process(os.getpid())
    pid = process.pid
    command = f"procpath record -i 1 -d out/{rank}.sqlite '$..children[?(@.stat.pid == {pid})]'"
    __exec(command)

def generate_report(rank):
    commands = [
        f"procpath plot -d out/{rank}.sqlite -q cpu -f out/{rank}-cpu.svg",
        f"procpath plot -d out/{rank}.sqlite -q rss -f out/{rank}-rss.svg"]

    for cmd in commands:
        __exec(cmd)


def profile(func):
    def wrapper(*args, **kwargs):
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        size = comm.Get_size()
        procname = MPI.Get_processor_name()

        mem_before = round(process_memory()  / 1024 ** 2, 2)

        kwargs['comm'] = comm
        kwargs['rank'] = rank
        kwargs['size'] = size
        kwargs['procname'] = procname

        # start_monitoring(rank)

        # Function execution
        result = func(*args, **kwargs)

        # generate_report(rank)

        # After execution
        mem_after = round(process_memory() / 1024 ** 2, 2)
        print(f"{rank}: host={procname}:consumed memory: {mem_before}MB -> {mem_after}MB: {(round(mem_after - mem_before, 2))}MB")
        return result

    return wrapper
