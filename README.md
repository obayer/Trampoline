Trampoline
==========

`Trampoline` is a lldb module that loads `.lldbinit` files depending on current active target.

## Motivation
Sometimes you might have breakpoints, watchpoints, or additional lldb commands in your `.lldbinit` that don't fit
for your current executable or don't fit your current architecture. `Trampoline` will load additional `.lldbinit` files according to your current executable and architecture.

## File name scheme
`Trampoline` will search for `.lldbinit` files named: [`executable.lldb`, `executable-arch.lldb`] per default within the same directory `trampoline.py` is in.

E.g. your executable is named `example` and you are running `lldb` on a x86_64 machine. `Trampoline` will search for `example.lldb` (used for architecture independent lldb commands) and `example-x86_64.lldb` (lldb commands that only work on that specific architecture) and load them if available.

## Installation
Copy the `trampoline.py` file somewhere onto your machine and insert into your `~/.lldbinit` file following line:

```Python
# ~/.lldbinit
command script import /path/to/your/trampoline.py
```

## Search path
Per default, `Trampoline` is searching for `*.lldb` files within the directory where `trampoline.py` is located.
To change the `search path` insert into your `/.lldbinit` file following line:
```Python
# ~/.lldbinit
script trampoline.lldb_files_search_path = '~/your/new/search/path/lldb'
```

## Disable automatic `*.lldb` file loading
Currently there seems to be a bug within `lldb` which prevents `Trampolines` automatic execution on startup, if `lldb` is run via terminal, if executed in Xcode everything works as usual.  
To temporarily bypass this unexpected behaviour you can disable automatically loading of `.lldb` files via
```Python
# ~/.lldbinit
script trampoline.disable_automatic_load = True
```

## Commands

Commands avaiable after enabling `Trampoline`.

### `tr_load`
To manually load `*.lldb` files during a lldb debug session, you can enter `tr_load` into your lldb command line interpreter, which loads the desired `*.lldb` files as described in [File name scheme](#file-name-scheme).
