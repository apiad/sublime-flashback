import sublime, sublime_plugin
import os

class FlashbackCommand(sublime_plugin.WindowCommand):
    def run(self):
        def highlight(i):
            pass

        git_log = subprocess.check_output(['git', 'log', '--pretty=format:"[%h] %s%n%cD (%cr)%n%cN (%ce)---"']).split(b'---')
        items = [self.split(log) for log in git_log]
        items = [i for i in items if i]
        print("Git log response: {}".format(items))
        self.window.show_quick_panel(items, highlight)

    def split(self, log):
        parts = [l.decode().strip('"') for l in log.split(b"\n")]
        return [p for p in parts if p]
