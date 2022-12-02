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

# Class to determin dataflow of live rapid data collection 
# To both a plotting utility and a save location
class DataFlow:

    #   @breif: initialize the DataflowClass
    #           - This will create the necessary processes
    #             and track them in a dictionary
    #   @params:
    #            data_read_channels: list of all data read functions.
    #                                   Function MUST RETURN the requested data
    # 
    #            live_plot: True if a plot is desired
    #            save_data: True if data is to be saved
    #            save_file: String of name of output file
    #            data_read_channel_args: list of args for each data_func -> must be 2d array 
    def __init__(self,  data_read_channels: list, 
                        live_plot: bool=True, 
                        save_data: bool=True, 
                        save_file: str=None,
                        data_read_channel_args: list[list[str]]=[[]]):

        # Child processes are labeled in dictionary
        self.child_processes = {}
        self.data_in = data_read_channels
        self.save_data = save_data
        self.live_plot = live_plot
        
        # This is a 2d array: list of list of args for each datafunc
        self.data_args = data_read_channel_args

        # outfile path is path to save file
        self.outfile_path = save_file

        # If the outfile_path is not set,
        # Set it to the date and time
        if save_file is None:
            date = datetime.today().strftime('%Y-%m-%d_%H:%M:%S')
            self.outfile_path = f"./{date}.csv"
        

        # Setup potential pipes
        self.recv_save_pipe, self.send_save_pipe = mp.Pipe()
        self.recv_plot_pipe, self.send_plot_pipe = mp.Pipe()

         
        self.active_pipes = []
        if self.save_data:
            self.active_pipes.append(self.send_save_pipe)
        if self.live_plot:
            self.active_pipes.append(self.send_plot_pipe)

        # Set a child process for reading each of the datasources
        for idx, f in enumerate(self.data_in):

            args = [f, tuple(self.active_pipes), self.data_args[idx]]

            self.child_processes[f'data_{idx}'] = mp.Process( target=self._data_func, args=tuple(args))

        # 
        if live_plot:
            self.child_processes['plot'] = mp.Process( target=self._plot, args=(self.recv_plot_pipe,) )

        if save_data:
            self.outfile=open(self.outfile_path, 'w+')
            self.child_processes['save'] = mp.Process( target=self._save, args=(self.recv_save_pipe, self.outfile) )


        self._run() 


    #   @breif: Internal function to handle the plotting thread
    def _plot(self, conn):
        
        # Define a signal handler to exit gracefully
        def __sigterm_handler(_signo, _stack_frame):
            print("CAUGHT EXCEPTION IN PLOT")
            exit(1)
        
        signal.signal(signal.SIGTERM, __sigterm_handler)

        while True:
            rec_data=conn.recv()
            print(f"PLOTTING - plotted: {rec_data}")
        
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
            print(f"SAVING! saved: {rec_data}")


    #   @breif: Internal function to handle data collection and distribution
    def _data_func(self, data_read, conn, data_read_args:list, continuous=True):

        def __sigterm_handler(_signo, _stack_frame):
            print("CAUGHT EXCEPTION IN DATA_FUNC")
            exit(1)
        
        signal.signal(signal.SIGTERM, __sigterm_handler)

        while True:
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


    #   @breif: cleanup method for sigkill intterupt
    def _kill(self, _signo, _stack_frame):
        for p in self.child_processes.values():
            p.terminate()


import random
if __name__ == "__main__":
    
    def random_num():
        return random.randint(0, 10)

    d = DataFlow(data_read_channels=[random_num])
