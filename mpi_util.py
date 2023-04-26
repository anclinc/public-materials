from mpi4py import MPI as mpi
from monitor_process import MonitoringProcess


class MPI:
    def __init__(self, func) -> None:
        self._func = func

    def __call__(self, *args, **kwargs):
        comm = mpi.COMM_WORLD
        kwargs['comm'] = comm
        kwargs['rank'] = comm.Get_rank()
        kwargs['size'] = comm.Get_size()
        kwargs['procname'] = mpi.Get_processor_name()
        
        monitor_process = MonitoringProcess(self._func)

        return monitor_process(*args, **kwargs)