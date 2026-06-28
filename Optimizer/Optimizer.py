from utils import *
from ExpManager.Trial import Trial
from ExpManager.Experiment import Experiment


class Optimizer:
    def __init__(self, name, script_path, default_config, metrics_to_optimize, algorithm_path=None):
        self.name = name


        self.script_path = script_path
        self.default_config = default_config
        self.metrics_to_optimize = metrics_to_optimize
        self.processor = 1

        self.base_dir = os.path.join(workdir_path, self.name)
        self.algorithm_path = algorithm_path


        self.create_folder_structure()

        self.Experiments = []  # List to hold experiments associated with this optimizer

    def create_folder_structure(self):
        paths = [
            os.path.join(self.base_dir, "Experiments"),
            os.path.join(self.base_dir, "Summary"),
        ]

        for path in paths:
            os.makedirs(path, exist_ok=True)
            print(f"Created folder: {path}")

    def acquire_experiment(self):
        name = "TestExperiment"
        description = "This is a test experiment."
        configs = [
            {"param1": 0.1, "param2": 0.5},
            {"param1": 0.2, "param2": 0.6},
            {"param1": 0.3, "param2": 0.7},
        ]

        return name, description, configs

    def start_optimize(self):
        init_exp = self.init_default_experiment()
        init_exp.run_all_trials()








    def init_default_experiment(self):
        name = "DefaultExperiment"
        description = "This is the default experiment."
        configs = [self.default_config]
        init_exp = self.create_experiment(name, description, configs)
        return init_exp


    def create_experiment(self, name, description, configs):
        experiment = Experiment(name, description, self)
        experiment.create_folder_structure()

        for config in configs:
            experiment.add_trial(config=config, index=experiment.get_n_trials())

        self.Experiments.append(experiment)


        return experiment

    def learning_algorithm(self):
        if not self.algorithm_path:
            print("No learning algorithm path provided.")
            return



    def update_learning_algorithm(self):
        pass


if __name__ == "__main__":

    import json
    with open("/home/easonfu/pyproj/UniverseOptimizer/testscripts/config.json", "r") as f:
        default_config = json.load(f)

    optimizer = Optimizer(
        name="TestOptimizer",
        script_path="/home/easonfu/pyproj/UniverseOptimizer/testscripts/run",
        default_config=default_config,
        metrics_to_optimize=["Eff", "Ghost"]
    )

    optimizer.start_optimize()




