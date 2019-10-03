__author__ = 'Oliver Bayer'
__copyright__ = 'Copyright (c) Oliver Bayer 2017'
__license__ = 'MIT'

import lldb
import os.path

lldb_files_search_path = "~/.lldb"
disable_automatic_load = False

def __lldb_init_module(debugger, internal_dict):
  debugger.HandleCommand('command script add -f trampoline.tr_load tr_load')

  debugger.HandleCommand('br s -n "main" -o true -N tr_brk_inject')
  debugger.HandleCommand('br s -n "dyldbootstrap::start" -s dyld -o true -N tr_brk_inject')

  debugger.HandleCommand('br command add -s python 1 -o "trampoline._breakpoint_callback()"')
  debugger.HandleCommand('br command add -s python 2 -o "trampoline._breakpoint_callback()"')

  file_path = os.path.realpath(__file__)
  search_path = os.path.dirname(file_path)

  global lldb_files_search_path
  lldb_files_search_path = search_path

  print("** Trampoline has been set up and will load target/architecture dependent lldb init files. **")

def tr_load(debugger, command, result, internal_dict):
  """Loads plattform/executable dependent .lldb files, e.g. executable.lldb, executable-86_64.lldb"""
  lldb.debugger.HandleCommand('br del tr_brk_inject')
  _load_lldb_files()

def _load_lldb_files():
  """Loads lldb files depending on current target/architecture"""
  target = lldb.debugger.GetSelectedTarget()

  for file_path in _resolve_file_paths(target, lldb_files_search_path):
    _load_lldb_file(file_path)

def _load_lldb_file(file_path):
  """Loads lldb commands from file_path"""
  print('** Looking for lldb extensions at: {} **'.format(file_path))

  if os.path.isfile(file_path):
    print('** Found **')
    lldb.debugger.HandleCommand('command source -s true \"{}\"'.format(file_path))
  else:
    print('** Not found **')

def _resolve_file_paths(target, search_path):
  """Returns a list of resolved lldb init file paths according to current target"""
  filename = _executable_name(target).replace(" ", "_")
  architecture = _architecture(target)

  return list(map(lambda name: os.path.join(os.path.expanduser(search_path), name), ['{}.lldb'.format(filename), '{}-{}.lldb'.format(filename, architecture)]))

def _architecture(target):
  """Returns architecture for current active target, e.g. i386, x86_64, armv7"""
  return target.GetTriple().split('-', 1)[0]

def _plattform(target):
  """Returns plattform for current active target, e.g. apple-macosx10.10.0"""
  return target.GetTriple().split('-', 1)[1]

def _executable_name(target):
  """Returns the filename of the current target"""
  return target.GetExecutable().GetFilename().lower()

def _breakpoint_callback():
  lldb.debugger.HandleCommand('br del tr_brk_inject')

  global disable_automatic_load
  if disable_automatic_load:
    print('** Automatic injection disabled **')
    return

  _load_lldb_files()
  lldb.debugger.GetSelectedTarget().GetProcess().Continue()
