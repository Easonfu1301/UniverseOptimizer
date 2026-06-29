import os.path
import json
from BaseAgent import BaseAgent


class SummaryAgent(BaseAgent):
    def __init__(self, exp_path, optim_path, metrics_to_optimize, metrics_direction):
        super().__init__()

        self.exp_path = exp_path
        self.optim_path = optim_path
        self.metrics_to_optimize = metrics_to_optimize
        self.metrics_direction = metrics_direction

    def generate_summary(self):
        description_path = os.path.join(self.exp_path, "description", "description.txt")
        analysis_path = os.path.join(self.exp_path, "ana_scripts")
        logic_path = os.path.join(self.optim_path, "Summary", "logic.md")
        params = os.path.join(self.optim_path, "Summary", "params.md")

        summary_path = os.path.join(self.exp_path, "summary")


        with open(description_path, "r") as f:
            description = f.read()

        prompt = f"""
这是一组实验。

实验描述：
----------------
{description}
----------------

实验结果位于：
{self.exp_path}
每个 trial 目录下包含 result.json。

另外可以参考：
- 实验逻辑：{logic_path}
- 参数说明：{params}

请完成实验总结，并生成 summary.md 到：
{summary_path}

要求如下：

## 1. 阅读所有 trial

统计所有 trial 的配置和结果。

重点关注：
- 不同参数组合
- {self.metrics_to_optimize} 的变化（优化方向：{self.metrics_direction}，max表示越大越好，min表示越小越好）
- 是否存在明显趋势

## 2. 总结实验事实（最重要）

总结必须**优先依据 trial 中直接观察到的数据**。

例如：

✓ 可以写：

- 当 learning_rate 从 A 调整到 B 时，metric 从 xx 提高到 yy。
- 在保持其他参数基本一致时，batch_size=32 的结果优于 batch_size=16。
- 多数最优结果出现在 xxx 参数附近。

✗ 不要写：

- learning rate 提高了模型泛化能力
- 说明模型收敛更加稳定
- 参数之间存在协同作用

除非 trial 数据能够直接证明，否则不要推断原因。

如果无法判断，请明确写：

"根据现有实验无法判断。"

## 3. 参数影响分析

结合 params.md 和 logic.md：

对于每个重要参数：

- 哪些 trial 修改了该参数
- metric 如何变化
- 是否能观察到明显趋势
- 是否证据不足

请区分：

### 已观察到

直接来自实验结果。

### 推测

只有在确实需要时才写，并明确标注：

> 推测：

且推测内容不要作为实验结论。

## 4. 总结实验结论

总结：

- 当前最优配置
- 最优 metric
- 哪些参数影响较明显
- 哪些参数尚不能得出结论

结论必须能够由实验结果支持。

## 5. 是否需要进一步分析

如果仅查看 result.json 无法回答上述问题，可以：

在：
{analysis_path}

生成分析脚本，例如：

- 汇总所有 trial
- 绘制参数 vs metric
- 排序结果
- 绘制趋势图

仅在确有必要时生成脚本，不要为了生成而生成，若生成，尽量把能表明结论的图表保存到{analysis_path}。

## 输出要求

summary.md 应尽量详细。

重点描述：

- 实验事实
- 数据支持的趋势
- 参数影响

不要过度分析，不要猜测实验原因，不要编造结论。

当证据不足时，明确说明：

"现有实验不足以支持该结论。"
        """


        add_dirs = [
            self.exp_path,
            self.optim_path
        ]

        self.response(prompt, workdir=summary_path, addition_dirs=add_dirs)







if __name__ == "__main__":
    agent = SummaryAgent(
        exp_path="/home/easonfu/pyproj/UniverseOptimizer/workdir/TestOptimizer/Experiments/Exp_DefaultExperiment",
        optim_path="/home/easonfu/pyproj/UniverseOptimizer/workdir/TestOptimizer",
        metrics_to_optimize=["eff", "effp5", "ghostrate"]
    )
    agent.generate_summary()