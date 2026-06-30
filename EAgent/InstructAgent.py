import os.path
import json
from BaseAgent import BaseAgent


class InstructAgent(BaseAgent):
    def __init__(self, experiment_paths, optim_path, algorithm_path, metrics_to_optimize, metrics_direction, target_metrics=None):
        super().__init__()

        self.experiment_paths = experiment_paths
        self.optim_path = optim_path
        self.algorithm_path = algorithm_path
        self.metrics_to_optimize = metrics_to_optimize
        self.metrics_direction = metrics_direction
        self.target_metrics = target_metrics





    def instruct(self):
        instruction_path = os.path.join(self.optim_path, "Summary", "instruction.md")
        param_path = os.path.join(self.optim_path, "Summary", "params.md")
        logic_path = os.path.join(self.optim_path, "Summary", "logic.md")
        if not os.path.exists(instruction_path):
            with open(instruction_path, "w") as f:
                f.write("")

        summary_paths = [os.path.join(exp, "summary") for exp in self.experiment_paths if os.path.exists(os.path.join(exp, "summary"))]







        target_metrics_text = ""
        if self.target_metrics:
            target_metrics_text = f"""

5. 目标指标值：
{self.target_metrics}

这些是希望达到的指标目标值（Target Metrics），在更新参数知识和规划下一轮实验时，
需优先关注是否已有参数组合能够满足这些目标值，以及哪些参数是达成目标的关键。
"""

        prompt = f"""
# 任务
请根据以下实验总结，对参数知识库进行持续更新，而不是重新生成。

## 输入资料

1. 参数知识库：
{param_path}

2. 实验总结（按顺序阅读）：
{'\n'.join(summary_paths)}

3. 算法逻辑，应能找到算法源码路径：
{logic_path}

4. 如有需要，可以重新阅读算法源码及参数说明：
{self.algorithm_path}
{target_metrics_text}
---

# 更新原则

请逐个参数进行分析，仅更新已有参数的理解，不要删除任何历史内容！

对于每个参数，请综合{'\n'.join(summary_paths)}的实验结果，补充或修正以下内容：

1. 参数含义
- 参数控制什么
- 在算法中的作用位置
- 默认值及推荐范围（如果能够确定）

2. 参数影响
- 对优化目标的影响方向
- 对收敛速度、稳定性、最终性能等的影响
- 敏感程度

3. 参数之间的关系
- 与哪些参数存在耦合
- 是否存在互相制约
- 是否适合联合优化
- 是否可以单独优化

4. 实验规律
总结所有实验中的表现，包括：
- 一致出现的趋势
- 不同实验中的差异
- 是否存在异常实验
- 是否存在与历史结论矛盾的现象

5. 原因分析
分析为什么会产生上述规律，可以结合：
- 算法原理
- 数学机制
- 实验数据
- optimization logic

如果没有充分证据，请明确说明这是推测，而不是确定结论。

6. 优化建议
总结：
- 推荐取值范围
- 调参顺序
- 与哪些参数一起调节效果最好
- 哪些情况下应提高或降低该参数

---

# 冲突处理

如果新的实验与 param.md 中已有结论冲突：

- 不要删除旧结论；
- 保留历史内容；
- 新增一节 **"新的实验发现"**；
- 明确指出：
    - 冲突内容；
    - 来源于哪个实验（summary 路径）；
    - 为什么认为新的结论更可信（样本更多、实验更充分等）。

---

# 输出要求

直接修改并更新：
{param_path}

要求：

- 保持 Markdown 格式；
- 保留已有内容；
- 新内容追加或插入对应参数下；
- 不要生成新的参数文件；
- 不要输出解释，不要输出分析过程，只更新参数知识库。

完成参数知识更新后，请同步更新：

{instruction_path}

要求：

1. 保留已有内容，不要删除历史记录。
2. 检查当前指导文件中的实验任务：
   - 已经完成的实验，在对应一级或二级标题后追加 **（已完成）** 标记。
   - 如果有实验不需要继续进行，请在对应标题后追加 **（无需尝试）** 标记。
   - 不要修改实验内容，仅增加标记。
3. 如果不存在 **"下一轮实验计划"** 小节，则在文档最后新增；如果已经存在，则更新该小节。
4. 根据目前所有实验结果、参数知识库和算法逻辑，规划下一轮值得开展的实验，包括但不限于：
   - 尚未充分探索的参数范围；
   - 参数之间的组合实验；
   - 用于验证已有结论的对照实验；
   - 针对异常结果的复现实验；
   - 用于验证理论推测的实验；
   - 可能带来进一步性能提升的新实验。
   - 保持未完成的总建议数量在最多5个左右
5. 每个实验建议应包含：
   - 实验目的；
   - 修改哪些参数；
   - 推荐的参数范围；
   - 希望验证的假设；
   - 预期观察指标。
6. 按照信息增益和优先级排序，使后续实验尽可能减少无效搜索、提高知识积累效率。
        """


        add_dirs = [
            os.path.join(self.optim_path, "Summary"),
            *summary_paths,
        ]

        self.response(prompt, workdir=os.path.dirname(instruction_path), addition_dirs=add_dirs)







if __name__ == "__main__":
    agent = InstructAgent(
        experiment_paths=[
            "/home/easonfu/pyproj/UniverseOptimizer/workdir/LongTrackOptimizer_v3/Experiments/Exp_1_DefaultExperiment",
            "/home/easonfu/pyproj/UniverseOptimizer/workdir/LongTrackOptimizer_v3/Experiments/Exp_2_MPForward_LocalSearch",
            "/home/easonfu/pyproj/UniverseOptimizer/workdir/LongTrackOptimizer_v3/Experiments/Exp_3_FTForward_LocalSearch",
        ],
        optim_path="/home/easonfu/pyproj/UniverseOptimizer/workdir/LongTrackOptimizer_v3",
        algorithm_path="/home/easonfu/Software/260613_Moore/stack",
        metrics_to_optimize=["eff", "effp5", "ghostrate"],
        metrics_direction=["max", "max", "min"]
    )
    agent.instruct()