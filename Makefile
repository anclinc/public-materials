all: clean run4_30mb report

hosts:
	cat hosts

clean:
	rm -r out/* || true

run_30mb:
	mpirun -np 2 --hostfile ./hosts python3.9 main.py "assets/sample_30MB.pdf"

run4_30mb:
	mpirun -np 4 --hostfile ./hosts python3.9 main.py "assets/sample_30MB.pdf"
	
run8_30mb:
	mpirun -np 8 --hostfile ./hosts python3.9 main.py "assets/sample_30MB.pdf"

report:
	python3.9 generate_report.py "out/pid"
