import math

Clock = 0 #時間
MaxSimTime = 1000
TotalResponseTime = 0
FinishedAJobNumber = 0
MissPJobNumber=0
TotalPJobNumber=0
Miss_rate = 0
Average_Response_Time = 0
us = 0.2

#periodic job
period_periodic = []
execution_time_periodic = []
task_periodic = []

#aperiodic job
phase_time_aperiodic = []
execution_time_aperiodic = []
task_aperiodic = []

path_in_periodic = 'periodic_0.9.txt'
path_in_aperiodic = 'aperiodic.txt'
tbspath_out = 'TBSpath_out.txt'
output_file = open(tbspath_out,'w')
output_file.close

class Job_periodic:
    def __init__(self,release_time,period,remain_execution_time,absolute_deadline,tid):
        self.release_time = release_time
        self.period = period
        self.remain_execution_time= remain_execution_time
        self.absolute_deadline = absolute_deadline
        self.tid = tid
        self.next = None

class SingleLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, release_time,period,remain_execution_time,absolute_deadline,tid):
        #建立Job的新Node
        new_node = Job_periodic(release_time,period,remain_execution_time,absolute_deadline,tid)
        
        #如果head==None，代表為第一個Node
        if self.head == None:
            self.head = new_node
            self.tail = new_node

        #比較新job跟ready queue中job的absolutedeadline
        else:
            current_node = self.head
            while current_node != None:
                if(new_node.absolute_deadline<current_node.absolute_deadline):
                    if(len(self)==1):
                        self.head = new_node
                        self.head.next = current_node
                        return
                    else:
                        if(current_node==self.head):
                            new_node.next = self.head
                            self.head = new_node
                            return
                        elif(current_node == self.tail):
                            index = self.head
                            while index.next != self.tail:
                                index = index.next
                            index.next = new_node
                            new_node.next = self.tail
                            return
                        else:
                            index = self.head
                            while index.next != current_node:
                                index = index.next
                            index.next = new_node
                            new_node.next = current_node
                            return
                #當absolute_deadline一樣時，判斷編號大小
                elif(new_node.absolute_deadline==current_node.absolute_deadline):
                    if(int(new_node.tid[1])<int(current_node.tid[1])):
                        if(len(self)==1):
                            self.head = new_node
                            self.head.next = current_node
                            return
                        else:
                            if(current_node==self.head):
                                new_node.next = self.head
                                self.head = new_node
                                return
                            elif(current_node == self.tail):
                                index = self.head
                                while index.next != self.tail:
                                    index = index.next
                                index.next = new_node
                                new_node.next = self.tail
                                return
                            else:
                                index = self.head
                                while index.next != current_node:
                                    index = index.next
                                index.next = new_node
                                new_node.next = current_node
                                return
                    else:
                        if(current_node != self.tail):
                            index = self.head
                            while index != current_node.next:
                                index = index.next
                            current_node.next = new_node
                            new_node.next = index
                            return
                current_node = current_node.next
            self.tail.next = new_node
            self.tail = new_node

    #檢查是否有工作miss掉deadline
    def checkAbsolutedeadline(self,Clock):
        miss_count = 0
        if self.head == None:
            return int(miss_count)
        else:
            current_node = self.head
            while current_node != None:
                if(current_node.absolute_deadline-Clock-current_node.remain_execution_time<0):
                    with open(tbspath_out,'a') as output_file:
                        print(str(Clock)+"：Miss deadline："+current_node.tid,file=output_file)
                    if(current_node==self.head):
                        if(len(self)==1):
                            self.head = None
                            self.tail = None
                            miss_count+=1
                        else:
                            self.head = self.head.next
                            miss_count+=1
                    elif(current_node==self.tail):
                        index = self.head
                        while index.next != current_node:
                            index = index.next
                        self.tail = index
                        self.tail.next = None
                        current_node = None
                        miss_count += 1
                        return int(miss_count)
                    else:
                        index = self.head
                        while index.next != current_node:
                            index = index.next
                        index.next = current_node.next
                        current_node.next = None
                        current_node = index
                        miss_count+=1
                current_node = current_node.next
        return int(miss_count)

    #比較periodic與aperiodic的優先度
    def find_minDL(self,Clock,cus_deadline):
        if self.head == None:
            #執行aperiodic工作
            ready_queue_aperiodic[0][2]-=1
            with open(tbspath_out,'a') as output_file:
                print(str(Clock)+" "+str(ready_queue_aperiodic[0][0]),file=output_file)
            if(ready_queue_aperiodic[0][2]==0):
                responsetime = Clock+1 - ready_queue_aperiodic[0][1]
                ready_queue_aperiodic.pop(0)
                if(len(queue_aperiodic)>0):
                    task_pair = []
                    task_pair.append(queue_aperiodic[0][0])
                    task_pair.append(queue_aperiodic[0][1])
                    task_pair.append(queue_aperiodic[0][2])
                    task_pair.append(queue_aperiodic[0][3])
                    ready_queue_aperiodic.append(task_pair)
                    queue_aperiodic.pop(0)
                print("responsetime:"+str(responsetime))
                return int(responsetime)
            return int(0)
        else:
            minDL = self.head.absolute_deadline
            if(minDL<ready_queue_aperiodic[0][3]):
                #執行periodic工作
                self.schedule(Clock)
                return int(0)
            else:
                #執行aperiodic工作
                ready_queue_aperiodic[0][2]-=1
                with open(tbspath_out,'a') as output_file:
                    print(str(Clock)+" "+str(ready_queue_aperiodic[0][0]),file=output_file)
                if(ready_queue_aperiodic[0][2]==0):
                    responsetime = Clock+1 - ready_queue_aperiodic[0][1]
                    ready_queue_aperiodic.pop(0)
                    if(len(queue_aperiodic)>0):
                        task_pair = []
                        task_pair.append(queue_aperiodic[0][0])
                        task_pair.append(queue_aperiodic[0][1])
                        task_pair.append(queue_aperiodic[0][2])
                        task_pair.append(queue_aperiodic[0][3])
                        ready_queue_aperiodic.append(task_pair)
                        queue_aperiodic.pop(0)
                    print("responsetime:"+str(responsetime))
                    return int(responsetime)
                return int(0)

    #執行ready queue中的工作
    def schedule(self,Clock):
        if self.head == None:
            with open(tbspath_out,'a') as output_file:
                print(str(Clock)+" No job",file=output_file)
            return 0
        else:
            complete_job = 0
            tid = self.head.tid
            self.head.remain_execution_time-=1
            if(self.head.remain_execution_time==0):
                complete_job = 1
                if(len(self)==1):
                    self.head = None
                    self.tail = None
                else:
                    self.head = self.head.next
        with open(tbspath_out,'a') as output_file:
            print(str(Clock)+" "+tid,file=output_file)
        return int(complete_job)

    #計算ready queue長度
    def __len__(self):
        length = 0
        current_node = self.head
        while current_node != None:
            length += 1
            current_node = current_node.next
        return length

    #印出ready queue
    def output_queue(self):
        current_node = self.head
        result = []
        while current_node != None:
            result.append(current_node.tid)
            current_node = current_node.next
        print("Ready Queue："+str(result))
        #print(result)
        return

