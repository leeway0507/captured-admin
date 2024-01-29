import subprocess


def check_port_open(port):
    try:
        # Run the 'lsof' command to check for open files on the specified port
        result = subprocess.run(
            ["lsof", "-i", f"tcp:{port}"], capture_output=True, text=True, check=True
        )

        # Print the output
        return True

    except subprocess.CalledProcessError as e:
        # Handle any errors that occur during the execution of the command
        return False
