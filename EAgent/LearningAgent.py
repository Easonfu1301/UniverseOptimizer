import os.path

from BaseAgent import BaseAgent


class LearningAgent(BaseAgent):
    def __init__(self, workdir, script_path, default_config, metrics_to_optimize, algorithm_path):
        super().__init__()

        self.workdir = workdir
        self.script_path = script_path
        self.default_config = default_config
        self.metrics_to_optimize = metrics_to_optimize
        self.algorithm_path = algorithm_path

    def learn(self):
        prompt = f"""
你将看到一个算法，由{self.script_path}的脚本所运行，它的默认配置是{self.default_config}，它的优化指标是{self.metrics_to_optimize}。
你需要根据这些信息，你需要做以下事情：
1. 请根据运行脚本，找到实际运行的算法链，排除没有用到的部分，知道算法之间的调用关系和数据流向
2. 了解最终的优化目标是如何定义和计算的。
3. 了解定义的参数({self.default_config.keys()})是如何影响优化目标的，为每一个参数生成一个总结
4. 对参数进行分组，将参数尽可能的分为可以独立优化的组，每一组参数的优化目标是独立的，尽可能的减少参数之间的耦合
5. 一步步的描述算法的运行过程
最后，你需要在{self.workdir}中生成尽可能详细的几个md文件，分别是：
1. 一个总结文件，包含算法的运行过程和优化目标的定义和计算方法，文件名为logic.md
2. 一个参数总结文件，包含每一个参数的总结，文件名为params.md，每一个参数为一个小节，包含参数可能如何影响最终的优化目标，参数的默认值，参数的取值范围，参数的影响因素，参数的优化方法等，
同时，在最后，你需要对参数进行分组，将参数尽可能的分为可以独立优化的组，组与组之间对于最终优化目标的影响应该尽量是独立的，尽可能的减少参数之间的耦合，并解释原因

做之前先plan一下
        """

        add_dirs = [
            os.path.dirname(self.script_path),
            os.path.dirname(self.algorithm_path),
        ]

        self.response(prompt, workdir=self.workdir, addition_dirs=add_dirs)


if __name__ == "__main__":
    agent = LearningAgent(
        workdir="/home/easonfu/pyproj/UniverseOptimizer/workdir/TestOptimizer/Summary",
        script_path="./example_script.py",
        default_config={"param1": 0.1, "param2": 0.5},
        metrics_to_optimize=["accuracy", "loss"],
        algorithm_path="./example_algorithm.py"
    )
    agent.learn()
