import os.path
import json
from BaseAgent import BaseAgent


class ParamCheckerAgent(BaseAgent):
    def __init__(self, workdir, script_path, default_config, metrics_to_optimize, metrics_direction, algorithm_path):
        super().__init__()

        self.workdir = workdir
        self.script_path = script_path
        self.default_config = default_config
        self.metrics_to_optimize = metrics_to_optimize
        self.metrics_direction = metrics_direction
        self.algorithm_path = algorithm_path

    def check(self):
        prompt = f"""
你将看到一个算法，由{self.script_path}的脚本所运行，它的默认配置是{self.default_config}，它的优化指标是{self.metrics_to_optimize}，优化方向分别是{self.metrics_direction}（max表示越大越好，min表示越小越好）。
你需要根据这些信息，你需要做以下事情：
1. 检查这些参数是否正确的传入到对应的算法中。
2. 检查这些参数是否在算法中已经存在
完成后，请写一个param_check.json到{self.workdir}，内容是一个字典，包含以下键值对：
- "param_name": true 或 false，表示检查是否成功。

做之前先plan一下
        """

        add_dirs = [
            os.path.dirname(self.script_path),
            os.path.dirname(self.algorithm_path),
        ]

        self.response(prompt, workdir=self.workdir, addition_dirs=add_dirs)

        self.print_false_params()

    def print_false_params(self):
        param_check_path = os.path.join(self.workdir, "param_check.json")
        if not os.path.exists(param_check_path):
            print(f"param_check.json not found in {self.workdir}")
            return

        with open(param_check_path, "r") as f:
            param_check = json.load(f)

        false_params = [param for param, status in param_check.items() if not status]
        if false_params:
            print("Parameters that failed the check:")
            for param in false_params:
                print(f"- {param}")
        else:
            print("All parameters passed the check.")

    def all_pass(self):
        param_check_path = os.path.join(self.workdir, "param_check.json")
        if not os.path.exists(param_check_path):
            print(f"param_check.json not found in {self.workdir}")
            return False

        with open(param_check_path, "r") as f:
            param_check = json.load(f)

        return all(status for status in param_check.values())

if __name__ == "__main__":
    agent = ParamCheckerAgent(
        workdir="/home/easonfu/pyproj/UniverseOptimizer/workdir/TestOptimizer/Summary",
        script_path="./example_script.py",
        default_config={"param1": 0.1, "param2": 0.5},
        metrics_to_optimize=["accuracy", "loss"],
        algorithm_path="./example_algorithm.py"
    )
    agent.learn()
