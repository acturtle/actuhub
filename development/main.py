import boto3
import queue
import threading
import time
from core import Job, Machine, Run
from dotenv import load_dotenv

from utils import load_from_s3, aggregate


# Connect with AWS
load_dotenv()
ec2_client = boto3.client('ec2')

# We have EC2 machines
machine_1 = Machine(ec2_client=ec2_client, instance_id="i-02a2e2e65f4ad6c77")
machine_2 = Machine(ec2_client=ec2_client, instance_id="i-0dcb10c450e33abad")

machine_1.start()
machine_2.start()

machine_1.setup()
machine_2.setup()

machines = [machine_1, machine_2]

# We have Runs
run_1 = Run(model="https://github.com/acturtle/life-insurance", versions=[1], num_chunks=2)

# We translate Runs into Jobs
job_1 = Job(run=run_1, version=1, chunk=1, output_filename="output-chunk1.csv", diagnostic_filename="diagnostic1.csv")
job_2 = Job(run=run_1, version=1, chunk=2, output_filename="output-chunk2.csv", diagnostic_filename="diagnostic2.csv")

# # We create a queue for jobs and run them
job_queue = queue.Queue()
job_queue.put(job_1)
job_queue.put(job_2)

threads = []

while not job_queue.empty():
    for machine in machines:
        if machine.available.is_set() and not job_queue.empty():
            job = job_queue.get()
            thread = threading.Thread(target=machine.run_job, args=(job,))
            thread.start()
            threads.append(thread)
    time.sleep(1)

# Wait for all threads to complete
for thread in threads:
    thread.join()

# Stop machines
machine_1.stop()
machine_2.stop()

# Aggregate results
s3_client = boto3.client('s3')

output_chunk1 = load_from_s3(s3_client, "actuhub-dev", "output-chunk1.csv")
output_chunk2 = load_from_s3(s3_client, "actuhub-dev", "output-chunk2.csv")
diagnostic = load_from_s3(s3_client, "actuhub-dev", "diagnostic1.csv")

result = aggregate(output_chunk1, output_chunk2, diagnostic)
result.to_csv("a-really-awesome-output3.csv")
