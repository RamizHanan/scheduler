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

    def getNextTask(self, deadlineList, currentTime,deadlineIteration, distanceTillDeadline, nextDeadline):
        for task in deadlineList: #loop over all tasks
            #move to execution function
            if currentTime == int(nextDeadline[task]): #if time has reached a deadline: 
                #self note: execution time should be 0 already
                nextDeadline[task] = int(deadlineIteration[task]) * int(deadlineList[task]) #update its next deadline
                deadlineIteration[task] += 1 #increment next deadline multiplier for that task

            #create time to next deadline for each task
            distanceTillDeadline[task] = int(nextDeadline[task]) - int(currentTime) 

        # Using all() + list comprehension 
        # Finding min value (deadline) in dict
        next =  [key for key in distanceTillDeadline if
                all(distanceTillDeadline[temp] >= distanceTillDeadline[key] 
                for temp in distanceTillDeadline)] 

        return str(next[0])


    # def executeTask(self,readyList, task):
    #     readyList[task] -= 1


    #     pass


# name: str, deadline: int, wcet1188: int, wcet918: int, wcet648: int, wcet384: int
    def EDF(self, tasks) -> list:
        readyList = {} #list of remaining execution times
        deadlineList = {} #constant list of deadlines
        deadlineIteration = {} #list of deadline iterations
        distanceTillDeadline = {} #which task got next
        nextDeadline = {} 
        edf = []
        currentTime = 1
        totalTime = int(self.exec_time) + 1
                                         
        #Check utilization
        utilization = 0
        for taskNum in range(len(tasks)):
            execution = tasks[taskNum].wcet1188
            deadline = tasks[taskNum].deadline
            utilization += float(execution) / float(deadline)    
        print("util amount {}".format(utilization))

        if utilization > 1.0:
            print('Utilization error!')
            return edf

        #initial loading
        for i in range(len(tasks)):
            readyList[tasks[i].name] = int(tasks[i].wcet1188) #initialize execution times
            deadlineList[tasks[i].name] = int(tasks[i].deadline) #initialize deadlines
            nextDeadline[tasks[i].name] = int(tasks[i].deadline) #duplicate of deadline list initially
            deadlineIteration[tasks[i].name] = 2 #next deadline is 2 * initial deadline...then 3 .. 4
            distanceTillDeadline[tasks[i].name] = 0 #used to determine who got next
        

        #for time in range(1, int(totalTime)):
        next = self.getNextTask(deadlineList, currentTime, deadlineIteration, distanceTillDeadline, nextDeadline)
        #execute(next)
        currentTime += 1

        edf.append(next)

        #deadline table
        #always take min of deadline table
        #each step update execution left 


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
