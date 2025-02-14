from core import Execution, Machine, Run

# We have EC2 machines
machine_1 = Machine(machine_id=1, ip_address="52.207.233.138", ssh_key_path="ubuntu-machines.pem", ssh_username="ubuntu")
# machine_2 = Machine(machine_id=2, ip_address=, ssh_key_path="ubuntu-machines.pem", ssh_username="ubuntu")
# machine_3 = Machine(machine_id=3, ip_address=, ssh_key_path="ubuntu-machines.pem", ssh_username="ubuntu")

# We have Runs
run_1 = Run(run_id=1, model="https://github.com/acturtle/life-insurance", versions=[1])

# We create Executions
execution_1 = Execution(execution_id=1, machine=machine_1, run=run_1, run_version=1)
execution_1.launch()
