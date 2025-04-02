import subprocess
import os

def start_call(number: str):
    command = f"echo 'd {number}' | baresip"
    env = os.environ.copy()
    process = subprocess.Popen(
        command,
        shell=True,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return process


def end_call():
    command = "echo 'q' | baresip"
    env = os.environ.copy()
    process = subprocess.Popen(
        command,
        shell=True,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return process