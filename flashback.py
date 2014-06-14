import sublime, sublime_plugin
import os
import subprocess


class FlashbackCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        git_log = subprocess.check_output(['git', 'log', '--pretty=format:"%s%n'
                                                         '[%h] %cN (%ce)%n%cD (%cr)---"',
                                           self.view.file_name()])
        git_log = git_log.split(b'---')

        items = [self.split(log) for log in git_log]
        items = [i for i in items if i]

        def get_commit(i):
            return items[i][1].split()[0][1:-1]

        def checkout(i):
            if i < 0:
                return

            commit = get_commit(i)
            cmd = 'git checkout {} {}'.format(commit, self.view.file_name())
            print("Flashback :: Executing %s" % cmd)
            # os.system(cmd)

        def show_diff(i):
            if i < 0:
                return

            commit = get_commit(i)
            path = os.path.basename(self.view.file_name())
            diff = subprocess.check_output(['git', 'show', commit + ":" + path])

            self.view.run_command('replace_content', {'text': diff})

        sublime.active_window().show_quick_panel(items, checkout, 0, 0, show_diff)

    def split(self, log):
        parts = [l.decode().strip('"') for l in log.split(b"\n")]
        return [p for p in parts if p]


class ReplaceContentCommand(sublime_plugin.TextCommand):
    def run(self, edit, text):
        self.view.replace(edit, sublime.Region(0, self.view.size()), text)
