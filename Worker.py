from queue import Queue
from threading import Thread
import time
import psutil


def prototype(thread_code):
    for i in range(100):
        time.sleep(0.1)
        thread_progress[thread_code] += 1

    return 100
    
class Worker:
    def __init__(self, method, options):
        global thread_progress
        thread_progress = []

        self.queue = Queue()
        self._thread_list = list()

        options = (queue, 0) + options
        for i in range(psutil.cpu_count()):
            options = (queue, i) + options[2:]
            thread = Thread(target=lambda q, arg1: q.put(method(arg1)), args=options)
            thread_progress.append(0)
            self._thread_list.append(thread)

    def start_threads(self):
        for thread in self._thread_list:
            thread.start()

    def get_progress(self):
        message = ''
        i = 0
        for progress in thread_progress:
            message += 'Thread {0}: {1:.2f}%, '.format(i + 1, progress)
            i += 1

        message = message[:-2]

        return message

    def finished(self):
        finished = 0

        for progress in thread_progress:
            if progress == 100:
                finished += 1

        if finished == len(thread_progress):
            return True
        else:
            return False

    def join_threads(self):
        if self.finished():
            for thread in self._thread_list:
                thread.join()

        results_list = []
        while not self.queue.empty():
            result = self.queue.get()
            results_list.append(result)

        return results_list