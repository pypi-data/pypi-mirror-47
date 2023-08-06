# pdbme - remote active debugger based on rpdb

This is active fork of https://github.com/tamentis/rpdb. 

Rpdb is a wrapper around pdb that re-routes stdin and stdout to a socket
handler. 

Pdbme is Rpdb, which is active. Which means, that while Rpdb open port and waits until you connect to this port, Pdbme connects to your port. 

So, in other words, you open pdbme-cli tool, ask your app "pdb me please" and your app will pdb you :). 

## Why active?

Rpdb opens debugger pon port (default 4444), but it has many drawbacks. Eg - it cannot be used in mutlithreaded or multiprocessing application. Even in non-parallel app, port can be occupied a little while after closing it and app will break trying to open it again. 

Calling your terminal sounds way better way. It's useful when you want to debug app which can break
simultaneously more than once in a time, and passive mode will refuse to open
port 4444 again.

Solution to the problem is:

    # default host is 127.0.0.1 and default port is 4444
    import pdbme; pdbme.set_trace()

or, in more complex case, eg. when it's running in other host, in your docker, or sth like that

    import pdbme
    pdbme.set_trace(host='192.168.1.120', port=12345)

You should have pdbme-cli running on other side of your communication. 

### pdbme-cli

pdbme-cli is a simple tool, using tmux, tcpwrapper and socat to accept incoming
connections and spawn tmux session for each incoming breakpoint. 

 * tcpwrapper comes from https://cr.yp.to/ucspi-tcp.html (available in many distros and in MacOS brew)
 * socat - http://www.dest-unreach.org/socat/


Installation in CPython (standard Python)
-----------------------------------------

 ~~pip install pdbme~~ (not yet on PyPi)

or
    
    pip install git+https://github.com/mahomahomaho/pdbme


Trigger rpdb with signal
------------------------

`set_trace()` can be triggered at any time by using the TRAP signal handler.
This allows you to debug a running process independantly of a specific failure
or breakpoint::

    import pdbme
    pdbme.handle_trap()

    # As with set_trace, you can optionally specify addr and port
    rpdb.handle_trap(host="0.0.0.0", port=4441)

Calling `handle_trap` will overwrite the existing handler for SIGTRAP if one has
already been defined in your application.

Author(s)
---------

Łukasz Mach <maho@pagema.net> - http://pagema.net/

based on work of rpdb author:
Bertrand Janin <b@janin.com> - http://tamentis.com/ 

and rpdbs contributors: (chronological, latest first):

 - Cameron Davidson-Pilon - @CamDavidsonPilon
 - Pavel Fux - @fuxpavel
 - Ken Manheimer - @kenmanheimer
 - Steven Willis - @onlynone
 - Jorge Niedbalski R <niedbalski@gmail.com>
 - Cyprien Le Pannérer <clepannerer@edd.fr>
 - k4ml <kamal.mustafa@gmail.com>
 - Sean M. Collins <sean@coreitpro.com>
 - Sean Myers <sean.myers@redhat.com>
