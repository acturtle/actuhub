import queue
from core import Execution, Job, Machine, Run

# We have EC2 machines
machine_1 = Machine(ip_address="52.207.233.138", ssh_key_path="ubuntu-machines.pem", ssh_username="ubuntu")
# machine_2 = Machine(machine_id=2, ip_address=, ssh_key_path="ubuntu-machines.pem", ssh_username="ubuntu")

# We have Runs
run_1 = Run(model="https://github.com/acturtle/life-insurance", versions=[1, 2])

# We translate Runs into Jobs
job_1 = Job(run=run_1, version=1)
job_2 = Job(run=run_1, version=2)

# We create a queue for jobs
job_queue = queue.Queue()
job_queue.put(job_1)
job_queue.put(job_2)

# We run the queue until it's empty
while not job_queue.empty():
    job = job_queue.get()
    execution = Execution(job=job, machine=machine_1)
    execution.launch()
