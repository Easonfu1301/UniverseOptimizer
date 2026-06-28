import os
import json
from JobRunner.JobRunner import JobRunner







class Trial:
    def __init__(self, name, config, experiment):
        self.name = name
        self.config = config
        self.experiment = experiment
        self.optimizer = experiment.optimizer

        self.base_dir = os.path.join(experiment.base_dir, "trials", self.name)

    def __str__(self):
        return f"Trial(name={self.name}, config={self.config})"

    def create_folder_structure(self):
        os.makedirs(self.base_dir, exist_ok=True)
        print(f"Created folder: {self.base_dir}")

    def submit_job(self, script, task_type):
        job_runner = JobRunner(script=script, workdir=self.base_dir, task_type=task_type)
        self.optimizer.task_pool.submit_task(script_path=script, workdir=self.base_dir, task_type=task_type)
        print(f"Submitted job for trial: {self.name}")


    def dump_config(self):
        config_path = os.path.join(self.base_dir, "config.json")
        with open(config_path, "w") as f:
            json.dump(self.config, f, indent=4)
        print(f"Dumped config to: {config_path}")

    def dump_description(self):
        description_path = os.path.join(self.base_dir, "description.txt")
        with open(description_path, "w") as f:
            f.write(f"Trial Name: {self.name}\n")
            f.write(f"Trial Config: {self.config}\n")
        print(f"Dumped description to: {description_path}")




if __name__ == "__main__":
    trial = Trial(name="Test Trial", config={"param1": 10, "param2": 20})
    print(f"Trial Name: {trial.name}")
    print(f"Trial Config: {trial.config}")









