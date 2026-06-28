import os
import time

from utils import *
from utils.funny_test import run_haha_job
from ExpManager.Trial import Trial
import threading
from EAgent.SummaryAgent import SummaryAgent



class Experiment:
    def __init__(self, name, description, optimizer):
        self.name = name
        self.description = description
        self.optimizer = optimizer
        self.base_dir = os.path.join(optimizer.base_dir, "Experiments", f"Exp_{self.name}")


        self.all_complete = False
        self.trials = []

        self.create_folder_structure()
        self.dump_description()



    def monitor_thread(self):
        while not self.all_complete:
            if all([trial.processed for trial in self.trials]):
                print(f"All trials in experiment {self.name} are complete.")
                self.all_complete = True
            else:
                print(f"Monitoring experiment {self.name}:, remaining trials: {len([trial for trial in self.trials if not trial.processed])}")
                time.sleep(1)

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
        self.all_complete = False
        for index, trial in enumerate(self.trials):
            print(f"Running {trial.name} with config: {trial.config}")
            trial.submit_job(script=self.optimizer.script_path, task_type="shell")


        self.monitor = threading.Thread(target=self.monitor_thread)
        self.monitor.start()



    def add_trial(self, config, index):
        trial = Trial(
            name=f"Trial_{index}",
            config=config,
            experiment=self,
        )

        self.trials.append(trial)

    def summary(self):
        workdir = os.path.join(self.base_dir, "summary")

        summary_agent = SummaryAgent(
            workdir, self.description
        )
        summary_agent.generate_summary()

    def get_n_trials(self):
        return len(self.trials)

    def dump_description(self):
        description_path = os.path.join(self.base_dir, "description", "description.txt")
        with open(description_path, "w") as f:
            f.write(self.description)



if __name__ == "__main__":
    exp = Experiment(
        name="Test Experiment",
        description="This is a test experiment.",
    )
    # exp.run()