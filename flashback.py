import sublime, sublime_plugin
import subprocess

class FlashbackCommand(sublime_plugin.WindowCommand):
    def run(self):
        git_log = subprocess.check_output("git log")
        print(git_log)
