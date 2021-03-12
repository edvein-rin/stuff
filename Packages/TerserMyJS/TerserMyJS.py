import subprocess
import os
import io

import sublime_plugin


class TerserCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        file_name = self.view.file_name()

        if '.js' in file_name:
            self.minify_js()
        elif '.coffee' in file_name:
            self.minify_coffee()

    def minify_coffee(self):
        input_file_name = self.view.file_name()
        output_file_name = input_file_name.replace('.coffee', '.min.js')

        # Coffee to JS
        command = ['coffee', '-b', '--compile', input_file_name]
        proc = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE)

        for line in io.TextIOWrapper(proc.stderr, encoding="utf-8"):
            print(line)

        # JS to Min JS
        command = ['terser', input_file_name.replace('.coffee', '.js'), '-o', output_file_name]
        proc = subprocess.Popen(command, shell=True)
        proc.communicate()

        os.remove(input_file_name.replace('.coffee', '.js'))

    def minify_js(self):
        input_file_name = self.view.file_name()
        output_file_name = input_file_name.replace('.js', '.min.js')

        command = ['terser', input_file_name, '-o', output_file_name]
        subprocess.Popen(command, shell=True)
