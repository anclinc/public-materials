# MPI Sample Application
**Pre-requisite:**
- An Amazon rocky linux instance is already prepared.

## I. Setting up Amazon EC2 Instance as NFS Server
1. On your local pc, modify the `hosts` file to contain the private IP Address of the MPI nodes and their corresponding number of processes to be allocated.
    ```
    10.0.0.1 slots=2
    10.0.0.2 slots=3
    ```

2. On your local pc, upload the following files; **`Makefile`**, **`setup.sh`**, **`hosts`** and **`.env`**.
    ```bash
    $ scp -i <your_private_key> Makefile setup.sh hosts .env rocky@<public_ip_or_public_dns>:/home/rocky
    ```

3. SSH to your AWS instance and execute the following command.
    ```bash
    $ sudo chmod +x ./setup.sh
    $ ./setup.sh
    ```
    > This command will update the instance OS and install `make` which is necessary for running make commands.

4. Still on Amazon EC2 instance, navigate to the directory where you uploaded the project files and run `make` command to install `python`, `native openmpi` libraries, and the `sample mpi application`.
    
    ```bash
    $ make conf-server-with-app
    ```
    It should take around 5 to 10 minutes.

5. After the installation, verify if `python` and `openmpi` has been successfully installed.
    ```bash
    $ which python3.9
    >>> /usr/bin/python3.9
    
    $ which mpirun
    >>> /opt/openmpi/bin/mpirun
    ```
    5.1. If somehow if fails to find `mpirun`, check `.bashrc` files if environment variables are appended. If not, make sure to append the following:
    ```/home/rocky/.bashrc
    export PATH= ...:/opt/openmpi/bin
    export LD_LIBRARY_PATH=:/opt/openmpi/lib
    ```
    5.2. Execute the following command to export the environment variables.
    ```bash
    $ source ~/.bashrc
    ```
    5.3. Perform `Step 4` again to verify `python` and `openmpi` is installed.

6. Run the sample application.
    ```bash
    $ cd public-materials/mpi/sample-app
    $ make
    ```

## II. Setting up Amazon EC2 Instance as NFS Client
1. On your local pc, upload the following files; **`Makefile`**, and **`setup.sh`**.
    ```bash
    $ scp -i <your_private_key> Makefile setup.sh rocky@<public_ip_or_public_dns>:/home/rocky
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
    
## III. Running the Sample Application
1. Modify the `hosts` the file to contain either of the following:
    - IP Address 
        ```sh
        $ hostname -I
        ```
    - Short Hostname; or
        ```sh
        $ hostname -s
        ```
    - Full Hostname
        ```sh
        $ hostname -b
        ```
2. Run the following `make` command to start running the sample mpi application.
```sh
$ make test-app HOSTS=~/hosts
```
This command will perform the following:
- Create a symbolic link of the `hosts` file you created, to the `hosts` file that the sample app uses.
- Execute the sample app's `make` command to run the application.