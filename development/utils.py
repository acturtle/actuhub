def exec_command(ssh, command):
    try:
        # Get the output and errors
        stdin, stdout, stderr = ssh.exec_command(command)
        stdout_content = stdout.read().decode("utf-8")
        stderr_content = stderr.read().decode("utf-8")

        # if stdout_content:
        #     print(f"Stdout:\n{stdout_content}")
        # if stderr_content:
        #     print(f"Stderr:\n{stderr_content}")

    except Exception as e:
        print(f"Exception:\n{str(e)}")

    return None