#讀取檔案
with open(path_in_periodic) as file:
    #任務編號
    task_index = 1
    for line in file.readlines():
        task_pair = []
        line_split = line.split(',')
        period_periodic.append(int(line_split[0]))
        execution_time_periodic.append(int(line_split[1]))

        task_pair.append("T"+str(task_index))
        task_pair.append(int(line_split[0]))
        task_pair.append(int(line_split[1]))

        task_periodic.append(task_pair)
        task_index+=1

print(task_periodic)

#讀取檔案
with open(path_in_aperiodic) as file:
    #任務編號
    task_index = 1
    for line in file.readlines():
        task_pair = []
        line_split = line.split(',')
        phase_time_aperiodic.append(int(line_split[0]))
        execution_time_aperiodic.append(int(line_split[1]))

        task_pair.append("A"+str(task_index))
        task_pair.append(int(line_split[0]))
        task_pair.append(int(line_split[1]))

        task_aperiodic.append(task_pair)
        task_index+=1

print(task_aperiodic)

ready_queue_periodic = SingleLinkedList()
ready_queue_aperiodic = []
queue_aperiodic = []
cus_deadline = 0

while(Clock<(MaxSimTime)):

    #檢查periodic job是否miss掉deadline
    MissJob = ready_queue_periodic.checkAbsolutedeadline(Clock)
    if(MissJob>0):
        MissPJobNumber = MissPJobNumber + MissJob

    #檢查目前時間是否是periodic job的抵達時間
    for i in range(len(task_periodic)):
        if(Clock % task_periodic[i][1] == 0):
            ready_queue_periodic.append(Clock,task_periodic[i][1],task_periodic[i][2],Clock+task_periodic[i][1],task_periodic[i][0])
            TotalPJobNumber+=1

    #檢查目前時間是否是periodic job的抵達時間
    for i in range(len(task_aperiodic)):
        if(Clock == task_aperiodic[i][1]):
            #假設aperiodic沒有job且clock大於cus的絕對截限時間，則更新cus的絕對截限時間
            if(len(ready_queue_aperiodic)==0):
                cus_deadline = max(cus_deadline,Clock) + task_aperiodic[i][2]/us
                task_pair = []
                task_pair.append(task_aperiodic[i][0])
                task_pair.append(task_aperiodic[i][1])
                task_pair.append(task_aperiodic[i][2])
                task_pair.append(cus_deadline)
                ready_queue_aperiodic.append(task_pair)
            #假設job進入時，aperiodic中有job或是clock小於cus的絕對截限時間，只需要將job放進queue中就好
            else:
                cus_deadline = max(cus_deadline,Clock) + task_aperiodic[i][2]/us
                task_pair = []
                task_pair.append(task_aperiodic[i][0])
                task_pair.append(task_aperiodic[i][1])
                task_pair.append(task_aperiodic[i][2])
                task_pair.append(cus_deadline)
                queue_aperiodic.append(task_pair)

    print("Clock"+str(Clock))
    ready_queue_periodic.output_queue()
    print(ready_queue_aperiodic)
    print(queue_aperiodic)

    if(len(ready_queue_aperiodic)>0):
        print(ready_queue_aperiodic[0][3])
        #找到絕對截限時間較小的job
        responsetime = ready_queue_periodic.find_minDL(Clock,cus_deadline)
        if(responsetime>0):
            TotalResponseTime = TotalResponseTime + responsetime
            FinishedAJobNumber+=1
    else:
        #執行periodic工作
        ready_queue_periodic.schedule(Clock)

    Clock+=1

print("MissPJobNumber:"+str(MissPJobNumber))
print("TotalPJobNumber:"+str(TotalPJobNumber))
Miss_rate = MissPJobNumber/TotalPJobNumber
print("Miss_rate:"+str(Miss_rate))

print("TotalResponseTime:"+str(TotalResponseTime))
print("FinishedAJobNumber:"+str(FinishedAJobNumber))
Average_Response_Time = TotalResponseTime/FinishedAJobNumber
print("Average_Response_Time:"+str(Average_Response_Time))

output_file.close
