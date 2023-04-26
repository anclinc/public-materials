import os
import sys
import csv
import shutil
import subprocess
from typing import Dict


DB_PATH = 'out/db.sqlite'

def extract_data(path: str) -> Dict:
    data = []
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append({
                'host': row[0],
                'rank': row[1],
                'pid': row[2]})
    return data

def generate_report(host: str, rank: str, pid: str) -> None:
    title = f'{host}:rank={rank}'
    print(f'Generating report for: {title}')
    command = f'procpath plot -d {DB_PATH} -q cpu -q rss -f out/{rank}-resource.svg --title {title} -p {pid}'
  
    if not shutil.which('procpath'):
        command = f'~/.local/bin/{command}'

    subprocess.call(command, shell=True)


def main() -> None:
    pids_filepath = sys.argv[1]

    if not all([os.path.exists(f) for f in [DB_PATH, pids_filepath]]):
        raise Exception('Database and process ids does not exist. Run `make` command.')

    host_data = os.listdir(pids_filepath)
    for fname in host_data:
        data = extract_data(f'{pids_filepath}/{fname}')
        host, rank, pid = tuple(data[0].values())
        generate_report(host, rank, pid)

main()