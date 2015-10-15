import sublime, sublime_plugin
import os
from subprocess import Popen
import winreg

WINMERGE = winreg.QueryValue(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\WinMergeU.exe')

if not WINMERGE:
	if os.path.exists("%s\WinMerge\WinMergeU.exe" % os.environ['ProgramFiles(x86)']):
		WINMERGE = '"%s\WinMerge\WinMergeU.exe"' % os.environ['ProgramFiles(x86)']
	else:
		WINMERGE = '"%s\WinMerge\WinMergeU.exe"' % os.environ['ProgramFiles']

fileA = fileB = None

def recordActiveFile(f):
	global fileA
	global fileB
	fileB = fileA
	fileA = f

def getWindowFile():
	global fileA
	global fileB
	for f in sublime.active_window().views():
		if (fileA == None) and (f.file_name() != fileB):
			fileA = f.file_name()
		if (fileB == None) and (f.file_name() != fileA):
			fileB = f.file_name()

class WinMergeCommand(sublime_plugin.ApplicationCommand):

	def run(self):
		if (fileA == None) or (fileB == None):
			getWindowFile()
		cmd_line = '%s /e /ul /ur "%s" "%s"' % (WINMERGE, fileA, fileB)
		print("WinMerge command: " + cmd_line)
		Popen(cmd_line)

class WinMergeFileListener(sublime_plugin.EventListener):
	def on_activated(self, view):
		if view.file_name() != fileA:
			recordActiveFile(view.file_name())
