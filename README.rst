===========
gogo-gadget
===========

A tool to aggregate custom command line tools into one.

It can thus serve as a
single entry point into a local ecosystem of tools and scripts. It is of course
inspired by https://en.wikipedia.org/wiki/Inspector_Gadget.

Instead of remembering obscure script names or command line tool names with possibly
even more obscure options, one can simply create a `gogo` file containing the
whole command and some more memorable command name. In contrast to bash aliases
an command can be split into several word tokens, e.g. `gogo cleanup conda`.
Thanks to support for autocompletion in the bash (<TAB> <TAB>), it is even
simpler to access the required commands.

Furthermore, help or a very short documentation can be included.

How does it work?
-----------------

On startup `gogo-gadget` loads a `gogo` file by default from `~/.gogo.yml`. It then
creates a command line interface on the fly using the `click` python library
(http://click.pocoo.org).


Installation
------------

It is recommended to use `pipsi` https://github.com/mitsuhiko/pipsi to install
`gogo-gadget`. Once `pipsi` is installed, run::

  pipsi install gogo-gadget

A `pip install gogo-gadget` would also work in principle, however, gogo would
need to be installed in all virtual environments used.

To enable tab autocompletion in the bash, add the following to `.bashrc`::

  eval "$(_GOGO_COMPLETE=source gogo)"


Example gogo File
-----------------

Gogo files are written in YAML.

See below a few command examples along with the corresponding YAML file.

Commands:

.. code-block:: bash

  gogo start foo
  gogo update
  gogo cleanup conda
  gogo cleanup conda -y
  gogo cleanup foo

Gogo file:

.. code-block:: yaml

   cleanup:
     conda:
       cmd: conda clean --all
       help: Remove obsolete files in current conda env
     foo:
       cmd: example_command
       help: doing some other sort cleanups
   start:
     foo:
       cmd: docker run -it --rm foo/foo:latest command_in_docker
       help: complicated docker command
   update:
     cmd: apt-get update && apt-get upgrade
     help: updating software on ubuntu
