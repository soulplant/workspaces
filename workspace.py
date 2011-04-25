import glob
import os
import re
from tmux import Tmux

class Workspace(object):
    WORKSPACE_DIR='.workspaces'
    @classmethod
    def all(cls, dir=None):
        if dir:
            dir = os.path.join(Workspace.WORKSPACE_DIR, dir)
        else:
            dir = Workspace.WORKSPACE_DIR
        files_and_dirs = glob.glob(os.path.join(os.path.expanduser('~'), dir, '*'))
        files = filter(os.path.isfile, files_and_dirs)
        return [Workspace(f) for f in files]
        
    def __init__(self, filename, tmux = Tmux()):
        self._filename = filename
        self._tmux = tmux

    def __str__(self):
        return 'Workspace[%s]' % self.name()

    def name(self):
        return os.path.basename(self._filename)

    def path(self):
        with open(self._filename) as f:
            return f.readline().rstrip()

    def open(self):
        self._tmux.attach(self.name(), self._filename, self.path())

    def has_sessions(self):
        return self._tmux.has_sessions(self.name())

    def summary_line(self):
        has_sessions = self.has_sessions()
        star = ''
        if has_sessions:
            star = ' *'
        return "%s%s" % (self.name(), star)

    def note(self):
        last_comment = None
        with open(self._filename) as f:
            line = f.readline()
            while line:
                line = line.rstrip()
                if re.match('#', line):
                    last_comment = line
                line = f.readline()
        return last_comment

    def add_note(self, note):
        with open(self._filename, 'a') as f:
            f.write('# ' + note + "\n")
