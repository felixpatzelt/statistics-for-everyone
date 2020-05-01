import subprocess
from glob import glob
import ipywidgets as widgets

class Voilauncher():
    def __init__(self, notebooks):
        self.notebook_file = ''
        self.process = None
        self.cmd_tpl = '''voila {notebook_file} --template=reveal --VoilaConfiguration.resources="{{'reveal': {{'theme': 'simple'}}}}"'''

        self.dropdown = widgets.Dropdown(options=notebooks)
        self.launch_btn = widgets.Button(description='Start Voila')
        self.terminate_btn = widgets.Button(description='Stop Voila')

        self.launch_btn.on_click(self.launch)
        self.terminate_btn.on_click(self.terminate)

    def launch(self,b):
        if self.process is not None:
            self.terminate()
        self.notebook_file = self.dropdown.value
        self.process = subprocess.Popen(self.cmd_tpl.format(notebook_file=self.notebook_file), shell=True)
        print("C'est parti! Started notebook", self.notebook_file, ' with pid', launcher.process.pid) # check notebook console
    
    def show(self):
        return widgets.Box([self.dropdown, self.launch_btn, self.terminate_btn])
    
    def terminate(self, b=None):
        self.process.terminate()
        launcher.process.wait()
        print("Terminated notebook", self.notebook_file, ' with pid', launcher.process.pid) # check notebook console

