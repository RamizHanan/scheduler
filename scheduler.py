import copy
from task import Task
from itertools import groupby


class Scheduler(object):

    def __init__(self, task_count: int, exec_time: int, ap1188: int, ap918: int,
                 ap648: int, ap384: int, apidle: int, sch_type: str, ee: bool):
        self.task_count = int(task_count)
        self.exec_time = int(exec_time)
        self.ap1188 = int(ap1188) * 0.001
        self.ap918 = int(ap918) * 0.001
        self.ap648 = int(ap648) * 0.001
        self.ap384 = int(ap384) * 0.001
        self.apidle = int(apidle) * 0.001
        self.sch_type = sch_type
        self.ee = ee

    def schedule(self, tasks):
        for task in tasks:
            task.ap = self.ap1188
        timing_list = None
        if self.sch_type.lower() == 'edf' and self.ee is False:
            timing_list = self.EDF(tasks)
        elif self.sch_type.lower() == 'rm' and self.ee is False:
            timing_list = self.RM(tasks)
        elif self.sch_type.lower() == 'edf' and self.ee is True:
            timing_list = self.EDF_EE(tasks)
        elif self.sch_type.lower() == 'rm' and self.ee is True:
            timing_list = self.RM_EE(tasks)
        return timing_list

    def EDF(self, tasks):
        pass

    def RM(self, tasks):
        # Create empty timing list
        timing_list = [None] * int(self.exec_time)
        # Sort tasks by deadline
        tasks = sorted(iter(tasks), key=lambda task: task.deadline)
        # for task in tasks:
        #     print(task)

        for task in tasks:
            exec_time = copy.deepcopy(task.wcet)
            # Construct deadlines list for Task
            x = 1
            count = 0
            while(x < self.exec_time):
                count = count + 1
                x = x + (task.deadline)

            times = [1] + [x * task.deadline for x in range(1, count)]
            deadlines = []
            for i in range(len(times)):
                try:
                    if times[i + 1] < self.exec_time:
                        deadlines.append((times[i], times[i + 1]))
                except IndexError:
                    if times[i] < self.exec_time:
                        deadlines.append((times[i], self.exec_time))
            # Schedule task
            for start, end in deadlines:
                pos = start - 1
                exec_time = copy.deepcopy(task.wcet)
                while(exec_time > 0 and pos < self.exec_time):
                    if timing_list[pos] is None:
                        timing_list[pos] = task
                        exec_time -= 1
                    pos += 1
                    # If deadline is missed, return empty list
                    if pos > end:
                        return []
        # Construct output
        res = []
        start = 1
        for key, group in groupby(timing_list):
            burst_length = len(list(group))
            end = start + burst_length - 1

            if isinstance(key, Task):
                res.append((start, key.name, '1188', end, round(burst_length * key.ap, 3)))
            else:
                res.append((start, 'IDLE', 'IDLE', end, round(burst_length * self.apidle, 3)))
            start = end + 1
        return res

    def EDF_EE(self, tasks):
        pass

    def RM_EE(self, tasks):
        print(self.calc_rm(tasks))
        s = []
        tasks = sorted(iter(tasks), key=lambda task: (self.get_next(task)[0] - task.wcet) / task.deadline)
        while(self.calc_rm(tasks)):
            tasks[0].wcet, tasks[0].ap = self.get_next(tasks[0])
            tasks = sorted(iter(tasks), key=lambda task: (self.get_next(task)[0] - task.wcet) / task.deadline)
        s = self.RM(tasks)
        for task in tasks:
            print('{} {}'.format(task.name, task.ap))
        return s

    def calc_rm(self, tasks):
        right = round(self.task_count * (2**(1 / self.task_count) - 1), 4)
        left = 0
        for task in tasks:
            left += task.wcet / task.deadline
        return left <= right

    def get_next(self, task):
        d = {task.wcet1188: (task.wcet918, self.ap918), task.wcet918: (
            task.wcet648, self.ap648), task.wcet648: (task.wcet384, self.ap384)}
        return d[task.wcet]

    def __str__(self):
        return "Scheduler: {} {} {} {} {} {} {} ({} {})".format(self.task_count, self.exec_time, self.ap1188,
                                                                self.ap918, self.ap648, self.ap384, self.apidle,
                                                                self.sch_type, self.ee)
