import sublime, sublime_plugin
import os

class FlashbackCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        git_log = subprocess.check_output(['git', 'log', '--pretty=format:"[%h]  '
                                                         '%s%n%cD (%cr)%n%cN (%ce)---"',
                                           self.view.file_name()])
        git_log = git_log.split(b'---')

        items = [self.split(log) for log in git_log]
        items = [i for i in items if i]

        def checkout(i):
            if i < 0:
                return

            commit = items[i][0].split()[0][1:-1]
            os.system('git checkout {} {}'.format(commit, self.view.file_name()))

        def show_diff(i):
            pass

        sublime.active_window().show_quick_panel(items, checkout, 0, 0, show_diff)

    def split(self, log):
        parts = [l.decode().strip('"') for l in log.split(b"\n")]
        return [p for p in parts if p]
