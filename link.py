import re, os
import sublime, sublime_plugin

from .command import NpmCommand

class NpmLink(NpmCommand):
	package_names = []


class NpmLinkRegisterCommand(NpmLink, sublime_plugin.TextCommand):
	def run(self, edit):
		self.run_npm_and_show(['link'])


class NpmLinkUseCommand(NpmLink, sublime_plugin.TextCommand):
	def run(self, edit):
		# find where npm links packages
		code, prefix, err = self.run_npm(['config', 'get', 'prefix'])
		if prefix:
			# remove whitespace, such as trailing EOL chars, and normalize
			prefix = os.path.normpath(prefix.strip())
			# now list out the packages at `node_modules`
			# platform difference, see https://github.com/PixnBits/sublime-text-npm/issues/2#issuecomment-52543172
			if os.name == 'nt':
				module_dir = os.path.join(prefix, 'node_modules')
			else:
				module_dir = os.path.join(prefix, 'lib', 'node_modules')
			#self.output_textarea("module_dir: "+module_dir)
			# check for directories?
			self.package_names = []
			#TODO check to ensure dir exists
			for entry in os.listdir(module_dir):
				if os.path.isdir( os.path.join(module_dir, entry) ):
					self.package_names.append(entry)
					# could parse package.json to get version, etc
			# show our formatted results to the user
			window = sublime.active_window()
			window.show_quick_panel(self.package_names, self.link_package_index, sublime.MONOSPACE_FONT)
		elif err:
			self.output_textarea("error getting prefix config: \n"+config_text)
		else:
			self.output_textarea("prefix not found :'(\n"+config_text)


	def link_package(self, package_name):
		self.run_npm_and_show(['link', package_name])

	def link_package_index(self, index):
		if index < 0 or len(self.package_names) < 1:
			return
		package_name = self.package_names[index]
		self.link_package(package_name)