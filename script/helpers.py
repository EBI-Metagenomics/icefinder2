import subprocess
import logging
from pathlib import Path
import csv

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_command(command: str, output_file: Path = None) -> None:
    """Run a command using a subprocess
    """
    try:
        command_str = list(map(str, command))
        logging.info(f"Command: {' '.join(command_str)}")
        # Execute the command
        result = subprocess.run(
            command_str,
            check=True,
            stdout=subprocess.PIPE if output_file is None else open(output_file, 'w'),
            stderr=subprocess.PIPE,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed with return code {e.returncode}")
        logging.error(f"Command output: {e.output}")
        logging.error(f"Command error output: {e.stderr}")
        raise
    return result.stdout
