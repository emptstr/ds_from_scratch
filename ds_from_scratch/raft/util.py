from ds_from_scratch.sim.core import Environment
from enum import Enum


class RingBufferRandom:

    def __init__(self, seq):
        self.seq = seq
        self.i = 0

    def randint(self, a, b):
        result = self.seq[self.i]
        if self.i < len(self.seq) - 1:
            self.i += 1
        else:
            self.i = 0
        return result


class Executor:

    def __init__(self, executor):
        self.executor = executor
        self.future_by_task = {}

    def submit(self, task):
        self.executor.submit(fn=task.run)

    def schedule(self, task, delay):
        future = self.executor.schedule(fn=task.run, delay=delay)
        self.future_by_task[type(task).__name__] = future

    def cancel(self, task_klass):
        if task_klass.__name__ in self.future_by_task:
            future = self.future_by_task[task_klass.__name__]
            return future.cancel()
        return False


class Logger:
    def __init__(self, address):
        self.address = address

    def info(self, msg):
        print("[{address}] {now} :- {msg}".format(address=self.address, now=self.now(), msg=msg))

    def now(self):
        env = Environment.get_instance()
        return env.now


class Role(Enum):
    CANDIDATE = 0
    LEADER = 1
    FOLLOWER = 2
