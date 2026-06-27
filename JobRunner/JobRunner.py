from multiprocessing import Process
import subprocess
from pathlib import Path
import os
import psutil
import time
import threading
from utils.funny_test import run_haha_job

from FUCKROOT import HEP_PLOT
import matplotlib.pyplot as plt

from utils import workdir_path
import numpy as np

class JobRunner:
    def __init__(self, script, workdir, task_type):
        self.script = script
        self.workdir = workdir
        self.task_type = task_type



        self.running = False
        self.processed = False
        self.succeed = False


        self.proc = None

        self.memory_monitor = []



    def create_process(self):
        if self.task_type == "shell":
            self.run_shell_script()
        elif self.task_type == "function":
            self.run_func()
        else:
            raise ValueError(f"Unsupported task type: {self.task_type}")

    def run_shell_script(self):

        try:
            self.proc = subprocess.Popen(
                f"source {self.script} && touch FLAG_DONE",
                cwd=self.workdir,
            )
            self.running = True
            self.processed = False
            self.succeed = False

        except Exception as e:
            print(f"Error running shell script: {e}")
            self.running = False
            self.processed = True
            self.succeed = False
            return

    def run_func(self):

        def _worker():
            os.chdir(self.workdir)
            self.script()
            Path(self.workdir).joinpath("FLAG_DONE").touch()

        try:
            self.proc = Process(target=_worker, daemon=True)
            self.proc.start()
            self.running = True
            self.processed = False
            self.succeed = False


        except Exception as e:
            print(f"Error running function: {e}")
            self.running = False
            self.processed = True
            self.succeed = False
            return

    def check_status(self):

        def _check():
            while self.running:
                if self.proc is None:
                    print("Process is not running.")
                    self.running = False
                    self.processed = True
                    self.succeed = False
                    break

                if self.task_type == "shell":
                    if self.proc.poll() is not None:  # Process has finished
                        self.running = False
                        self.processed = True
                        self.succeed = (self.proc.returncode == 0)
                        break

                elif self.task_type == "function":
                    if not self.proc.is_alive():  # Process has finished
                        self.running = False
                        self.processed = True
                        self.succeed = True  # Assuming function runs successfully if it finishes
                        break

                else:
                    print(f"Unsupported task type for status check: {self.task_type}")
                    self.running = False
                    self.processed = True
                    self.succeed = False
                    break

                time.sleep(1)  # Check every second

        self.status_checker = threading.Thread(target=_check, daemon=True)
        self.status_checker.start()

    def memory_monitoring(self, interval=1.0):
        def _monitor():


            if self.proc is None or not self.running:
                print("Process is not running. Cannot monitor memory.")
                return

            if self.task_type not in ["shell", "function"]:
                print(f"Unsupported task type for memory monitoring: {self.task_type}")
                return

            if self.task_type == "shell":
                proc = psutil.Process(self.proc.pid)
            elif self.task_type == "function":
                proc = psutil.Process(self.proc.pid)
            else:
                raise ValueError(f"Unsupported task type for memory monitoring: {self.task_type}")

            while self.running:
                try:
                    mem_info = proc.memory_info()
                    timestamp = time.time()
                    self.memory_monitor.append((timestamp, mem_info.rss))  # Store timestamp and memory usage in bytes
                    # print(f"Memory usage at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))}: {mem_info.rss / (1024 * 1024):.2f} MB")
                except psutil.NoSuchProcess:
                    print("Process has terminated.")
                    break
                except Exception as e:
                    print(f"Error monitoring memory: {e}")
                    break

                time.sleep(interval)

        self.memory_monitor_thread = threading.Thread(target=_monitor, daemon=True)
        self.memory_monitor_thread.start()

    def plot_memory_usage(self):

        if not self.memory_monitor:
            print("No memory usage data to plot.")
            return

        timestamps, memory_usage = zip(*self.memory_monitor)
        timestamps = [ts - timestamps[0] for ts in timestamps]
        memory_usage_mb = [mem / (1024 * 1024) for mem in memory_usage]  # Convert to MB

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(timestamps, memory_usage_mb, marker='o')
        ax.set_title("Memory Usage Over Time")
        ax.set_xlabel("Timestamp")
        ax.set_ylabel("Memory Usage (MB)")
        ax.grid()
        plt.tight_layout()
        plt.show()




if __name__ == "__main__":
    job_runner = JobRunner(script=run_haha_job, workdir=workdir_path, task_type="function")
    job_runner.create_process()
    job_runner.check_status()
    job_runner.memory_monitoring(interval=0.1)

    print("Job started. Waiting for completion...")

    time.sleep(20)  # Wait for some time to let the job run and memory monitoring to collect data

    job_runner.plot_memory_usage()  # Call the plotting function to visualize memory usage
