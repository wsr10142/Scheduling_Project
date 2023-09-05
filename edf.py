import math

Clock = 0 #時間
Total_Job_Number=0 #紀錄進入系統工作任務的個數
Miss_Deadline_Job_Number=0 #紀錄無法在絕對截限時間之前完成的工作

phase_time = []
period = []
relative_deadline = []
execution_time = []

task_index = 1
task = []
schedule = []
path_in = 'test1.txt'
EDFpath_out = 'EDFpath_out.txt'
output_file = open(EDFpath_out,'w')
output_file.close

#ready queue
class Job:
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
        new_node = Job(release_time,period,remain_execution_time,absolute_deadline,tid)
        
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
                            while index != current_node:
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
                                while index != current_node:
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
                    with open(EDFpath_out,'a') as output_file:
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

    #執行ready queue中的工作
    def schedule(self,Clock):
        if self.head == None:
            with open(EDFpath_out,'a') as output_file:
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
        with open(EDFpath_out,'a') as output_file:
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

#求最小公倍數
def lcm(num):
    minimum = 1
    for i in num:
        minimum = int(i)*int(minimum) / math.gcd(int(i), int(minimum))
    return int(minimum)

#檢查該該排程是否可排
def Schedulability_test():
    sum = 0
    for i in range(len(task)):
        sum+=(task[i][4]/min(task[i][3],task[i][2]))
    print(sum)
    if(sum<=1):
        with open(EDFpath_out, 'a') as output_file:
                print("此排程可排", file=output_file)
    else:
        with open(EDFpath_out, 'a') as output_file:
                print("此排程不可排", file=output_file)
    return

#讀取檔案
with open(path_in) as file:
    for line in file.readlines():
        task_pair = []
        line_split = line.split(',')
        phase_time.append(int(line_split[0]))
        period.append(int(line_split[1]))
        relative_deadline.append(int(line_split[2]))
        execution_time.append(int(line_split[3]))

        task_pair.append("T"+str(task_index))
        task_pair.append(int(line_split[0]))
        task_pair.append(int(line_split[1]))
        task_pair.append(int(line_split[2]))
        task_pair.append(int(line_split[3]))

        task.append(task_pair)
        task_index+=1

print(task)

N = len(phase_time) #總共有幾個任務
LCM = lcm(period) #週期的最小公倍數
MaxPH = max(phase_time) #所有任務的最大phase time

Schedulability_test()
ready_queue = SingleLinkedList()
while(Clock<(LCM+MaxPH)):

    print("Clock"+str(Clock))
    ready_queue.output_queue()

    #檢查missdeadline的工作
    Miss_Deadline_Job_Number += Miss_Deadline_Job_Number+ready_queue.checkAbsolutedeadline(Clock)
    Total_Job_Number-=Miss_Deadline_Job_Number

    #檢查目前時間是否是Job的抵達時間
    for i in range(len(task)):
        if((Clock - task[i][1]) % task[i][2] == 0 and Clock>=task[i][1]):
            ready_queue.append(Clock,task[i][2],task[i][4],Clock+task[i][3],task[i][0])
            Total_Job_Number+=1

    #print("Total_Job_Number："+str(Total_Job_Number))
    #print("Miss_Deadline_Job_Number："+str(Miss_Deadline_Job_Number))

    #執行工作
    Total_Job_Number-=ready_queue.schedule(Clock)

    Clock+=1

output_file.close
