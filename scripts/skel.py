__AUTHOR__ = "hugsy"
__VERSION__ = 0.2

import os
import tempfile

TEMPLATE="""#!/usr/bin/env python3
import sys, os
from pwn import *
context.update(
    arch="{arch}",
    endian="{endian}",
    os="linux",
    log_level="debug",
    terminal=["tmux", "split-window", "-h", "-p 65"],
)

REMOTE = False
TARGET=os.path.realpath("{filepath}")
elf = ELF(TARGET)

def attach(r):
    if not REMOTE:
        bkps = {bkps}
        cmds = []
        gdb.attach(r, '\\n'.join(["break {{}}".format(x) for x in bkps] + cmds))
    return

def exploit(r):
    attach(r)
    # r.sendlineafter(b"> ", b"HelloPwn" )
    r.interactive()
    return

if __name__ == "__main__":
    if len(sys.argv)==2 and sys.argv[1]=="remote":
        REMOTE = True
        r = remote("{target}", {port})
    else:
        REMOTE = False
        r = process([TARGET,])
    exploit(r)
    exit(0)
"""


class ExploitTemplateCommand(GenericCommand):
    """Generates a exploit template."""
    _cmdline_ = "exploit-template"
    _syntax_  = "{:s} [local|remote TARGET:PORT]".format(_cmdline_)
    _aliases_ = ["skeleton", ]

    @only_if_gdb_running
    def do_invoke(self, args):
        if len(args) < 1:
            self.usage()
            return

        scope = args[0].lower()
        if scope not in ("local", "remote"):
            self.usage()
            return

        target, port = "127.0.0.1", "1337"
        if scope == "remote":
            if len(args) < 2:
                self.usage()
                return

            target, port = args[1].split(":", 1)
            port = int(port)

        bkps = [b.location for b in gdb.breakpoints()]
        temp = TEMPLATE.format(
            target=target,
            port=port,
            arch="amd64" if "x86-64" in get_arch() else "i386",
            endian="big" if is_big_endian() else "little",
            filepath=get_filepath(),
            bkps=bkps
        )
        fd, fname = tempfile.mkstemp(suffix='.py', prefix='gef_')
        with os.fdopen(fd, "w") as f:
            f.write(temp)

        ok("Exploit generated in '{:s}'".format(fname))
        return


if __name__ == "__main__":
    register_external_command(ExploitTemplateCommand())
