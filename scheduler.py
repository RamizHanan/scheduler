class Scheduler(object):

    def __init__(self, task_count: int, exec_time: int, ap1188: int, ap918: int,
                 ap648: int, ap384: int, apidle: int, sch_type: str, ee: bool):
        self.task_count = task_count
        self.exec_time = exec_time
        self.ap1188 = ap1188
        self.ap918 = ap918
        self.ap648 = ap648
        self.ap384 = ap384
        self.apidle = apidle
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
        # for i in range(len(tasks)):
        #     print(tasks[i].name)

         #Check utilization
        utilization = 0
        for taskNum in range(len(tasks)):
            execution = tasks[taskNum].wcet1188
            deadline = tasks[taskNum].deadline
            utilization += float(execution) / float(deadline)
            
            print(utilization)
        if utilization > 1:
            print('Utilization error!')

        pass

    def RM(self, tasks):
        time_units = [None] * self.exec_time
        pass

    def EDF_EE(self):
        pass

    def RM_EE(self):
        pass

    def __str__(self):
        return "Scheduler: {} {} {} {} {} {} {} ({} {})".format(self.task_count, self.exec_time, self.ap1188,
                                                                self.ap918, self.ap648, self.ap384, self.apidle,
                                                                self.sch_type, self.ee)
