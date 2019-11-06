import copy
from itertools import groupby


class Scheduler(object):

    def __init__(self, task_count: int, exec_time: int, ap1188: int, ap918: int,
                 ap648: int, ap384: int, apidle: int, sch_type: str, ee: bool):
        self.task_count = int(task_count)
        self.exec_time = int(exec_time)
        self.ap1188 = int(ap1188)
        self.ap918 = int(ap918)
        self.ap648 = int(ap648)
        self.ap384 = int(ap384)
        self.apidle = int(apidle)
        self.sch_type = sch_type
        self.ee = ee

    def schedule(self, tasks):
        if self.sch_type.lower() == 'edf' and self.ee is False:
            self.EDF(tasks)
        elif self.sch_type.lower() == 'rm' and self.ee is False:
            self.RM(tasks)
        elif self.sch_type.lower() == 'edf' and self.ee is True:
            self.EDF_EE()
        elif self.sch_type.lower() == 'rm' and self.ee is True:
            self.RM_EE()

    def EDF(self, tasks):
        pass

    def RM(self, tasks):
        time_units = [None] * int(self.exec_time)
        tasks = sorted(iter(tasks), key=lambda task: task.deadline)
        for task in tasks:
            exec_time = copy.deepcopy(task.wcet1188)
            # Construct deadlines list for Task
            x = 1
            count = 0
            while(x < self.exec_time):
                count = count + 1
                x = x + (task.deadline)
            deadlines = [1] + [x * task.deadline for x in range(1, count + 1)]
            #print(task)
            #for dead in deadlines:
            #    print(dead)
            #print('==')
            # add task to schedule
            for deadline in deadlines:
                pos = deadline - 1
                #print('POS: {}'.format(pos))
                exec_time = copy.deepcopy(task.wcet1188)
                #print('TIME: {}'.format(exec_time))
                while(exec_time > 0 and pos < self.exec_time):
                    if time_units[pos] is None:
                        time_units[pos] = task.name
                        exec_time -= 1
                    pos += 1
        #print(time_units)
        res = []
        start = 1
        for key, group in groupby(time_units):
            length = len(list(group))
            end = start + length - 1
            res.append((start, key, end))
            start = end + 1
        print(res)

    def EDF_EE(self):
        pass

    def RM_EE(self):
        pass

    def __str__(self):
        return "Scheduler: {} {} {} {} {} {} {} ({} {})".format(self.task_count, self.exec_time, self.ap1188,
                                                                self.ap918, self.ap648, self.ap384, self.apidle,
                                                                self.sch_type, self.ee)
