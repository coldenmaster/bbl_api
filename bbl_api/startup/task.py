
from threading import Thread
import time
from bbl_api.api01.iot_api import esp_test_task_5s
from bbl_api.utils_pure import print_red


def run_thread_task():
    task = sec_cycle
    print_red(f"bbl_api task run_thread_task: {task}")
    Thread(target=task).start()

def sec_cycle():
    cnt = 0
    while(True):
        # print_red(f" 5 sec cycle: {cnt}")
        if cnt % 5 == 0:   
            esp_test_task_5s()
            pass
        if cnt % 10 == 0:   
            # print_red(f" 10 sec cycle: {time.time()} / {time.ctime()}")
            pass
        if cnt % 30 == 0:
            pass
        cnt += 1
        time.sleep(1)

# run_thread_task()