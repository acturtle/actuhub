import paramiko

from urllib.parse import urlparse


# Credentials
EC2_INSTANCE_IP = "3.88.49.150"
PRIVATE_KEY_PATH = "ssh/cashflowerhub-keypair.pem"
USERNAME = "ubuntu"


def exec_command(ssh, command):
    try:
        stdin, stdout, stderr = ssh.exec_command(command)

        # Get the output and errors
        stdout_content = stdout.read().decode("utf-8")
        stderr_content = stderr.read().decode("utf-8")

        # Print output if available
        if stdout_content:
            print(f"Stdout:\n{stdout_content}")
        if stderr_content:
            print(f"Stderr:\n{stderr_content}")

        # Return the result as a tuple (returncode, stdout_content, stderr_content)
        return (stdout.channel.recv_exit_status(), stdout_content, stderr_content)

    except Exception as e:
        # Handle any exceptions and return error status
        print(f"Exception:\n{str(e)}")
        return (1, "", str(e))  # Return a non-zero exit code to indicate an error


def parse_string_to_list(input_string):
    result = []
    elements = input_string.split(',')  # Split by commas to get individual parts

    for element in elements:
        element = element.strip()  # Remove any surrounding whitespace

        if ':' in element or '-' in element:
            # Handle ranges defined by ':' or '-'
            start, end = map(int, element.replace(':', '-').split('-'))
            result.extend(range(start, end + 1))
        else:
            # Handle single numbers
            result.append(int(element))

    return result


def get_commands(run):
    # Extract repository details
    repo_url = run.cash_flow_model.repository_url
    repo_name = urlparse(repo_url).path.split('/')[-1].replace('.git', '')

    # Execution commands
    commands = [
        # Python + pip
        "sudo apt update",
        "sudo apt install -y python3",
        "sudo apt install -y python3-pip",
        "sudo python3 -m pip install --upgrade pip",

        # Virtual environment setup
        "sudo apt install -y python3-venv",  # Install venv if not installed
        "python3 -m venv ~/venv",  # Create a virtual environment in the home directory
        "source ~/venv/bin/activate && echo $VIRTUAL_ENV && pip install cashflower",  # Install the cashflower package in the virtual environment

        # Git + repo
        "sudo apt install -y git",
        f"git clone {repo_url}",
        f"source ~/venv/bin/activate && cd {repo_name} && python3 run.py"
        
        # Deactivate virtual environment
        # "deactivate"
    ]

    return commands


def process_run(run):
    try:
        run.status = 'running'
        run.save()

        # SSH connection
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(EC2_INSTANCE_IP, username=USERNAME, key_filename=PRIVATE_KEY_PATH)

        commands = get_commands(run)
        result = (0,)
        for command in commands:
            print(f"\nCommand: {command}")
            result = exec_command(ssh, command)

        run.status = 'completed' if result[0] == 0 else 'error'
        ssh.close()
    except Exception as e:
        run.status = 'error'
        print(f"Error processing run {run.id}: {e}")

    finally:
        run.save()
