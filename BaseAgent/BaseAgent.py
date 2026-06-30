from utils import *
import subprocess
import sys


try:
    from init import *
except ImportError:
    from .init import *

class BaseAgent:
    def __init__(self):
        self.config = load_agent_config()

    def __str__(self):
        return f"BaseAgent(config={self.config})"

    def _make_env(self):
        """构造带共享配置的环境变量副本"""
        env = os.environ.copy()
        env.update(self.config)
        return env

    def response(self, prompt, workdir='.', addition_dirs=None):
        cmd = [
            "copilot",
            "-C", workdir,
        ]

        if addition_dirs:
            for add_dir in addition_dirs:
                cmd.extend(["--add-dir", f"{add_dir}"])

        cmd.extend([
            "-p", prompt,
            # "--log-level", "debug",
            "--reasoning-effort", self.config.get("THINKING_EFFORT", "high"),
            "--allow-all-tools"
        ])

        env = self._make_env()
        process = subprocess.Popen(
            cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # 同步逐行读取 stdout 实现流式打印
        for line in process.stdout:
            print(line, end='', flush=True)

        process.wait()
        stderr = process.stderr.read()
        if stderr:
            print(stderr, file=sys.stderr, flush=True)
        







if __name__ == "__main__":
    agent = BaseAgent()
    print("BaseAgent initialized successfully.")

    agent.response("hello! 计算一下1+1")


