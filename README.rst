NAME

::

   LIBPRG - program library


DESCRIPTION

::



   LIBPRG is a python3 library providing all the tools to create a
   unix command line program, such as disk perisistence for
   configuration files, event handler to handle the client/server
   connection, code to introspect modules for commands, a parser to
   parse commandline options and values, etc.

   LIBPRG is a contribution back to society and is Public Domain.


SYNOPSIS

::

   >>> from prg.object import *
   >>> o = Object()
   >>> o.a = "b"
   >>> write(o, "test")
   >>> oo = Object()
   >>> read(oo, "test")
   >>> oo
   {"a": "b"}  


INSTALL

::

   $ pip install libprg


AUTHOR

::

  libbot <libbotx@gmail.com>


COPYRIGHT

::

   LIBPRG is placed in the Public Domain.
