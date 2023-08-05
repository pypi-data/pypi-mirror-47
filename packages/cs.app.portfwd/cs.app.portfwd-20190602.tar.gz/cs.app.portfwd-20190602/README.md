Manage persistent ssh tunnels and port forwards.


Manage persistent ssh tunnels and port forwards.

Portfwd runs a collection of ssh tunnel commands persistently,
each in its own `cs.app.svcd <https://pypi.org/project/cs.app.svcd>`_ instance
with all the visibility and process control that SvcD brings.

It reads tunnel preconditions from special comments within the ssh config file.
It uses the configuration options from the config file
as the SvcD signature function
thus restarting particular ssh tunnels when their specific configuration changes.
It has an "automatic" mode (the -A option)
which monitors the desired list of tunnels
from statuses expressed via `cs.app.flag <https://pypi.org/project/cs.app.flag>`_
which allows live addition or removal of tunnels as needed.

## Function `Condition(portfwd, op, invert, *args)`

Factory to construct a condition from a specification.

## Class `FlagCondition`

MRO: `_PortfwdCondition`  
A flag based condition.

## Function `main(argv=None, environ=None)`

Command line main programme.

## Class `PingCondition`

MRO: `_PortfwdCondition`  
A ping based condition.

## Class `Portfwd`

MRO: `cs.app.flag.FlaggedMixin`  
An ssh tunnel built on a SvcD.

### Method `Portfwd.__init__(self, target, ssh_config=None, conditions=(), test_shcmd=None, trace=False, verbose=False, flags=None)`

Initialise the Portfwd.

Parameters:
* `target`: the tunnel name, and also the name of the ssh configuration used
* `ssh_config`: ssh configuration file if not the default
* `conditions`: an iterable of `Condition`s
  which must hold before the tunnel is set up;
  the tunnel also aborts if these cease to hold
* `test_shcmd`: a shell command which must succeed
  before the tunnel is set up;
  the tunnel also aborts if this command subsequently fails
* `trace`: issue tracing messages; default `False`
* `verbose`: be verbose; default `False`
* `flags`: optional preexisting `Flags` instance

## Class `Portfwds`

A collection of Portfwd instances and associated control methods.
