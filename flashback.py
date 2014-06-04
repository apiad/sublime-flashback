import sublime, sublime_plugin
import os

class FlashbackCommand(sublime_plugin.WindowCommand):
    def run(self):
        def highlight(i):
            pass

        git_log = subprocess.check_output(['git', 'log', '--pretty=format:"[%h] %s %n%cr by %cN (%ce)"'])
        self.window.show_quick_panel(git_log, highlight)
