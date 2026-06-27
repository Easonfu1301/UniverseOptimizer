import os
import json








class Trial:
    def __init__(self, name, config, experiment):
        self.name = name
        self.config = config
        self.experiment = experiment

        self.base_dir = os.path.join(experiment.base_dir, "trials", self.name)

    def __str__(self):
        return f"Trial(name={self.name}, config={self.config})"

    def create_folder_structure(self):
        os.makedirs(self.base_dir, exist_ok=True)
        print(f"Created folder: {self.base_dir}")

    def dump_config(self):
        config_path = os.path.join(self.base_dir, "config.json")
        with open(config_path, "w") as f:
            json.dump(self.config, f, indent=4)
        print(f"Dumped config to: {config_path}")




if __name__ == "__main__":
    trial = Trial(name="Test Trial", config={"param1": 10, "param2": 20})
    print(f"Trial Name: {trial.name}")
    print(f"Trial Config: {trial.config}")









