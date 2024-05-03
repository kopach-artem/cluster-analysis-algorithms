import os
import random
from pathlib import Path


class Helper:
    target_directory = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "..", "..", "..", "data_bank", "results"
        )
    )
    target_path = Path(target_directory)

    @staticmethod
    def random_color():
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    @staticmethod
    def find_next_file_number(algorithm_name: str):
        if not Helper.target_path.exists():
            return "Path problem!"

        files = [file for file in Helper.target_path.glob(f"{algorithm_name}*.png")]
        count = len(files) + 1
        return count


# def console_output()
