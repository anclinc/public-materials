# MPI Sample Application
**Pre-requisite:**
- An Amazon rocky linux instance is already prepared.

## I. Setting up Amazon EC2 Instance
1. On your local pc, upload the following files; **`Makefile`**, **`setup.sh`**, and **`.env`**.
    ```bash
    $ scp -i <your_private_key> Makefile setup.sh .env rocky@<public_ip_or_public_dns>:/home/rocky
    ```

2. SSH to your AWS instance and execute the following command.
    ```bash
    $ sudo chmod +x ./setup.sh
    $ ./setup.sh
    ```
    > This command will update the instance OS and install `make` which is necessary for running make commands.
3. Still on Amazon EC2 instance, navigate to the directory where you uploaded the project files and run `make` command to install `python`, `native openmpi` libraries, and the `sample mpi application`.
    
    ```bash
    $ make
    ```
    It should take around 5 to 10 minutes.
4. After the installation, verify if `python` and `openmpi` has been successfully installed.
    ```bash
    $ which python3.9
    >>> /usr/bin/python3.9
    
    $ which mpirun
    >>> /opt/openmpi/bin/mpirun
    ```
    4.1. If somehow if fails to find `mpirun`, check `.bashrc` files if environment variables are appended. If not, make sure to append the following:
    ```/home/rocky/.bashrc
    export PATH= ...:/opt/openmpi/bin
    export LD_LIBRARY_PATH=:/opt/openmpi/lib
    ```
    4.2. Execute the following command to export the environment variables.
    ```bash
    $ source ~/.bashrc
    ```
    4.3. Perform `Step 4` again to verify `python` and `openmpi` is installed.
5. Run the sample application.
    ```bash
    $ cd public-materials/mpi/sample-app
    $ make
    ```

## Configure AWS Instance as NFS Server

1. On your local pc, upload the following files; **`Makefile`**, **`setup.sh`**, and **`.env`**.
    ```bash
    $ scp -i <your_private_key> Makefile setup.sh .env rocky@<public_ip_or_public_dns>:/home/rocky
    ```

2. SSH to your AWS instance and execute the following command.
    ```bash
    $ sudo chmod +x ./setup.sh
    $ ./setup.sh
    ```
    > This command will update the instance OS and install `make` which is necessary for running make commands.
3. Run the following make command. 
    ```bash
    $ make conf-nfs-server
    ```
    - The script will automatically obtain the host subnet mask and convert to to CIDR notation which is required for setting up NFS directory.
    - You can also provide host's subnet in CIDR notation manually through the following command.
        - **`make conf-nfs-server HOST_CIDR=<SUBNET_CIDR>`**
    
    ```bash
    $ make conf-nfs-server HOST_CIDR=10.0.0.0/20
    ```

## Configure AWS Instace as NFS Client
1. On your local pc, upload the following files; **`Makefile`**, **`setup.sh`**, and **`.env`**.
    ```bash
    $ scp -i <your_private_key> Makefile setup.sh .env rocky@<public_ip_or_public_dns>:/home/rocky
    ```

2. SSH to your AWS instance and execute the following command.
    ```bash
    $ sudo chmod +x ./setup.sh
    $ ./setup.sh
    ```
    > This command will update the instance OS and install `make` which is necessary for running make commands.
3. Run the following make command: 
        - **`make conf-nfs-client NFS_IP_ADDR=<NFS_SERVER_IP>`**
    ```bash
    $ make conf-nfs-client NFS_IP_ADDR=10.0.0.120
    ```
    
