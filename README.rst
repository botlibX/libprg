NAME
####

::

 LIBPRG - program library


DESCRIPTION
===========

::

 LIBPRG is a python3 library implementing the 'prg' package. It
 provides all the tools to program a bot, such as disk perisistence
 for configuration files, event handler to handle the client/server
 connection, code to introspect modules for commands, deferred
 exception handling to not crash on an error, a parser to parse
 commandline options and values, etc.

 LIBPRG provides a demo bot, it can connect to IRC, fetch and
 display RSS feeds, take todo notes, keep a shopping list
 and log text. You can also copy/paste the service file and run
 it under systemd for 24/7 presence in a IRC channel.

 LIBPRG is a contribution back to society and is Public Domain.


SYNOPSIS
========

::

 prg <cmd> [key=val] 
 prg <cmd> [key==val]
 prg [-c] [-d] [-v] [-i]


INSTALL
=======

::

 pipx install libprg


USAGE
=====


default action is doing nothing::

 $ prg
 $

first argument is a command::

 $ prg cmd
 cfg,cmd,dlt,dne,dpl,fnd,log,met,mod,mre,
 nme,pwd,rem,rss,sts,tdo,thr,ver

starting a console requires an option::

 $ prg -c
 >

list of modules::

 $ prg mod
 bsc,err,flt,irc,log,mod,rss,shp,sts,tdo,
 thr,udp

to start the prg as daemon::

 $ prg -d
 $ 

add -v if you want to have verbose logging::

 $ prg -cv
 PRG started Wed Nov 8 15:38:56 2023 CVI
 >


CONFIGURATION
=============


irc configuration is done with the cli interface
using the ``cfg`` command::

 $ prg cfg server=<server>
 $ prg cfg channel=<channel>
 $ prg cfg nick=<nick>

sasl need a nickserv nick/password pair to generate
a password for sasl::

 $ prg pwd <nsnick> <nspass>
 $ prg cfg password=<frompwd>

rss has several configuration commands::

 $ prg rss <url>
 $ prg dpl <url> <item1,item2>
 $ prg rem <url>
 $ prg nme <url> <name>


COMMANDS
========

here is a list of the most basic commands::

 cfg - irc configuration
 cmd - commands
 dlt - remove a user
 dne - mark todo as done
 dpl - sets display items
 fnd - find objects 
 log - log some text
 met - add a user
 mre - displays cached output
 nme - display name of a feed
 pwd - sasl nickserv name/pass
 rem - removes a rss feed
 rss - add a feed
 sts - show status
 tdo - add todo item
 thr - show the running threads


SYSTEMD
=======

save the following it in /etc/systems/system/prgd.service and
replace "<user>" with the user running pipx::

 [Unit]
 Description=program library
 Requires=network.target
 After=network.target

 [Service]
 Type=simple
 User=<user>
 Group=<user>
 WorkingDirectory=/home/<user>/.prg
 ExecStart=/home/<user>/.local/pipx/venvs/libprg/bin/prg -d
 RemainAfterExit=yes

 [Install]
 WantedBy=multi-user.target

then run this::

 sudo systemctl enable prgd --now

 default channel/server is #bot on localhost


FILES
=====

::

 ~/.prg
 ~/.local/bin/prg
 ~/.local/bin/prgd
 ~/.local/pipx/venvs/libprg/


AUTHOR
======

::

 libbot <libbotx@gmail.com>


COPYRIGHT
=========

::

 LIBPRG is a contribution back to society and is Public Domain.
