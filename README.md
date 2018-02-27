Trampoline
==========

`Trampoline` is a lldb module that loads _lldb.init_ files depending on current active target.

## Motivation
Sometimes you might have breakpoints, watchpoints, or additional lldb commands in your `lldb.init` that don't fit
for your current executable or don't fit your current architecture. `trampoline` will load additional `lldb.init` files according to your current executable and architecture.

## File name scheme
`trampoline` will search for `lldb.init` files named: [`executable.lldb`, `executable-arch.lldb`] per default within the same directory `trampoline.py` is in.

E.g. your executable is named `example` and you are running `lldb` on a x86_64 machine. `trampoline` will look for `example.lldb` (used for architecture independent lldb commands) and `example-x86_64.lldb` (lldb commands that only work on that specific architecture).

## Installation
Copy the `trampoline.py` file somewhere onto your machine and insert into your `~/.lldbinit` file following line:

```Python
# ~/.lldbinit
command script import /path/to/your/trampoline.py
```

To change the `search path` insert into your `/.lldbinit` file following line:
```Python
# ~/.lldbinit
script trampoline.set_search_path('~/your/new/search/path/lldb')
```
