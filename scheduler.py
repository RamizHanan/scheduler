import copy
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
        timing_list = None
        if self.sch_type.lower() == 'edf' and self.ee is False:
            timing_list = self.EDF(tasks)
        elif self.sch_type.lower() == 'rm' and self.ee is False:
            timing_list = self.RM(tasks)
        elif self.sch_type.lower() == 'edf' and self.ee is True:
            timing_list = self.EDF_EE()
        elif self.sch_type.lower() == 'rm' and self.ee is True:
            timing_list = self.RM_EE()
        return timing_list

    def EDF(self, tasks):
        pass

    def RM(self, tasks):
        # Create empty timing list
        timing_list = [None] * int(self.exec_time)
        # Sort tasks by deadline
        tasks = sorted(iter(tasks), key=lambda task: task.deadline)

        for task in tasks:
            exec_time = copy.deepcopy(task.wcet1188)
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
                exec_time = copy.deepcopy(task.wcet1188)
                while(exec_time > 0 and pos < self.exec_time):
                    if timing_list[pos] is None:
                        timing_list[pos] = task.name
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
            index = list(str(key))[-1]
            if str(index).isdigit():
                curr_task = tasks[int(index) - 1]
                res.append((start, curr_task.name, '1188', end, round(burst_length * self.ap1188, 3)))
            else:
                res.append((start, 'IDLE', 'IDLE', end, round(burst_length * self.apidle, 3)))
            start = end + 1
        return res

    def EDF_EE(self):
        pass

    def RM_EE(self):
        pass

    def __str__(self):
        return "Scheduler: {} {} {} {} {} {} {} ({} {})".format(self.task_count, self.exec_time, self.ap1188,
                                                                self.ap918, self.ap648, self.ap384, self.apidle,
                                                                self.sch_type, self.ee)
