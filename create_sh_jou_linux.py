#import subprocess
#!/usr/bin/env python

cpus = [8]
file_name="aircraft_wing_2m"
benchmark_iterations=10
nodes=1
avx_status='noavx'

if avx_status=='noavx':
    avx_command=""
else:
    avx_command=" -platform=intel"

script_temp="""
file set-tui-version "18.2"
file read-case-data "{0}"
file read-macro benchmark.scm
file start-transcript {0}_{1}_core_{2}.trn
(benchmark '(iterate {3}))
exit yes
"""

for cpu in cpus:
	jou_file_name = "{0}_core_{1}.jou".format(cpu,avx_status)
	with open(jou_file_name, 'wt') as jou_file:
		jou_file.write(script_temp.format(file_name, cpu, avx_status, benchmark_iterations))

pbs_temp="""#!/bin/bash
#PBS -S /bin/bash
#PBS -m abe
#PBS -l nodes={0}:ppn={1}
cd $PBS_O_WORKDIR
/apps/ansys_inc/v182/fluent/bin/fluent 3ddp -t{1} -mpi=intel{3} -cnf=$PBS_NODEFILE -g -i {1}_core_{2}.jou
"""
for cpu in cpus:
	sh_file_name = "{0}_core_{1}.sh".format(cpu,avx_status)
	with open(sh_file_name, 'wt') as sh_file:
		sh_file.write(pbs_temp.format(nodes, cpu, avx_status,avx_command))

# subprocess.run(['qsub', sh_file_name])
