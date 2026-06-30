import os.path
import json
from natsort import natsorted
from BaseAgent import BaseAgent



class ExpDesignAgent(BaseAgent):
    def __init__(self, optim_path, metrics_to_optimize, metrics_direction, base_config_path):
        super().__init__()

        self.optim_path = optim_path
        self.metrics_to_optimize = metrics_to_optimize
        self.metrics_direction = metrics_direction
        self.base_config_path = base_config_path

    def acquire_experiment(self):
        summary_base = os.path.join(self.optim_path, "Summary")

        tmp_workdir = os.path.join(self.optim_path, "exp_design_tmp")
        tmp_workdir_trials = os.path.join(tmp_workdir, "trials")

        os.makedirs(tmp_workdir, exist_ok=True)
        os.makedirs(tmp_workdir_trials, exist_ok=True)


        prompt = f"""
这是一个迭代实验优化任务。

实验指导与算法配置说明位于：

{summary_base}

请重点阅读 instruction.md（实验指导与历史实验总结），并结合 logic.md（算法逻辑）、params.md（参数说明）等文件来理解整体上下文。

你的目标不是重新设计整个算法，而是根据已有实验，为下一轮实验生成新的搜索方案。
本轮实验应尽量只验证一个优化分组问题（One Optimization Group Problem），而不是同时验证多个优化分组问题。

请按照下面流程完成。

# Step 1 阅读历史实验

逐个阅读所有 summary。

对于每个实验，总结：

- 实验目标
- 调整了哪些参数
- 哪些参数表现较好
- 哪些参数表现较差
- 哪些参数尚未充分探索

不要重新分析 trial，只依据 summary。

# Step 2 汇总历史实验

结合所有实验：

分析：

- 哪些参数已经比较确定
- 哪些参数值得继续搜索
- 哪些参数需要扩大范围
- 哪些参数需要缩小范围
- 是否存在值得进一步验证的组合

如果证据不足，请明确说明。

不要凭经验猜测算法性质。

# Step 3 设计下一轮实验

目标：

进一步优化

{self.metrics_to_optimize}

优化方向分别是{self.metrics_direction}（max表示越大越好，min表示越小越好）。

尽量逼近 Pareto Front。

实验设计应遵循：

- 优先探索历史最优附近
- 少量探索新的参数区域
- 避免重复已有实验
- 保持实验数量合理
- 每个实验都应说明设计原因
- 既要寻找多目标之间的平衡研究，也要有针对单目标极致性能的研究

如果无法证明某参数有效，则继续探索，而不是固定。
# Step 3.5 实验预算（Experiment Budget）

本轮实验不是最终一轮优化，而是整个迭代优化流程中的一次搜索。

因此，本轮实验应控制实验规模，而不是一次性覆盖全部搜索空间。

请遵循以下原则：

1. 优先设计低维实验

优先进行一维或二维参数搜索。

仅当历史实验已经证明多个参数存在明显耦合关系时，才考虑三维及以上搜索。

不要主动设计高维网格搜索。

2. 控制实验数量

建议的实验规模：

- 一维搜索：约 5 个 trial
- 二维搜索：约 16 个 trial（例如 4x4 ）
- 三维及以上：原则上避免；如果确有必要，应采用随机采样，并控制在较少数量。

不要生成几百甚至上千个 trial。

3. 留有后续优化空间

本轮目标不是找到最终最优参数，而是进一步缩小搜索空间。

对于仍存在不确定性的参数，可以保留到下一轮继续探索，而不是一次性搜索完。

4. 优先局部搜索

对于表现较好的参数区域，进行更细粒度搜索；

对于未知区域，仅进行少量探索。

建议采用：

- 约 60% 的实验用于已有最优附近（exploit）
- 约 40% 的实验用于探索新的区域（explore）

5. 如果预计生成的 trial 数量超过上述规模，请主动调整实验设计，例如：

- 固定部分参数；
- 减少搜索维度；
- 缩小搜索范围；
- 将部分搜索计划推迟到下一轮。


# Step 4 生成实验生成脚本（重点）

不要直接生成大量 config_i.json。

请生成：

generate_trials.py

放置于：

{tmp_workdir}

然后：

运行该脚本，生成config文件（务必确认 {tmp_workdir_trials} 目录中有生成好的config）

脚本负责：

1. 读取基础配置{self.base_config_path}
2. 根据本次实验设计自动生成多个 config_i.json
3. 输出到：

{tmp_workdir_trials}

脚本应：

- 可重复运行
- 参数集中管理
- 易于修改
- 自动创建目录
- 自动命名 config_000.json 等

如果需要，可定义：

PARAM_GRID

或

SEARCH_SPACE

统一管理搜索空间。

尽量避免手写多个 json。

# Step 5 生成实验设计文档

生成：

description.md

放到：

{tmp_workdir}

内容包括：

- 本轮实验目的
- 搜索参数
- 每个参数的搜索范围
- 实验数量
- 为什么这样设计
- 希望验证哪些假设

注意：

这里描述的是实验设计，而不是实验结果。

# Step 5.5 生成实验名称

为了便于后续管理，请生成一个实验名称文件：

{tmp_workdir}/name.txt

要求：

1. 文件中仅包含一行内容，即实验名称，不要包含任何解释或额外文字。

2. 实验名称应能够概括本轮实验主题。

3. 使用英文。

4. 仅允许包含：
   - 大小写字母
   - 数字
   - 下划线（_）

5. 不允许包含：
   - 空格
   - 连字符（-）
   - 中文
   - 其它特殊字符

6. 名称尽量简洁，建议采用：

<Theme>_<SearchType>

例如：

ForwardFT_LocalSearch

或

MergeCuts_GridSearch

或

LongBackwardMP_ThresholdSweep

7. 名称应反映本轮唯一的实验主题，而不是多个主题。
# Step 6 自检

最后检查：

✓ generate_trials.py 是否可以直接运行

✓ 是否能够生成所有 config

✓ config 是否命名规范

✓ 是否遗漏必要参数

✓ 是否与已有实验冲突

如果发现问题，请自动修正。

------

分析原则：

1.

历史实验 > 推测

2.

已有数据支持 > 经验

4.

不要生成重复实验

5.

不要手写大量 config，而应使用脚本批量生成。

开始前，请先制定一个 Plan，再依次完成以上步骤。
        """

        add_dirs = [
            summary_base,
            os.path.dirname(self.base_config_path)
        ]



        self.response(prompt, workdir=tmp_workdir, addition_dirs=add_dirs)



    def acquire_experiment_best(self):
        summary_base = os.path.join(self.optim_path, "Summary")

        tmp_workdir = os.path.join(self.optim_path, "exp_design_tmp")
        tmp_workdir_trials = os.path.join(tmp_workdir, "trials")

        os.makedirs(tmp_workdir, exist_ok=True)
        os.makedirs(tmp_workdir_trials, exist_ok=True)

        prompt = f"""
这是一个实验优化任务。

实验指导与算法配置说明位于：

{summary_base}

请重点阅读 instruction.md（实验指导与历史实验总结），并结合 logic.md（算法逻辑）、params.md（参数说明）等文件来理解整体上下文。

你的目标不是设计下一轮搜索，也不是继续验证假设。

你的目标是：

**基于已有实验形成的全部认知，生成一组最有希望达到当前最佳 Pareto Front 的配置。**

可以认为：

- 当前轮次已经积累了足够实验；
- 你的任务不是获取更多信息，而是利用已有信息；
- 每一个生成的配置，都应该尽可能具有较高成功概率，而不是用于探索未知区域。

整个任务应遵循：

> Best Configuration Synthesis，而不是 Experiment Design。

--------------------------------------------------
Step 1 阅读历史实验
--------------------------------------------------

逐个阅读所有 summary。

对于每个实验，总结：

- 实验目标
- 调整了哪些参数
- 哪些参数明显提升了目标
- 哪些参数明显恶化了目标
- 哪些参数没有明显影响
- 哪些参数之间出现了稳定组合

不要重新分析 trial。

仅依据 summary。

--------------------------------------------------
Step 2 综合全部实验
--------------------------------------------------

结合所有实验，

总结：

哪些结论已经有充分证据支持。

哪些参数：

- 基本已经确定最佳区域
- 存在稳定最优组合
- 存在明显 trade-off
- 对不同目标存在不同最佳值

对于证据不足的部分，应明确指出。

不要根据经验推测算法性质。

只能依据已有实验。

--------------------------------------------------
Step 3 Pareto Front 分析
--------------------------------------------------

优化目标：

{self.metrics_to_optimize}

优化方向：

{self.metrics_direction}

分析：

已有 Pareto Front 具有哪些特点？

哪些配置已经接近 Pareto Front？

还有哪些方向可能进一步改进？

如果多个目标之间存在冲突，

请明确指出：

哪些参数偏向：

- Metric A
- Metric B
- 综合平衡

--------------------------------------------------
Step 4 生成最终配置
--------------------------------------------------

目标：

不是继续探索。

而是：

**生成当前最有希望成为 Pareto Front 的配置集合。**

设计原则：

1.

优先采用历史实验已经证明有效的参数区域。

2.

可以微调已有最佳参数。

例如：

如果历史最优：

threshold=0.30

可以尝试：

0.28
0.29
0.30
0.31
0.32

而不是跳到：

0.6

3.

允许生成多个配置，但每个配置都必须有充分理由。

不要生成明显成功概率较低的探索配置。

4.

允许不同配置分别偏向：

- 极致 Metric A
- 极致 Metric B
- 最佳综合平衡

以形成更好的 Pareto Front。

5.

不同配置之间应具有明确差异。

不要仅修改无关参数。

6.

如果历史已经证明某参数最佳，

应直接固定。

不要为了探索而继续改变。

--------------------------------------------------
Step 5 控制数量
--------------------------------------------------

本轮目标不是覆盖搜索空间。

而是输出：

一组高质量候选。

建议：

5~20 个 config。

数量宁少勿滥。

每个 config 都应该有较高成功概率。

--------------------------------------------------
Step 6 生成 generate_trials.py
--------------------------------------------------

生成：

generate_trials.py

放置：

{tmp_workdir}

脚本负责：

读取：

{self.base_config_path}

自动生成所有 config。

然后：

运行该脚本，生成config文件（务必确认 {tmp_workdir_trials} 目录中有生成好的config）

要求：

- 可重复运行
- 参数统一管理
- 自动创建目录
- 自动命名：

config_000.json

config_001.json

...

不要手写 json。

--------------------------------------------------
Step 7 生成 description.md
--------------------------------------------------

生成：

description.md

放置到：

{tmp_workdir}

内容包括：

1.

历史实验得到的主要结论。

2.

为什么最终选择这些参数。

3.

每个 config 的设计理由。

4.

它预计偏向哪个优化目标。

例如：

- High Accuracy
- High Recall
- Balanced Pareto

5.

为什么认为这些配置最有希望进入 Pareto Front。

--------------------------------------------------
Step 8 生成 name.txt
--------------------------------------------------

生成：

name.txt

仅包含：

一个英文实验名称。

例如：

ParetoCandidate_Final

BalancedFront_Candidates

AccuracyRecall_FinalConfigs

要求：

仅允许：

字母
数字
下划线

--------------------------------------------------
Step 9 自检
--------------------------------------------------

检查：

✓ 是否遗漏参数

✓ generate_trials.py 是否可直接运行

✓ config 是否全部生成

✓ 是否存在重复 config

✓ 每个 config 是否均有明确设计理由

✓ 是否全部基于已有实验，而不是经验猜测

--------------------------------------------------
核心原则
--------------------------------------------------

历史实验 > 推测

已有证据 > 经验

局部最优微调 > 大范围探索

高成功概率 > 信息增益

Pareto Front 最大化 > 搜索空间覆盖

最终输出应代表：

**依据当前所有证据，能够生成的最强候选配置集合，而不是下一轮实验设计。**

不要刻意保持参数多样性。参数多样性不是目标。唯一目标是提高进入 Pareto Front 的概率。如果多个候选最终非常相似，只要它们都具有最高成功概率，也是允许的。

不要为了覆盖搜索空间而生成配置。每一个配置都应像是在有限实验预算下愿意真实运行的高价值候选。宁可少生成，也不要生成低置信度配置。

开始前，请先制定一个 Plan，再依次完成以上步骤。
                """

        add_dirs = [
            summary_base,
            os.path.dirname(self.base_config_path)
        ]

        self.response(prompt, workdir=tmp_workdir, addition_dirs=add_dirs)






    def readout_experiment_design(self):
        tmp_workdir = os.path.join(self.optim_path, "exp_design_tmp")

        name_path = os.path.join(tmp_workdir, "name.txt")
        with open(name_path, "r") as f:
            name = f.read().strip()


        description_path = os.path.join(tmp_workdir, "description.md")
        with open(description_path, "r") as f:
            description = f.read()

        trials_path = os.path.join(tmp_workdir, "trials")
        config_files = natsorted([f for f in os.listdir(trials_path) if f.startswith("config_") and f.endswith(".json")])
        configs = [json.load(open(os.path.join(trials_path, config_file), "r")) for config_file in config_files]


        return name, description, configs

    def del_tmp_workdir(self):
        tmp_workdir = os.path.join(self.optim_path, "exp_design_tmp")
        if os.path.exists(tmp_workdir):
            import shutil
            shutil.rmtree(tmp_workdir)
            print(f"Deleted temporary workdir: {tmp_workdir}")
        else:
            print(f"No temporary workdir found at: {tmp_workdir}")

if __name__ == "__main__":
    agent = ExpDesignAgent(
        optim_path="/home/easonfu/pyproj/UniverseOptimizer/workdir/TestOptimizer",
        metrics_to_optimize=["eff", "effp5", "ghostrate"],
        base_config_path="/home/easonfu/pyproj/UniverseOptimizer/testscripts/config.json"
    )
    # agent.acquire_experiment()

    name, description, configs = agent.readout_experiment_design()
    print(f"Experiment Name: {name}")
    # print(f"Experiment Description: {description}")
    print(f"Number of Configs: {len(configs)}")

    # agent.del_tmp_workdir()