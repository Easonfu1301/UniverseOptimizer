from JobRunner.JobRunner import JobRunner
import threading
import numpy as np
import time

from utils.funny_test import run_haha_job


class TaskPool:
    def __init__(self, max_workers=1):
        self.max_workers = max_workers
        self.jobs = []

        self.running_status = []
        self.processed_jobs = []
        self.succeed_jobs = []

    def start_pool(self):
        mon_thread = threading.Thread(target=self.monitor_status_thread)
        mon_thread.start()



    def monitor_status_thread(self):
        while True:
            self.running_status = [job.running for job in self.jobs]
            self.processed_jobs = [job.processed for job in self.jobs]
            self.succeed_jobs = [job.succeed for job in self.jobs]

            print(
                f"Total Jobs: {len(self.jobs)}, "
                f"Running Status: {np.sum(self.running_status)}, "
                f"Processed Jobs: {np.sum(self.processed_jobs)}, "
                f"Succeed Jobs: {np.sum(self.succeed_jobs)}"
            )
            if np.sum(self.running_status) < self.max_workers:
                for job in self.jobs:
                    if not job.running and not job.processed:
                        job.create_process()
                        job.check_status()
                        break

            time.sleep(1)  # Sleep for a while before checking again





    def submit_task(self, job_runner):
        with threading.Lock():
            # job_runner = JobRunner(script=script_path, workdir=workdir, task_type=task_type)
            self.jobs.append(job_runner)


if __name__ == "__main__":
    task_pool = TaskPool(max_workers=2)
    task_pool.start_pool()


    print(1)



    for i in range(3):
        print(f"Submitting task {i + 1}")
        script_path = f"/home/easonfu/pyproj/UniverseOptimizer/testscripts/run"
        workdir = f"/home/easonfu/pyproj/UniverseOptimizer/workdir/TestOptimizer/Experiments/Exp_DefaultExperiment/trials/Trial_{i}"
        task_pool.submit_task(script_path=script_path, workdir=workdir, task_type="shell")
        time.sleep(2)


    time.sleep(30)

    for i in range(3):
        print(f"Submitting task {i + 1}")
        script_path = f"/home/easonfu/pyproj/UniverseOptimizer/testscripts/run"
        workdir = f"/home/easonfu/pyproj/UniverseOptimizer/workdir/TestOptimizer/Experiments/Exp_DefaultExperiment/trials/Trial_{i}"
        task_pool.submit_task(script_path=script_path, workdir=workdir, task_type="shell")
        time.sleep(2)