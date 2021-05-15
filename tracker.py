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
import logging

class Tracker:

    def __init__(self, pid):
        self._pid = pid
        self._start = None
        self.history = []
        self.times = []

    @property
    def pid(self):
        return self._pid

    @pid.setter
    def pid(self, pid):
        if pid < 0:
            raise ValueError('PID value must be positive or equal to zero.')
        self._pid = pid

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        self._start = start

    def track(self, interval=5, time_span=10):

        logging.basicConfig(filename='./logs/tracker_log', filemode='w', level=logging.DEBUG,
                            format='[%(asctime)s] %(levelname)s: %(message)s',
                            datefmt='%m/%d/%Y %H:%M:%S'
                            )
        logging.getLogger('matplotlib.font_manager').disabled = True
        logging.info('The PID is {}'.format(self.pid))

        is_process = True
        if self.pid > 0:
            ## Start the process with pid specified
            process = psutil.Process(self.pid)

            ## Print the tracking start time
            print('CPU tracker is now tracking on PID {}\n'.format(self.pid))
            logging.info('CPU tracker is now tracking on PID {}\n'.format(self.pid))
        else:
            is_process = False
            print('CPU tracker is now tracking the server')
            logging.info('CPU tracker is now tracking the server')

        self.start = datetime.now()
        print('Current time is {}'.format(self.start))
        logging.info('Current time is {}'.format(self.start))

        delta = timedelta(seconds=time_span*60)
        print('Estimate time span is {} min\n'.format(time_span))
        logging.info('Estimate time span is {} min\n'.format(time_span))

        end = self.start + delta
        print('Estimate endtime is {}\n'.format(end))
        logging.info('Estimate endtime is {}\n'.format(end))

        ## Enter the loop
        time_samples = []

        logging.debug('Entering the while loop...')

        now = datetime.now()
        logging.debug('Time tracker for now is {}'.format(now))

        while now < end:

            if is_process:
                ## Find the CPU percentage for the specific process
                try:
                    percent = process.cpu_percent(interval=interval)
                    logging.debug('CPU usuage for PID {} is now {} percent, with {}s interval'.format(self.pid, percent, interval))
                except:
                    logging.debug('PID cannot be found. Generating zero value...')
                    percent = 0

            else:
                ## Find the CPU percentage for the server
                percent = psutil.cpu_percent(interval=interval)
                logging.debug('CPU usage for the server is now {} percent, with {}s interval'.format(percent, interval))

            ## Record time
            delta = now - self.start
            logging.debug('time delta is {}'.format(delta))
            time_samples.append(delta)
            logging.debug('time sample is appended')

            ## Write cpu percentage to the histroy list
            self.history.append(percent)
            logging.debug('CPU history list updated\n')

            ## Update time
            now = datetime.now()
            logging.debug('Time tracker for now is updated to {}'.format(now))

        logging.debug('Breaking the while loop.....')

        ## Transform timedelta to elapsed seconds
        self.times = [t.seconds for t in time_samples]
        logging.debug('Elapsed times transformed to seconds')

        return self.history, self.times

    def save(self):
        df_out = pd.DataFrame(columns=['Time', 'CPU_Percentage'])
        df_out['Time'] = self.times
        df_out['CPU_Percentage'] = self.history
        start_str = self.start.strftime('%m-%d-%Y_%H-%M-%S')
        df_out.to_csv('./history/Tracker_history_{}.csv'.format(start_str), index=False)

    def plot(self):

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

