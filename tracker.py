'''
Objective:
    This module is for tracking CPI usage of certain job or total usage for a server

'''

import psutil
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import os
import pandas as pd

class Tracker:

    def __init__(self, pid=0, history=[], times=[], start=None):
        self.pid = pid
        self.history = history
        self.times = times
        self.start = start

    def track(self, interval=5, time_span=10):

        if self.pid != 0:
            ## Start the process with pid specified
            process = psutil.Process(self.pid)

            ## Print the tracking start time
            print('CPU tracker is now tracking on PID {}\n'.format(self.pid))

        else:
            print('CPU tracker is now tracking the server')

        self.start = datetime.now()
        print('Current time is {}'.format(self.start))

        delta = timedelta(seconds=time_span*60)
        print('Estimate endtime is {}\n'.format(time_span))

        end = self.start + delta
        print('Estimate endtime is {}\n'.format(end))


        ## Enter the loop
        now = datetime.now()
        time_samples = []

        while now < end:

            if self.pid != 0:
                ## Find the CPU percentage for the specific process
                try:
                    percent = process.cpu_percent(interval=interval)
                    print('CPU usuage for PID {} is now {} percent, with {}s interval'.format(self.pid, percent, interval))
                except:
                    print('PID cannot be found. Generating zero value...')
                    percent = 0

            else:
                ## Find the CPU percentage for the server
                percent = psutil.cpu_percent(interval=interval)
                print('CPU usage for the server is now {} percent, whih {}s interval'.format(percent, interval))

            ## Record time
            delta = now - self.start
            time_samples.append(delta)

            ## Write cpu percentage to the histroy list
            self.history.append(percent)
            print('List updated\n')

            ## Update time
            now = datetime.now()

        ## Transform timedelta to elapsed seconds
        self.times = [t.seconds for t in time_samples]

        return self.history, self.times

    def plot(self):
        df_out = pd.DataFrame(columns=['Time', 'CPU_Percentage'])
        df_out['Time'] = self.times
        df_out['CPU_Percentage'] = self.history
        df_out.to_csv('./logs/Tracker_history_{}.csv'.format(self.start), index=False)

    def report(self):

        print('\n' + '='*30 + '\n')
        print('Printing out CPU usage chart')
        print('\n' + '='*30 + '\n')

        fig = plt.figure(figsize=(10, 6))

        if self.pid != 0:
            plt.plot(self.times, self.history, '-o')
            plt.xlabel('Time (s)')
            plt.ylabel('CPU usage')
            plt.title('CPU Usage for PID {}, \n starting {}'.format(self.pid, self.start))
            plt.savefig('./plots/Tracker_chart_{}.jpg'.format(self.start))
            ##os.system('eog Tracker_chart_{}.jpg'.format(self.start))

        else:
            plt.plot(self.times, self.history, '-o')
            plt.xlabel('Time (s)')
            plt.ylabel('CPU usuage')
            plt.title('CPU Usage for Server, \n starting {}'.format(self.start))
            plt.savefig('./plots/Tracker_chart_{}.jpg'.format(self.start))
            ##os.system('eog Tracker_chart_{}.jpg'.format(self.start))

