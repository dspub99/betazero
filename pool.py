#!/usr/bin/env python

import multiprocessing

class Worker:
    def __call__(self, task):
        result = None
        return result

class Message:
    def __init__(self, id, msg):
        self.id = id
        self.msg = msg

class WorkerContainer(multiprocessing.Process):
    def __init__(self, taskQueue, resultQueue, worker):
        multiprocessing.Process.__init__(self)
        self._taskQueue = taskQueue
        self._resultQueue = resultQueue
        self._worker = worker

    def run(self):
        while True:
            task = self._taskQueue.get() # a list of Messages
            results = [Message(m.id, self._worker(m.msg)) for m in task]
            self._resultQueue.put(results)
            self._taskQueue.task_done()

class Pool:
    def __init__(self, workers):
        self._taskQueue = multiprocessing.JoinableQueue()
        self._resultQueue = multiprocessing.Queue()
        self._workerContainers = [WorkerContainer(self._taskQueue, self._resultQueue, w)
                                  for w in workers]

    def start(self):
        for w in self._workerContainers:
            w.start()

    def runTasks(self, tasks):
        nw = len(self._workerContainers)
        taskLists = [[] for _ in range(nw)]
        it = 0
        for id, t in enumerate(tasks):
            taskLists[it].append(Message(id, t))
            it += 1
            if it == nw:
                it = 0

        for tl in taskLists:
            self._taskQueue.put(tl)

        results = []
        while len(results) < len(tasks):
            res = self._resultQueue.get()
            results.extend( [ (m.id, m.msg) for m in res] )
        results.sort()
        return [r[1] for r in results]

    def stop(self):
        for wc in self._workerContainers:
            wc.terminate()

if __name__=="__main__":

    class MyWorker:
        def __init__(self):
            pass
        def __call__(self, task):
            result = 2*task
            return result

    import sys
    n = int(sys.argv[1])
    import time
    p = Pool([MyWorker() for _ in range(38)])
    p.start()
    print ("Ok")
    t0 = time.time()
    print (len(p.runTasks(list(range(n)))))
    tf = time.time()
    print ("Done dt = %f" % (tf-t0))
    p.stop()




