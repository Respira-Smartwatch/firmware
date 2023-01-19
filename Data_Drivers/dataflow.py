# -----------------------------------------------------
# Dataflow class for multiprocessed data recording
# -----------------------------------------------------
# Author: Matteo Vidali
#
# Notes: This dataflow class is capable of ~ 16kHz sampling atm
# -----------------------------------------------------

import multiprocessing as mp
import signal
from datetime import datetime
import serial
import time
import os


# Class to determin dataflow of live rapid data collection 
# To both a plotting utility and a save location
class DataFlow:

    #   @breif: initialize the Dataflow Class
    #           - This will create the necessary processes
    #             and track them in a dictionary
    #   @params:
    #            data_read_channels: list of all data read functions.
    #                                   Function MUST RETURN the requested data
    # 
    #            live_plot: True if a plot is desired - will output on serial port
    #            save_data: True if data is to be saved
    #            save_file: String of name of output file or path to desired file location
    #                       The last word in the string (seperated by /) will be used as the filename
    #                       (i.e: 'foo/bar' will create a file named 'bar' in the 'foo' dir)
    #            fs:    Sampling rate desired for the data.
    #            data_read_channel_args: list of args for each data_func -> must be 2d array 
    def __init__(self,  data_read_channels: list[function], 
                        live_plot: bool=True, 
                        save_data: bool=True, 
                        save_file: str=None,
                        fs: int=256,
                        data_read_channel_args: list[list[str]]=[[]]):

        # Child processes are labeled in dictionary
        self.child_processes = {}
        self.data_in = data_read_channels
        self.save_data = save_data
        self.live_plot = live_plot
        self.fs = fs
        
        # This is a 2d array: list of list of args for each datafunc
        self.data_args = data_read_channel_args

        # Save file path handling
        # If the outfile_path is not set,
        # Set it to the date and time
        if save_file is None or "/":
            date = datetime.today().strftime('%Y-%m-%d_%H:%M:%S')
            self.outfile_path = "./"
            self.filename = f"{date}.csv"
        
        elif "/" not in save_file:
            self.outfile_path = f"./"
            self.filename = save_file
        
        else:
            self.outfile_path = ("/").join(save_file.split("/")[:-1])
            self.filename = save_file.split("/")[-1]

        if not os.path.exists(self.outfile_path):
            try:
                os.mkdir(self.outfile_path)
            except PermissionError:
                print(f"{self.outfile_path}is not a writeable Directory. Exiting...")
                exit(1)

        else:
            print("Error, File not writeable")
            exit(1)


        # Set up the multi processes
        self.active_pipes = []

        # If save_data is true, set up a process for saving, and create a pipe to it
        if self.save_data:
            self.recv_save_pipe, self.send_save_pipe = mp.Pipe()
            self.active_pipes.append(self.send_save_pipe)
            self.outfile=open(f"{self.outfile_path}/{self.filename}", 'w+')
            self.child_processes['save'] = mp.Process( target=self._save, args=(self.recv_save_pipe, self.outfile) )
        
        # Same with live_plot
        if self.live_plot:
            self.recv_plot_pipe, self.send_plot_pipe = mp.Pipe()
            self.active_pipes.append(self.send_plot_pipe)
            self.child_processes['plot'] = mp.Process( target=self._plot, args=(self.recv_plot_pipe,) )

        # Set a child process for reading each of the datasources
        for idx, f in enumerate(self.data_in):
            args = [f, tuple(self.active_pipes), self.fs, self.data_args[idx]]
            self.child_processes[f'data_{idx}'] = mp.Process( target=self._data_func, args=tuple(args))

        self._run() 


    #   @breif: Internal function to handle the plotting thread
    #           This function will output to the serial port

    def _plot(self, conn):
        ser = serial.Serial("/dev/ttyS0",
                            baudrate=9600,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS,
                            timeout=1)        


        # Define a signal handler to exit gracefully
        def __sigterm_handler(_signo, _stack_frame):
            print("CAUGHT EXCEPTION IN PLOT")
            exit(1)
        
        signal.signal(signal.SIGTERM, __sigterm_handler)
        while True:
            rec_data=conn.recv()
            #print(f"PLOTTING - plotted: {rec_data}")
            ser.write(rec_data.to_bytes(1, 'little'))

        
        return

    #   @breif: Internal funciton to be passed to file saving thread
    def _save(self, conn, outfile):
        
        # Define a signal handler to exit gracefully
        def __sigterm_handler(_signo, _stack_frame):
            print("\n\nCAUGHT EXCEPTION IN SAVE\n\n")
            outfile.close()
            exit(1)

        # Link signal handler 
        signal.signal(signal.SIGTERM, __sigterm_handler)

        # Actual save loop
        while True:
            rec_data = conn.recv()
            outfile.writelines(str(rec_data)+',\n')
            #print(f"SAVING! saved: {rec_data}")


    #   @breif: Internal function to handle data collection and distribution
    def _data_func(self, data_read, conn, fs, data_read_args:list, continuous=True):

        def __sigterm_handler(_signo, _stack_frame):
            print("CAUGHT EXCEPTION IN DATA_FUNC")
            exit(1)
        
        signal.signal(signal.SIGTERM, __sigterm_handler)


        def tick():
            t = time.time()
            while True:
                t += 1/fs
                yield max(t-time.time(), 0)
        
        g = tick()
        while True:
            time.sleep(next(g))
            data = data_read(*data_read_args)
            for c in conn:
                c.send(data)
            if not continuous:
                break

    #   @breif: Runs all child processes, and sets up 
    #           signal linking 
    def _run(self):
        signal.signal(signal.SIGINT, self._kill)
        if self.save_data:
            self.child_processes['save'].start()
        if self.live_plot:
            self.child_processes['plot'].start()

        self.child_processes['data_0'].start()

    def pause(self):
        pass
    def resume(self):
        pass
    #   @breif: cleanup method for sigkill intterupt
    def _kill(self, _signo, _stack_frame):
        for p in self.child_processes.values():
            p.terminate()


import random
if __name__ == "__main__":
    
    def random_num():
        return random.randint(0, 10)

    d = DataFlow(data_read_channels=[random_num])
