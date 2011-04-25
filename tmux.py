import os

class Tmux(object):
    def __init__(self):
        pass

    def running(self):
        return self._exec('list-sessions') == 0

    def has_session(self, session_name):
        return self._exec('has-session -t %s' % session_name) == 0

    def attach(self, session_name, workspace, dir='.'):
        if self.has_session(session_name):
            self._exec('attach -t %s' % session_name, dir)
        else:
            self._exec('new -s %s "vim %s"' % (session_name, workspace), dir)

    def has_sessions(self, session_name):
        return self._exec('list-sessions | grep %s' % session_name) == 0

    def _exec(self, tmux_command, dir='.'):
        return os.system('(cd %s && tmux %s) 1>/dev/null 2>&1' % (dir, tmux_command))
