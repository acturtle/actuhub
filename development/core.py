import paramiko
from utils import exec_command


class Machine:
    def __init__(self, ip_address, ssh_key_path, ssh_username):
        self.ip_address = ip_address
        self.ssh_key_path = ssh_key_path
        self.ssh_username = ssh_username
        self.setup()

    def setup(self):
        """Install git, python, venv and pip"""
        commands = [
            "sudo apt update",
            "sudo apt install -y git",
            "sudo apt install -y python3",
            "sudo apt install -y python3-venv",
            "sudo apt install -y python3-pip",
            "sudo python3 -m pip install --upgrade pip",
        ]

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip_address, username=self.ssh_username, key_filename=self.ssh_key_path)

        for command in commands:
            print(f"\nCommand: {command}")
            exec_command(ssh, command)


class Run:
    def __init__(self, model, versions):
        self.model = model
        self.versions = versions


class Job:
    def __init__(self, run, version):
        self.run = run
        self.version = version


class Execution:
    def __init__(self, job, machine):
        self.job = job
        self.machine = machine

    def launch(self):
        commands = [
            "source ~/venv/bin/activate && echo $VIRTUAL_ENV && pip install cashflower",
            f"git clone {self.job.run.model}",
            f"source ~/venv/bin/activate && cd life-insurance && python3 run.py"  # TODO - replace repo and add version
        ]

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.machine.ip_address, username=self.machine.ssh_username, key_filename=self.machine.ssh_key_path)

        for command in commands:
            print(f"\nCommand: {command}")
            exec_command(ssh, command)
