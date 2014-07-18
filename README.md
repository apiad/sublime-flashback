# Flashback

A Sublime Text 3 plugin to quickly navigate a file's commit history.

### Disclaimer

This plugin is in active development, which means it can be absolutely broken. **Always** save your changes before using it, to avoid data losses. Use at your own risk.

## What does it do?

**Flashback** is a dead simple plugin. It opens up a list of all the commits for the current file, and updates the file content as you browse through the history.

I made this plugin to replace the standard **git log** command. Such command opens the log list, and when you select a commit, it opens the **diff** in a new window. I consider that feature to be absolutely useless. Instead, this plugin updates the **content** of your view with the content of the same file as it is stored in the selected commit. If you press `Escape` it will restore the content you had before running the plugin.

## Installing

Just use [Package Control](https://sublime.wbond.net).

## Using

When editing any file under a git repository, hit `ctrl+alt+f`, or hit `ctrl+shift+p` and find `Flashback` on the command list.
