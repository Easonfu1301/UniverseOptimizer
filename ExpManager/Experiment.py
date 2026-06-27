import os

from utils import *
from utils.funny_test import run_haha_job
from ExpManager.Trial import Trial



class Experiment:
    def __init__(self, name, description, optimizer):
        self.name = name
        self.description = description
        self.optimizer = optimizer
        self.base_dir = os.path.join(optimizer.base_dir, "Experiments", f"Exp_{self.name}")


        self.trials = []



    def create_folder_structure(self):
        folders = [
            os.path.join(self.base_dir, "description"),
            os.path.join(self.base_dir, "trials"),
            os.path.join(self.base_dir, "summary"),
            os.path.join(self.base_dir, "ana_scripts"),
        ]
        for folder in folders:
            os.makedirs(folder, exist_ok=True)
            print(f"Created folder: {folder}")

    def run_all_trials(self):
        print(f"Running all trials for experiment: {self.name}")

    def add_trial(self, config, index):
        trial = Trial(
            name=f"Trial_{index}",
            config=config,
            experiment=self,
        )

        self.trials.append(trial)
        trial.create_folder_structure()
        trial.dump_config()


    def get_n_trials(self):
        return len(self.trials)





if __name__ == "__main__":
    exp = Experiment(
        name="Test Experiment",
        description="This is a test experiment.",
    )
    # exp.run()