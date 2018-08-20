__author__ = 'Oliver Bayer'
__copyright__ = 'Copyright (c) Oliver Bayer 2017'
__license__ = 'MIT'

import lldb
import os.path

lldb_init_search_path = "~/.lldb"

def __lldb_init_module(debugger, internal_dict):
  debugger.HandleCommand('br set -F "main" -o true')
  debugger.HandleCommand('br command add -s python 1 -o "trampoline.__breakpoint_callback()"')

  file_path = os.path.realpath(__file__)
  search_path = os.path.dirname(file_path)

  global lldb_init_search_path
  lldb_init_search_path = search_path

  print("Trampoline has been set up and will load target/architecture dependent lldb init files.")

def set_search_path(search_path):
  """Set the search path that __name__ will use to look for arch/target dependent lldb init files"""
  global lldb_init_search_path
  lldb_init_search_path = search_path

def __load_lldb_files():
  """Loads lldb files depending on current target/architecture"""
  target = lldb.debugger.GetSelectedTarget()

  for file_path in __resolve_file_paths(target, lldb_init_search_path):
    __load_lldb_file(file_path)

def __load_lldb_file(file_path):
  """Loads lldb commands from file_path"""
  print('** Looking for lldb extensions at: {} **'.format(file_path))

  if os.path.isfile(file_path):
    print('** Found **')
    lldb.debugger.HandleCommand('command source -s true {}'.format(file_path))
  else:
    print('** Not found **')

def __resolve_file_paths(target, search_path):
  """Returns a list of resolved lldb init file paths according to current target"""
  filename = __executable_name(target).replace(" ", "_")
  architecture = __architecture(target)

  return list(map(lambda name: os.path.join(os.path.expanduser(search_path), name), ['{}.lldb'.format(filename), '{}-{}.lldb'.format(filename, architecture)]))

def __architecture(target):
  """Returns architecture for current active target, e.g. i386, x86_64, armv7"""
  return target.module_iter().next().GetTriple().split('-', 1)[0]

def __executable_name(target):
  """Returns the filename of the current target"""
  return target.GetExecutable().GetFilename().lower()

def __breakpoint_callback():
  __load_lldb_files()
  lldb.debugger.GetSelectedTarget().GetProcess().Continue()
