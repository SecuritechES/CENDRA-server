timeout = 3

__code_dump_stack__ = """
import sys, traceback

for thread, frame in sys._current_frames().items():
    print('Thread 0x%x' % thread)
    traceback.print_stack(frame)
    print()
"""

def dump_stack_for_process(pid):
    import pyrasite

    ipc = pyrasite.PyrasiteIPC(pid)
    ipc.connect()
    print(ipc.cmd(__code_dump_stack__))
    ipc.close()

def worker_abort(worker):
    pid = worker.pid
    print("worker is being killed - {}".format(pid))
    dump_stack_for_process(pid)