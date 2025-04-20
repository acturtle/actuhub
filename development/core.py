import queue
import paramiko
import threading
import time
from utils import exec_command


class Machine:
    def __init__(self, ec2_client, instance_id, ssh_key_path="ubuntu-machines.pem", ssh_username="ubuntu"):
        self.ec2_client = ec2_client
        self.instance_id = instance_id
        self.ssh_key_path = ssh_key_path
        self.ssh_username = ssh_username
        self.lock = threading.Lock()
        self.available = threading.Event()
        self.available.set()

    @property
    def ip(self):
        response = self.ec2_client.describe_instances(InstanceIds=[self.instance_id])
        return response['Reservations'][0]['Instances'][0].get('PublicIpAddress')

    def start(self):
        self.ec2_client.start_instances(InstanceIds=[self.instance_id])
        waiter = self.ec2_client.get_waiter('instance_running')
        waiter.wait(InstanceIds=[self.instance_id])

    def setup(self):
        """Install git, python, venv and pip"""
        commands = [
            "sudo apt update",
            "sudo apt install -y git",
            "sudo apt install -y python3",
            "sudo apt install -y python3-venv",
            "sudo apt install -y python3-pip",
            "sudo python3 -m pip install --upgrade pip",
            "python3 -m venv venv"
        ]

        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.ip, username=self.ssh_username, key_filename=self.ssh_key_path)

            for command in commands:
                print(f"\nCommand: {command}")
                exec_command(ssh, command)

    def run_job(self, job):
        with self.lock:
            self.available.clear()

            run_command = " ".join([
                "python3 run.py",
                f"--version {job.version}" if job.version else "",
                f"--chunk {job.chunk} {job.run.num_chunks}" if job.chunk else ""
            ]).strip()

            for key, value in job.kwargs.items():
                run_command += f" --{key} {value}"

            commands = [
                "source ~/venv/bin/activate && pip install --upgrade cashflower",
                "source ~/venv/bin/activate && pip install --upgrade boto3",
                f"rm -rf life-insurance",  # TODO - replace name of the folder
                f"git clone {job.run.model}",
                f"source ~/venv/bin/activate && cd life-insurance && {run_command}"  # TODO - replace repo
            ]

            with paramiko.SSHClient() as ssh:
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(self.ip, username=self.ssh_username, key_filename=self.ssh_key_path)

                for command in commands:
                    print(f"\nCommand: {command}")
                    exec_command(ssh, command, show_output=True)

            self.available.set()

    def stop(self):
        self.ec2_client.stop_instances(InstanceIds=[self.instance_id])


class Run:
    def __init__(self, model, versions, num_chunks=None):
        self.model = model
        self.versions = versions
        self.num_chunks = num_chunks


class Job:
    def __init__(self, run, version, chunk=None, **kwargs):
        self.run = run
        self.version = version
        self.chunk = chunk
        self.kwargs = kwargs


class Manager:
    def __init__(self, machines):
        self.machines = machines
        self.job_queue = queue.Queue()

    def add_job(self, job):
        self.job_queue.put(job)

    def schedule_jobs(self):
        while not self.job_queue.empty():
            for machine in self.machines:
                if machine.available.is_set():
                    job = self.job_queue.get()
                    threading.Thread(target=machine.run_job, args=(job,)).start()
            time.sleep(1)
