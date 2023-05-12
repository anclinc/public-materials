import sys
import json
from mpi_util import MPI
from io import BytesIO
from typing import List
from pdf_service import PdfService


@MPI
def main(comm, rank, size, procname):
    pdf_buffers: List[BytesIO] = []
    msg = f"Processed by {procname}, rank {rank} out of {size-1} processors"

    if rank == 0:
        path = sys.argv[1]
        """
            pdf_buffers = [
                "0_1_2_3.pdf",
                "4_5_6_7.pdf",
                "8_9_10_11.pdf",
                ...
            ]
        """  
        pdf_buffers = PdfService.split(path, size)    
        
    # Scatter the data from RANK_0 to all workers
    recv_pdf_buffer = comm.scatter(pdf_buffers, root=0)

    # Gather results to RANK_0
    result = comm.gather(PdfService.extract(recv_pdf_buffer, rank, procname, size), root=0)

    if rank == 0:
        # Remove empty result
        result = [obj for obj in result if obj]
        print(json.dumps(result, indent=2))

main()
