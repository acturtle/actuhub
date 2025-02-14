import paramiko
from utils import exec_command


class Machine:
    def __init__(self, machine_id, ip_address, ssh_key_path, ssh_username):
        self.id = machine_id
        self.ip_address = ip_address
        self.ssh_key_path = ssh_key_path
        self.ssh_username = ssh_username


class Run:
    def __init__(self, run_id, model, versions):
        self.id = run_id
        self.model = model
        self.versions = versions


class Execution:
    def __init__(self, execution_id, machine, run, run_version):
        self.id = execution_id
        self.machine = machine
        self.run = run
        self.run_version = run_version

    def launch(self):
        commands = [
            # Python + pip
            "sudo apt update",
            "sudo apt install -y python3",
            "sudo apt install -y python3-pip",
            "sudo python3 -m pip install --upgrade pip",

            # Virtual environment
            "sudo apt install -y python3-venv",
            "python3 -m venv ~/venv",
            "source ~/venv/bin/activate && echo $VIRTUAL_ENV && pip install cashflower",

            # Git + repo
            "sudo apt install -y git",
            f"git clone {self.run.model}",
            f"source ~/venv/bin/activate && cd life-insurance && python3 run.py"  # TODO - replace repo
        ]

        # SSH connection
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.machine.ip_address, username=self.machine.ssh_username, key_filename=self.machine.ssh_key_path)

        for command in commands:
            print(f"\nCommand: {command}")
            exec_command(ssh, command)
