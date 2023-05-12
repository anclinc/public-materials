import os
import shutil
import subprocess
import psutil as ps
from typing import Any

class MonitoringProcess:

    PID_PATH = 'out/pids'
    DB_PATH = 'out/db.sqlite'

    def __init__(self, func: Any) -> None:
        self._func = func

    def __call__(self, *args, **kwargs) -> Any:
        process = ps.Process(os.getpid())
        rank = kwargs['rank']
        procname = kwargs['procname']

        # Write rank with pid in out/pids file
        self.__write_pid(procname, rank, process.pid)

        # Get rss before function execution
        rss_before = self.__get_mem_rss()

        # Start process monitoring
        self.__monitor_process(process.pid)

        # Execute function
        result = self._func(*args, **kwargs)

        # Get rss after function execution
        rss_after = self.__get_mem_rss()
        rss_consumption = round(rss_after - rss_before, 2)

        print(f"{rank}: host={procname}:consumed memory: {rss_before}MB -> {rss_after}MB: {rss_consumption}MB")
        return result

    def __get_mem_rss(self) -> float:
        process = ps.Process(os.getpid())
        mem_info = process.memory_info()
        rss = mem_info.rss

        return round(rss / 1024 ** 2, 2)

    def __monitor_process(self, pid: int) -> None:
        command = f"procpath record -i 1 -d out/db.sqlite '$..children[?(@.stat.pid == {pid})]' --stop-without-result"
        self.__exec_cmd(command)

    def __exec_cmd(self, cmd: str) -> None:
        if not shutil.which('procpath'):
            cmd = f'~/.local/bin/{cmd}'
        subprocess.Popen(cmd, shell=True)

    def __write_pid(self, host: str, rank: int, pid: int) -> None:
        fname = f'out/pid/{str(rank)}_{str(pid)}'
        os.makedirs(os.path.dirname(fname), exist_ok=True)

        with open(fname, 'w+') as f:
            f.write(f"{host},{str(rank)},{str(pid)}\n")