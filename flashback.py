import sublime, sublime_plugin
import os
import subprocess
import threading
import datetime
import time


def async(function):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=function, args=args, kwargs=kwargs)

        try:
            thread.start()
            return thread
        except Exception as e:
            print(str(e))

    return wrapper


class Loader:
    def __init__(self, msg):
        self.msg = msg
        self.stop = False

    def __enter__(self):
        self.run()

    def __exit__(self, _type, _value, _traceback):
        self.stop = True

    @async
    def run(self):
        count = 0

        chars = "◒◑◓◐"

        while not self.stop:
            load = chars[count % 4]
            sublime.status_message("Flashback :: " + self.msg +
                                   " " + load)
            time.sleep(0.1)
            count += 1

        sublime.status_message("")


def loading(msg):
    return Loader(msg)


class FlashbackCommand(sublime_plugin.TextCommand):
    @async
    def run(self, edit):
        current_content = self.view.substr(sublime.Region(0, self.view.size()))
        items = []

        base = self.find_git_root(self.view.file_name())

        if base is None:
            sublime.status_message("This file is not in version control")

        path = self.view.file_name()[len(base):]

        if path[0] == '/':
            path = path[1:]

        with loading("Processing history"):
            git_log = subprocess.check_output(['git', 'log', '--pretty=format:"%s%n'
                                                             '[%h] %cN (%ce)%n%cD (%cr)---"',
                                               self.view.file_name()])
            git_log = git_log.split(b'---')

            now = str(datetime.datetime.now()) + " (Present)"

            items = [self.split(log) for log in git_log]
            items = [['HEAD', '', now]] + [i for i in items if i]

        def get_commit(i):
            return items[i][1].split()[0][1:-1]

        def checkout(i):
            if i < 0:
                self.view.run_command('replace_content', {'text': current_content})
                return

        def show_diff(i):
            if i < 0:
                return

            if i == 0:
                self.view.run_command('replace_content', {'text': current_content})
                return

            commit = get_commit(i)
            diff = subprocess.check_output(['git', 'show', '--encoding=utf8', commit + ":" + path])

            self.view.run_command('replace_content', {'text': diff.decode('utf8')})

        sublime.active_window().show_quick_panel(items, checkout, 0, 0, show_diff)

    def split(self, log):
        parts = [l.decode().strip('"') for l in log.split(b"\n")]
        return [p for p in parts if p]

    def find_git_root(self, fn):
        while fn != "/":
            if os.path.exists(os.path.join(fn, '.git')):
                return fn

            fn = os.path.abspath(os.path.join(fn, '..'))

        return None


class ReplaceContentCommand(sublime_plugin.TextCommand):
    def run(self, edit, text):
        self.view.replace(edit, sublime.Region(0, self.view.size()), text)
