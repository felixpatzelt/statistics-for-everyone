#!/usr/bin/env python

# Helper for automated notebook conversion & viewing
# use:  python make_slides.py --serve True --watch True
# more: python make_slides.py --help

import os
import argparse
from glob import glob
import subprocess
from multiprocessing import Process
from functools import partial
import shlex
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from time import sleep


INPUT_GLOB = '*.ipynb'
OUTPUT_DIR = 'slides'
SERVE      = False
WATCH      = False
PORT       = 8000

def convert_notebook(
        filename,
        output_dir,
        cmd_tpl = (
            "jupyter nbconvert --execute {filename} "
            "--output-dir={output_dir} --to slides --no-input"
        ),
        extra_env = {'CONVERT':'TRUE'},
        verbose=True
    ):
    cmd = cmd_tpl.format(filename=filename, output_dir=output_dir)
    env = os.environ.copy()
    env.update(extra_env)
    sp = subprocess.run(shlex.split(cmd), env=env, capture_output=True)
    if verbose:
        print(sp.stdout.decode())
        print(sp.stderr.decode())
    return sp


def serve(directory, port):

    Handler = partial(SimpleHTTPRequestHandler, directory=directory)
    
    with TCPServer(("localhost", port), Handler) as httpd:
        print("serving at port", port)
        httpd.serve_forever()


class Server():
    def __init__(self, directory, port):
        self.directory = directory
        self.port      = port
        self.process   = None
        
    def start(self):
        if self.process is not None:
            self.stop()
        self.process = Process(target=serve, args=[self.directory, self.port])
        self.process.start()
        print("Started server with pid", self.process.pid)
       
    def stop(self):
        self.process.terminate()
        print("Stopped server with pid", self.process.pid)


class Watcher():
    def __init__(self, glob_pattern, callback):
        self.glob_pattern = glob_pattern
        self.callback = callback
        nb_files = glob(self.glob_pattern)
        self.last_changes = {
            file: 0 for file in nb_files
        }
        
    def update(self):
        nb_files = glob(self.glob_pattern)
        for file in nb_files:
            last_change = os.path.getmtime(file)
            if (
                not file in self.last_changes
                or last_change > self.last_changes[file]
            ):
                self.callback(file)
                self.last_changes[file] = last_change

    def watch(self):
        while True:
            self.update()
            sleep(2)


def main(input_glob, output_dir, serve, watch, port):
    
    if serve:
        server = Server(output_dir, port)
        server.start()
    else:
        server = None
    
    watcher = Watcher(input_glob, partial(convert_notebook, output_dir=output_dir))
    
    if watch:
        watcher.watch()
    else:
        watcher.update()
    
    return server, watcher
    

def str2bool(v):
    "https://stackoverflow.com/a/43357954"
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert notebooks to slides')

    parser.add_argument(
        '--input_glob', 
        default=INPUT_GLOB,
        help=f'Glob pattern to select notebooks (default: {INPUT_GLOB})'
    )
    parser.add_argument(
        '--output_dir', 
        default=OUTPUT_DIR,
        help=f'Directory where slides are written (default: {OUTPUT_DIR})'
    )
    parser.add_argument(
        '--serve', 
        default=SERVE,
        type=str2bool,
        help=f'Start webserver on localhost to serve converted slides (default: {SERVE})'
    )
    parser.add_argument(
        '--watch', 
        default=WATCH,
        type=str2bool,
        help=f'Keep watching for future changes and re-convert slides automatically (default: {WATCH})'
    )
    parser.add_argument(
        '--port', 
        default=PORT,
        type=int,
        help=f'Port for serving (default: {PORT})'
    )   
    args = parser.parse_args()
    
    
    main(args.input_glob, args.output_dir, args.serve, args.watch, args.port)
