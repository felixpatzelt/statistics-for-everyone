#!/usr/bin/env python

# Helper for automated notebook conversion & local viewing
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

# nb conversion
INPUT_GLOB = '*.ipynb'
OUTPUT_DIR = 'slides'

# serving
SERVE      = False
WATCH      = False
PORT       = 8000
HOST       = "localhost" # currently fixed

# template for index with table of contents
INDEX_TEMPLATE_FILE = 'index.template.html'
INDEX_TOC_PRE_TPL   = "  <ul>"
INDEX_TOC_ENTRY_TPL = "    <li><a href={href}>{title}</li>"
INDEX_TOC_POST_TPL  = "  </ul>"


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
    

def make_index(output_dir):
    """Create index.html with list of slide decks (.html files in output dir)
    """
    
    print("updating index.html")
    with open(INDEX_TEMPLATE_FILE, 'r') as f:
        index_template = f.read()
    
    html_files = sorted(glob(os.path.join(output_dir, '*.html')))    
    toc         = [INDEX_TOC_PRE_TPL]
    for f in html_files:
        href = f.split('/')[-1]
        if href == "index.html":
            continue
        title = (
            href.lower()
            .replace('.html','')
            .replace('.slides','')
            .replace('_', ' ')
            .title()
        )
        toc.append(INDEX_TOC_ENTRY_TPL.format(href=href, title=title))
    toc.append(INDEX_TOC_POST_TPL)
    
    index_page = (index_template.format(table_of_contents="\n".join(toc)))
    
    with open(os.path.join(output_dir,'index.html'), 'w') as f:
        f.write(index_page)
        

def convert_notebook_and_update_index(
        notebook_filename, output_dir, **convert_nb_kwargs
    ):
    convert_notebook(notebook_filename, output_dir, **convert_nb_kwargs)
    make_index(output_dir)


def serve(directory, port):
    "See https://docs.python.org/2/library/simplehttpserver.html"
    Handler = partial(SimpleHTTPRequestHandler, directory=directory)
    
    with TCPServer((HOST, port), Handler) as httpd:
        print(f"serving {directory} at http://{HOST}:{port}")
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
    
    watcher = Watcher(
        input_glob, 
        partial(convert_notebook_and_update_index, output_dir=output_dir)
    )
    
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
