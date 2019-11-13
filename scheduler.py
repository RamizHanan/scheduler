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


    def getNextTask(self, deadlineList, time, distanceTillDeadline, nextDeadline, readyList):
        
        if(self.idleCheck(readyList, time, nextDeadline) == True):
            return 'IDLE'

        for task in deadlineList: #loop over all tasks
            #update distance until deadline
            distanceTillDeadline[task] = int(nextDeadline[task]) - int(time) 

        # Using all() + list comprehension 
        # Finding min value (deadline) in dict
        next =  [key for key in distanceTillDeadline if
                all(distanceTillDeadline[temp] >= distanceTillDeadline[key] 
                for temp in distanceTillDeadline)] 

        return str(next[0])

    def idleCheck(self, readyList, time, nextDeadline):
        idle = False
                
        #if all execution times are 0 and there is time left until all their deadlines
        if (all(executeTime == 0 for executeTime in readyList.values()) and 
            all(deadline > time for deadline in nextDeadline.value())):
            idle = True

        return idle

    def checkExecutionFinished(self,readyList, task, time, executionTimes,
                    deadlineIteration, nextDeadline, returnTime, deadlineList):
        #next return time is the next deadline
        if readyList[task] == 0 and time == int(returnTime[task]):
            returnTime[task] = int(nextDeadline[task])#next return time is the next deadline
            readyList[task] = executionTimes[task] #reset execution
            nextDeadline[task] = int(deadlineIteration[task]) * int(deadlineList[task]) #update its next deadline
            deadlineIteration[task] += 1 #increment next deadline multiplier for that task

    def executeTask(self,readyList, task, time, executionTimes,
                    deadlineIteration, nextDeadline, returnTime, deadlineList):
        if task == "IDLE":
            return task

        #execute
        readyList[task] -= 1
        executed = task

        self.checkExecutionFinished(readyList, task, time, executionTimes,
                                    deadlineIteration, nextDeadline, returnTime, deadlineList)
        
        return executed


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
        time = 1
        totalTime = int(self.exec_time) + 1
                                         
        #Check utilization
        utilization = 0
        for taskNum in range(len(tasks)):
            execution = tasks[taskNum].wcet1188
            deadline = tasks[taskNum].deadline
            utilization += float(execution) / float(deadline)    
        #print("util amount {}".format(utilization))

        if utilization > 1.0:
            print('Utilization error!')
            return edf

        #initial loading
        for i in range(len(tasks)):
            readyList[tasks[i].name] = int(tasks[i].wcet1188) #initialize execution times
            deadlineList[tasks[i].name] = int(tasks[i].deadline) #initialize deadlines
            nextDeadline[tasks[i].name] = int(tasks[i].deadline) #duplicate of deadline list initially
            returnTime[tasks[i].name] = int(tasks[i].deadline) #list for return times to the system
            deadlineIteration[tasks[i].name] = 2 #next deadline is 2 * initial deadline...then 3 .. 4
            distanceTillDeadline[tasks[i].name] = 0 #used to determine who got next
        

        for time in range(1, int(totalTime)):
            nextTask = self.getNextTask(deadlineList, time, distanceTillDeadline, nextDeadline, readyList)
            executeTask = self.executeTask(readyList, nextTask, time, executionTimes,
                    deadlineIteration, nextDeadline, returnTime, deadlineList)
            
            edf.append(executeTask)
            time += 1

        print(str(edf))
        return edf

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
