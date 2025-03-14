import boto3
import queue
import threading
import time
from core import Job, Machine, Run
from dotenv import load_dotenv

# Connect with AWS
load_dotenv()
ec2_client = boto3.client('ec2')

# We have EC2 machines
machine_1 = Machine(ec2_client=ec2_client, instance_id="i-02a2e2e65f4ad6c77")
machine_2 = Machine(ec2_client=ec2_client, instance_id="i-0dcb10c450e33abad")
# machine_1.start()
# machine_2.start()
machines = [machine_1, machine_2]

# We have Runs
run_1 = Run(model="https://github.com/acturtle/life-insurance", versions=[1, 2])
run_2 = Run(model="https://github.com/acturtle/life-insurance", versions=[3, 4])

# We translate Runs into Jobs
job_1 = Job(run=run_1, version=1)
job_2 = Job(run=run_1, version=2)
job_3 = Job(run=run_2, version=3)
job_4 = Job(run=run_2, version=4)

# # We create a queue for jobs and run them
job_queue = queue.Queue()
job_queue.put(job_1)
job_queue.put(job_2)
job_queue.put(job_3)
job_queue.put(job_4)

while not job_queue.empty():
    for machine in machines:
        if machine.available.is_set():
            job = job_queue.get()
            threading.Thread(target=machine.run_job, args=(job,)).start()
    time.sleep(1)

# Stop machines
machine_1.stop()
machine_2.stop()
