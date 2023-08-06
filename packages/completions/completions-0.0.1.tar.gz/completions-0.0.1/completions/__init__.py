#!/usr/bin/env python
"""
Generate completions for shells
"""
import re
import sys
import uuid
import warnings
from os import path, sep, rename
from simpleconf import Config
from completions.templates import assembleBashWithCommands, assembleBashWithoutCommands, \
	assembleFishWithCommands, assembleFishWithoutCommands, \
	assembleZshWithCommands, assembleZshWithoutCommands


def checkOptname(optname):
	"""Send warning if necessary"""
	if optname.startswith('--') and len(optname) <= 3:
		warnings.warn('Long option %r specified, but the name has length < 2' % optname)
	if optname.startswith('-') and not optname.startswith('--') and len(optname) > 2:
		warnings.warn('Short option %r specified, but the name has length > 1' % optname)

def log(msg, *args):
	"""simple log on the screen"""
	sys.stderr.write('- %s\n' % (msg % args))

class CompletionsLoadError(Exception):
	"""Raises while failed to load completions from configuration file"""

class Command:
	"""A command"""
	def __init__(self, name, desc, options = None):
		self.name = name
		self.desc = desc
		self.options = options or {}

	def addOption(self, opt, desc):
		self.options[opt] = desc

class Completions(Command):

	def __init__(self, name = None, desc = None, options = None, fullpath = None):
		super(Completions, self).__init__(name, desc, options)
		self.name = name or sys.argv[0]
		self.desc = desc or ''
		self.commands = {}
		self.uid      = None
		self.fullpath = fullpath and path.realpath(fullpath)

		if sep in self.name:
			self.fullpath = self.fullpath or path.realpath(self.name)
			self.name = path.basename(self.name)

	@property
	def availname(self):
		"""Make an available for function name"""
		return re.sub(r'[^\w_]+', '_', path.basename(self.name))

	def addCommand(self, name, desc, options = None):
		self.commands[name] = Command(name, desc, options)

	def command(self, name):
		return self.commands[name]

	def _automateFish(self, source):
		compfile = path.expanduser('~/.config/fish/completions/%s.fish' % self.name)
		backfile = compfile + '.completions.bak'
		if path.isfile(compfile):
			log('Completion file exists: %r', compfile)
			log('Back it up to: %r', backfile)
			rename(compfile, backfile)
		log('Writing completion code to: %r', compfile)
		with open(compfile, 'w') as fcomp:
			fcomp.write(source)
		log('Done, you may need to restart your shell in order for the changes to take effect.')

	def _automateBash(self, source):
		pass

	def _automateZsh(self, source):
		pass

	def _generateBash(self):
		if self.commands:
			return assembleBashWithCommands(
				[self.name, self.fullpath],
				'_%s_%s_complete' % (self.availname, self.uid),
				self.options,
				self.commands)
		return assembleBashWithoutCommands(
			[self.name, self.fullpath],
			'_%s_%s_complete' % (self.availname, self.uid),
			self.options)

	def _generateFish(self):
		if self.commands:
			return assembleFishWithCommands(
				self.name,
				'_%s_%s_complete' % (self.availname, self.uid),
				self.options,
				self.commands)
		return assembleFishWithoutCommands(
			self.name,
			'_%s_%s_complete' % (self.availname, self.uid),
			self.options)

	def _generateZsh(self):
		if self.commands:
			return assembleZshWithCommands(
				[self.name, self.fullpath],
				'_%s_%s_complete' % (self.availname, self.uid),
				self.options,
				self.commands)
		return assembleZshWithoutCommands(
			[self.name, self.fullpath],
			'_%s_%s_complete' % (self.availname, self.uid),
			self.options)

	def generate(self, shell, auto = False):
		self.uid = str(uuid.uuid3(uuid.NAMESPACE_DNS, self.name)).split('-')[-1]
		if shell == 'fish':
			source = self._generateFish()
			if not auto:
				return source
			self._automateFish(source)
		elif shell == 'bash':
			source = self._generateBash()
			if not auto:
				return source
			self._automateBash(source)
		elif shell == 'zsh':
			source = self._generateZsh()
			if not auto:
				return source
			self._automateZsh(source)
		else:
			raise ValueError('Currently only bash, fish and zsh supported.')

	def load(self, dict_var):
		# integrity check
		if 'program' not in dict_var:
			raise CompletionsLoadError("No 'program' key found.")

		program = dict_var['program']
		if 'name' not in program:
			raise CompletionsLoadError("A program name should be given by 'program.name'")
		self.name = program['name']
		self.desc = program['desc']
		if sep in self.name:
			self.fullpath = path.realpath(self.name)
			self.name = path.basename(self.name)

		for key, val in program.get('options', {}).items():
			self.addOption(key, val)

		commands = dict_var.get('commands', '')
		for key, val in commands.items():
			self.addCommand(
				name = key,
				desc = val.get('desc') or '',
				options = val.get('options', {})
			)

	def loadFile(self, compfile):
		config = Config(with_profile = False)
		config._load(compfile)
		self.load(config)

def main():
	"""Entry point of the script"""
	from pyparam import commands
	commands._.shell.desc     = 'The shell, one of bash, fish and zsh.'
	commands._.shell.required = True
	commands._.auto           = False
	commands._.auto.desc      = [
		'Automatically write completions to destination file:',
		'Bash: `~/bash_completion.d/<name>.bash-completion`',
		'  Also try to source it in ~/.bash_completion',
		'Fish: `~/.config/fish/completions/<name>.fish`',
		'Zsh:  `~/.zfunc/_<name>`',
		'  `fpath+=~/.zfunc` is ensured to add before `compinit`'
	]
	commands._.a                  = commands._.auto
	commands._.s                  = commands._.shell
	commands.self                 = 'Generate completions for myself.'
	commands.self._hbald          = False
	commands.generate             = 'Generate completions from configuration files'
	commands.generate.config.desc = [
		'The configuration file. Scheme should be aligned following json data:',
		'{',
		'	"program": {',
		'		"name": "program",',
		'		"desc": "A program",',
		'		"options": {',
		'			"-o": "Output file",',
		'			"--output": "Long version of -o"',
		'		}',
		'	},',
		'	"commands": {',
		'		"list": {',
		'			"desc": "List commands",',
		'			"options": {',
		'				"-a": "List all commands",',
		'				"--all": "List all commands"',
		'			}',
		'		}',
		'	}',
		'}',
		'',
		'Configuration file that is supported by `python-simpleconf` is supported.'
	]
	commands.generate.config.required = True
	commands.generate.c = commands.generate.config
	command, options, goptions = commands._parse()

	auto = goptions['auto']
	if command == 'self':
		source = commands._complete(goptions['shell'], auto = auto)
		if not auto:
			print(source)
	else:
		completions = Completions()
		completions.loadFile(options['config'])
		source = completions.generate(goptions['shell'], auto = auto)
		if not auto:
			print(source)

if __name__ == '__main__':
	main()
