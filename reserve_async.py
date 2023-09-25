from multiprocessing import Process, Value
# custom process class
from time import sleep, time

from reserve import ReserveSystem


class ReserveProcess(Process):
    # override the constructor
    def __init__(self):
        # execute the base constructor
        Process.__init__(self)
        # self.rer = ReserveSystem()

    def arg(self, i, j, k):
        self.i = i
        self.j = j
        self.k = k
    # override the run function

    def run(self):
        # ('start:', self.i, self.j, self.pid)
        rer = ReserveSystem()
        rer.reserve_once(self.i, self.j, self.k)
        # sleep(1)
        # print('end: ', self.i, self.j, self.pid)


class MyJob:
    def __init__(self) -> None:
        pass

    def run(self, field_list, time_list, dateadd):
        pros = []
        cnt = 0
        for field in field_list:
            for tim in time_list:
                process = ReserveProcess()
                process.arg(field, tim, dateadd)
                process.start()
                pros.append(process)
                process.join()
        # [x.start() for x in pros]
        # [x.join() for x in pros]


# entry point
if __name__ == '__main__':
    # create the process
    start = time()
    job = MyJob()
    job.run([2, 3, 5], [8, 9], 1)
    end = time()
    print("cost: ", end-start)
