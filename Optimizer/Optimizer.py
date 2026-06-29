from utils import *
from ExpManager.Trial import Trial
from ExpManager.Experiment import Experiment
from TaskPool.TaskPool import TaskPool
from EAgent.ParamCheckerAgent import ParamCheckerAgent
from EAgent.LearningAgent import LearningAgent
from EAgent.ExpDesignAgent import ExpDesignAgent
import time

import matplotlib
matplotlib.use('Agg')

from FUCKROOT import HEP_PLOT
import matplotlib.pyplot as plt


class Optimizer:
    def __init__(self, name, script_path, config_path, metrics_to_optimize, metrics_direction, algorithm_path=None):
        self.all_pass = None
        self.name = name

        self.script_path = script_path

        self.default_config_path = config_path
        with open(self.default_config_path, "r") as f:
            self.default_config = json.load(f)

        self.metrics_to_optimize = metrics_to_optimize
        self.metrics_direction = metrics_direction

        self.processor = 10
        self.task_pool = TaskPool(max_workers=self.processor)

        self.base_dir = os.path.join(workdir_path, self.name)
        self.algorithm_path = algorithm_path

        self.create_folder_structure()

        self.Experiments = []  # List to hold experiments associated with this optimizer
        self.wait_FALG = False

    def create_folder_structure(self):
        paths = [
            os.path.join(self.base_dir, "Experiments"),
            os.path.join(self.base_dir, "Summary"),
        ]

        for path in paths:
            os.makedirs(path, exist_ok=True)
            print(f"Created folder: {path}")

    def set_pareto_metrics(self, keys):
        self.pareto_metrics = keys


    def acquire_experiment(self):
        agent = ExpDesignAgent(
            optim_path=self.base_dir,
            metrics_to_optimize=self.metrics_to_optimize,
            metrics_direction=self.metrics_direction,
            base_config_path=self.default_config_path
        )

        if len(self.Experiments) % 5 == 0:
            agent.acquire_experiment_best()
        else:
            agent.acquire_experiment()

        name, description, configs = agent.readout_experiment_design()
        print(f"Experiment Name: {name}")
        # print(f"Experiment Description: {description}")
        print(f"Number of Configs: {len(configs)}")

        agent.del_tmp_workdir()

        return name, description, configs

    def start_optimize(self):

        self.task_pool.start_pool()

        init_exp = self.init_default_experiment()
        init_exp.run_all_trials()

        self.learning_algorithm()

        self.wait_FALG = True
        self.wait_or_continue()
        self.plot_all_exp_pareto_fronts()

        while True:
            name, description, configs = self.acquire_experiment()
            name = f"{len(self.Experiments) + 1}_{name}"
            new_exp = self.create_experiment(name, description, configs)
            new_exp.run_all_trials()

            # self.learning_algorithm()

            self.wait_FALG = True
            self.wait_or_continue()
            self.plot_all_exp_pareto_fronts()

    def wait_or_continue(self):
        while self.wait_FALG and not self.complete_all_experiments():
            # print(self.wait_FALG, [exp.all_complete for exp in self.Experiments])
            print("Waiting for all trials to complete...")
            time.sleep(5)

        self.wait_FALG = False

    def complete_all_experiments(self):
        return all([exp.all_complete for exp in self.Experiments])

    def init_default_experiment(self):
        name = "1_DefaultExperiment"
        description = "Experiment to test the default configuration."
        configs = [self.default_config for i in range(1)]
        init_exp = self.create_experiment(name, description, configs)
        return init_exp

    def create_experiment(self, name, description, configs):
        experiment = Experiment(name, description, self)

        for config in configs:
            experiment.add_trial(config=config, index=experiment.get_n_trials())

        self.Experiments.append(experiment)

        return experiment

    def check_parameter(self):
        if not self.algorithm_path:
            print("No learning algorithm path provided.")
            return

        param_checker = ParamCheckerAgent(
            workdir=os.path.join(self.base_dir, "Summary"),
            script_path=self.script_path,
            default_config=self.default_config,
            metrics_to_optimize=self.metrics_to_optimize,
            metrics_direction=self.metrics_direction,
            algorithm_path=self.algorithm_path
        )
        param_checker.check()
        self.all_pass = param_checker.all_pass()

    def learning_algorithm(self):
        if not self.algorithm_path:
            print("No learning algorithm path provided.")
            return

        algo_learner = LearningAgent(
            workdir=os.path.join(self.base_dir, "Summary"),
            script_path=self.script_path,
            default_config=self.default_config,
            metrics_to_optimize=self.metrics_to_optimize,
            metrics_direction=self.metrics_direction,
            algorithm_path=self.algorithm_path
        )
        algo_learner.learn()

    def update_learning_algorithm(self):
        pass


    def plot_all_exp_pareto_fronts(self):
        assert len(self.pareto_metrics) == 2, "Exactly two metrics must be provided for Pareto front plotting."
        fig, ax = plt.subplots(figsize=(20, 16))
        x_metric, y_metric = self.pareto_metrics

        for exp in self.Experiments:
            pareto_front = exp.cal_pareto_front(self.pareto_metrics)
            if pareto_front:
                xs = [p[x_metric] for p in pareto_front]
                ys = [p[y_metric] for p in pareto_front]
                ax.scatter(xs, ys, label=f"Experiment {exp.name}")
        ax.set_xlabel(x_metric)
        ax.set_ylabel(y_metric)
        ax.set_title(f"Pareto Fronts for {x_metric} vs {y_metric}")
        ax.legend()

        fig.savefig(os.path.join(self.base_dir, "Summary", f"pareto_front_{x_metric}_vs_{y_metric}.png"), dpi=300)
        plt.close(fig)
        plt.close(fig)



if __name__ == "__main__":

    import json

    optimizer = Optimizer(
        name="LongTrackOptimizer_v2",
        script_path="/home/easonfu/pyproj/UniverseOptimizer/testscripts/run",
        config_path="/home/easonfu/pyproj/UniverseOptimizer/testscripts/config.json",
        metrics_to_optimize=["eff", "effp5", "ghostrate"],
        metrics_direction=["max", "max", "min"],
        algorithm_path="/home/easonfu/Software/260613_Moore/stack"
    )

    optimizer.set_pareto_metrics(["eff", "ghostrate"])

    optimizer.check_parameter()
    if optimizer.all_pass:
        print("All parameters passed the check. Starting optimization...")
        optimizer.start_optimize()

    # optimizer.start_optimize()
