import numpy as np




def run_haha_job():
    print("Running haha job...")
    # Simulate some work
    import time
    for i in range(10):
        re = []
        for i in range(100):
            re.extend(np.random.rand(500_000).tolist())
            # time.sleep(0.1)  # Simulate time-consuming work

    print("Haha job done!")