import os

from utils import *
from utils.funny_test import run_haha_job




class Experiment:
    def __init__(self, name, description, processor):
        self.name = name
        self.description = description
        self.processor = processor



        self.create_folder_structure()






    def run(self):
        # Placeholder for running the experiment
        print(f"Running experiment: {self.name}")
        print(f"Description: {self.description}")
        print(f"Process: {self.processor}")
        run_haha_job()


    def create_folder_structure(self):
        folders = [
            os.path.join(workdir_path, f"Exp_{self.name}", "description"),
            os.path.join(workdir_path, f"Exp_{self.name}", "trials"),
            os.path.join(workdir_path, f"Exp_{self.name}", "summary"),
            os.path.join(workdir_path, f"Exp_{self.name}", "ana_scripts"),
        ]
        for folder in folders:
            os.makedirs(folder, exist_ok=True)
            print(f"Created folder: {folder}")



    def add_trial(self, trial):
        # Placeholder for adding a trial to the experiment
        print(f"Adding trial: {trial}")




if __name__ == "__main__":
    exp = Experiment(
        name="Test Experiment",
        description="This is a test experiment.",
        processor="Sample process"
    )
    # exp.run()