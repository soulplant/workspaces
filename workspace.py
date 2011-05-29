import glob
import os
import re
import time
from tmux import Tmux

class Workspace(object):
    WORKSPACE_DIR='.workspaces'
    @classmethod
    def workspace_files_and_dirs(cls, dir=None):
        if dir:
            dir = os.path.join(Workspace.WORKSPACE_DIR, dir)
        else:
            dir = Workspace.WORKSPACE_DIR
        return glob.glob(os.path.join(os.path.expanduser('~'), dir, '*'))

    @classmethod
    def all(cls, dir=None):
        files_and_dirs = Workspace.workspace_files_and_dirs(dir)
        files = filter(os.path.isfile, files_and_dirs)
        result = [Workspace(f) for f in files]
        index = LastAccessedIndex()
        return index.sort(result)

    @classmethod
    def all_subdirs(cls, dir=None):
        files_and_dirs = Workspace.workspace_files_and_dirs(dir)
        dirs = filter(os.path.isdir, files_and_dirs)
        return [os.path.basename(dir) for dir in dirs]

    def __init__(self, filename, tmux = Tmux()):
        self._filename = filename
        self._tmux = tmux

    def __str__(self):
        return 'Workspace[%s]' % self.name()

    def name(self):
        return os.path.basename(self._filename)

    def filename(self):
        return self._filename

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

# TODO Put this in its own file.
class LastAccessedIndex(object):
    INDEX_FILENAME = os.path.join(
                os.path.expanduser('~'),
                Workspace.WORKSPACE_DIR,
                '.order')

    def __init__(self):
        self._index = self._parse_index(LastAccessedIndex.INDEX_FILENAME)

    def _parse_index(self, filename):
        if not os.path.isfile(filename):
            return {}
        result = {}
        with open(filename) as f:
            for line in f.readlines():
                name, number = line.rstrip().split(':')
                result[name] = int(number)
        return result

    def now(self):
        return int(time.time())

    def sort(self, workspaces):
        def lookup(x):
            if self._index.has_key(x.filename()):
                return self._index[x.filename()]
            else:
                return 0

        def compare(x, y):
            return -cmp(lookup(x), lookup(y))

        result = workspaces[:]
        result.sort(compare)
        return result

    def touch(self, workspace):
        self._index[workspace.filename()] = self.now()
        self.save()

    def save(self):
        with open(LastAccessedIndex.INDEX_FILENAME, 'w') as f:
            lines = ["%s:%d\n" % (key, self._index[key])
                     for key in self._index.keys()]
            f.writelines(lines)
