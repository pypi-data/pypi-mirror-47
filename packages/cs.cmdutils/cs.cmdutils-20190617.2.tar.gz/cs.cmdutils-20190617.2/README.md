convenience functions for working with the Cmd module and other command line related stuff




## Class `BaseCommand`

A base class for handling nestable command lines.

This class provides the basic parse and dispatch mechanisms
for command lines.
To implement a command line
one instantiates a subclass of BaseCommand:

  class MyCommand(BaseCommand):
    GETOPT_SPEC = 'ab:c'
  ...
  the_cmd = MyCommand()

Running a command is done by:

  the_cmd.run(argv)

The subclass is customised by overriding the following methods:
* `apply_defaults(options)`:
  prepare the initial state of `options`
  before any command line options are applied
* `apply_opts(options,opts)`:
  apply the `opts` to `options`.
  `opts` is an option value mapping
  as returned by `getopot.getopt`.
* `cmd_`*subcmd*`(argv,options)`:
  if the command line options are followed by an argument
  whose value is *subcmd*,
  then method `cmd_`*subcmd*`(argv,options)`
  will be called where `argv` contains the command line arguments
  after *subcmd*.
* `main(argv,options)`:
  if there are no command line aguments after the options
  or the first argument does not have a corresponding
  `cmd_`*subcmd* method
  then method `main(argv,options)`
  will be called where `argv` contains the command line arguments.
* `run_context(argv,options,cmd=None)`:
  a context manager to provide setup or teardown actions
  to occur before and after the command implementation respectively.
  If the implementation is a `cmd_`*subcmd* method
  then this is called with `cmd=`*subcmd`;
  if the implementation is `main`
  then this is called with `cmd=None`.

To aid recursive use
it is intended that all the per command state
is contained in the `options` object
and therefore that in typical use
all of `apply_opts`, `cmd_`*subcmd*`, `main` and `run_context`
should be static methods making no reference to `self`.

Editorial: why not arparse?
Primarily because when incorrectly invoked
an argparse command line prints the help/usage messgae
and aborts the whole programme with `SystemExit`.

### Method `BaseCommand.__init__(self, getopt_spec=None)`

Initialise the BaseCommand.

Parameters:
* `getopt_spec`: optional `getopt.getopt` compatible
  option specifier.
  The default comes from the class' `.GETOPT_SPEC` attribute.

## Function `docmd(dofunc)`

Decorator for Cmd subclass methods
to supply some basic quality of service.

This decorator:
- wraps the function call in a `cs.pfx.Pfx` for context
- intercepts `getopt.GetoptError`s, issues a `warning`
  and runs `self.do_help` with the method name,
  then returns `None`
- intercepts other `Exception`s,
  issues an `exception` log message
  and returns `None`

The intended use is to decorate `cmd.Cmd` `do_`* methods:

  @docmd
  def do_something(...):
    ... do something ...
