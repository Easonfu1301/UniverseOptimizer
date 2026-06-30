import os
import json
import time
from FUCKROOT import HEP_PLOT
from utils import *
from utils.funny_test import run_haha_job
from ExpManager.Trial import Trial
import threading
import matplotlib
matplotlib.use('Agg')

from EAgent.SummaryAgent import SummaryAgent
import matplotlib.pyplot as plt


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
                self.plot_pareto_front()
                self.summary()
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

        summary_agent = SummaryAgent(
            self.base_dir, self.optimizer.base_dir, self.optimizer.metrics_to_optimize,
            self.optimizer.metrics_direction,
            self.optimizer.target_metrics
        )
        summary_agent.generate_summary()

    def get_n_trials(self):
        return len(self.trials)

    def dump_description(self):
        description_path = os.path.join(self.base_dir, "description", "description.md")
        with open(description_path, "w") as f:
            f.write(self.description)


    def plot_pareto_front(self, keys=None):
        if keys is None:
            keys = self.optimizer.pareto_metrics  # Default to the first two metrics

        assert len(keys) == 2, "Exactly two metrics must be provided for Pareto front plotting."

        pareto_front = self.cal_pareto_front(keys)
        if pareto_front:
            fig, ax = plt.subplots(figsize=(20, 16))
            ax.scatter([point[keys[0]] for point in pareto_front],
                          [point[keys[1]] for point in pareto_front], color='blue', label='Pareto Front')

            ax.set_xlabel(keys[0])
            ax.set_ylabel(keys[1])
            ax.set_title('Pareto Front')
            ax.legend()
            fig.savefig(os.path.join(self.base_dir, "summary", f"pareto_front_{keys[0]}_vs_{keys[1]}.png"), dpi=300)
            plt.close(fig)
        else:
            print("No Pareto front found. Ensure that trials have been processed and results are available.")



    def cal_pareto_front(self, keys):
        results = []
        for trial in self.trials:
            if trial.processed:
                result_path = os.path.join(trial.base_dir, "result.json")
                if os.path.exists(result_path):
                    with open(result_path, "r") as f:
                        result = json.load(f)
                        results.append({key: result[key] for key in keys})

        # Map directions: only for the keys that are being queried
        direction_map = dict(zip(self.optimizer.metrics_to_optimize,
                                 self.optimizer.metrics_direction))
        directions = [direction_map.get(k, "min") for k in keys]
        pareto_front = calculate_pareto_front(results, keys, directions)
        return pareto_front





if __name__ == "__main__":
    exp = Experiment(
        name="Test Experiment",
        description="This is a test experiment.",
    )
    # exp.run()