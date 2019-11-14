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

        
    def getNextTask(self, deadlineList, time, nextDeadline, readyList):
        distanceTillDeadline = {}
        unfinishedTasksDeadlines = {}

        if(self.idleCheck(readyList, time, nextDeadline) == True):
            return 'IDLE'

        #exclude items with 0 execution left
        for (task, executionLeft) in readyList.items():
            if executionLeft != 0:
                unfinishedTasksDeadlines[task] = nextDeadline[task]


        for task in unfinishedTasksDeadlines: #loop over all tasks
            #update distance until deadline
            distanceTillDeadline[task] = int(nextDeadline[task]) - int(time) 

        # Using all() + list comprehension 
        # Finding min value (deadline) in dict
        next =  [key for key in distanceTillDeadline if
                all(distanceTillDeadline[temp] >= distanceTillDeadline[key] 
                for temp in distanceTillDeadline)]

        if(next):
            return str(next[0])

        return 'IDLE'

    def idleCheck(self, readyList, time, nextDeadline):
        idle = False
                
        #if all execution times are 0 and there is time left until all their deadlines
        if (all(executeTime == 0 for executeTime in readyList.values()) and 
            all(deadline > time for deadline in nextDeadline.values())):
            idle = True

        return idle
    
    def checkExecutionFinished(self,readyList, time, executionTimes,
                    deadlineIteration, nextDeadline, returnTime, deadlineList):
        '''   
        this needs to be checked for every task at evert time unit.. if a task has 0 execution left,
        then compare time to its return time and update if necessary
        '''
        for task, executionTime in readyList.items():
            if executionTime == 0 and time == int(returnTime[task]):
                nextDeadline[task] = int(deadlineIteration[task]) * int(deadlineList[task]) #update its next deadline
                returnTime[task] = int(nextDeadline[task])#next return time is the next deadline
                readyList[task] = executionTimes[task] #reset execution
                deadlineIteration[task] += 1 #increment next deadline multiplier for that task
        #next return time is the next deadline
            

    def executeTask(self,readyList, task, time, executionTimes,
                    deadlineIteration, nextDeadline, returnTime, deadlineList):
        if task == "IDLE":
            return task

        #execute
        readyList[task] -= 1
        executed = task

        return executed

    def checkEdfUtilization(self,tasks):
         #Check utilization
        utilization = 0
        for taskNum in range(len(tasks)):
            execution = tasks[taskNum].wcet1188
            deadline = tasks[taskNum].deadline
            utilization += float(execution) / float(deadline)

        return utilization

# name: str, deadline: int, wcet1188: int, wcet918: int, wcet648: int, wcet384: int
    def EDF(self, tasks) -> list:
        readyList = {} #list of remaining execution times
        executionTimes = {} #constant list of execution times
        deadlineList = {} #constant list of deadlines
        deadlineIteration = {} #list of deadline iterations
        distanceTillDeadline = {} #which task got next
        nextDeadline = {}
        returnTime = {} 
        edf = []
        totalTime = int(self.exec_time) + 1
                                         
        #EDF utilization checker 2.0 BETA
        if self.checkEdfUtilization(tasks) > 1.0:
            print('Utilization error!')
            return edf

        #initial loading
        for i in range(len(tasks)):
            readyList[tasks[i].name] = int(tasks[i].wcet1188) #initialize execution times
            deadlineList[tasks[i].name] = int(tasks[i].deadline) #initialize deadlines
            nextDeadline[tasks[i].name] = int(tasks[i].deadline) #duplicate of deadline list initially
            returnTime[tasks[i].name] = int(tasks[i].deadline) #list for return times to the system
            deadlineIteration[tasks[i].name] = 2 #next deadline is 2 * initial deadline...then 3 .. 4
            executionTimes[tasks[i].name] = int(tasks[i].wcet1188) #execution table
        

        for time in range(1, int(totalTime)):
            
            nextTask = self.getNextTask(deadlineList, time, nextDeadline, readyList)
            executeTask = self.executeTask(readyList, nextTask, time, executionTimes,
                    deadlineIteration, nextDeadline, returnTime, deadlineList)
            self.checkExecutionFinished(readyList, time, executionTimes,
                                    deadlineIteration, nextDeadline, returnTime, deadlineList)
            
            edf.append(executeTask)
            #print(executeTask,time)

        print(str(edf))
        return edf

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





#   for task in deadlineList: #loop over all tasks
#             #update distance until deadline
#             distanceTillDeadline[task] = int(nextDeadline[task]) - int(time) 

#         # Using all() + list comprehension 
#         # Finding min value (deadline) in dict
#         next =  [key for key in distanceTillDeadline if
#                 all(distanceTillDeadline[temp] >= distanceTillDeadline[key] 
#                 for temp in distanceTillDeadline)] 