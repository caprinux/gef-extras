"""
ARM Cortex-M support for GEF

To use, source this file *after* gef

Original PR: https://github.com/hugsy/gef/pull/651
Author: SWW13
"""


@register_architecture
class ARM_M(ARM):
    arch = "ARM-M"
    aliases = ("ARM-M", )

    all_registers = ARM.all_registers[:-1] + ["$xpsr", ]
    flag_register = "$xpsr"
    flags_table = {
        31: "negative",
        30: "zero",
        29: "carry",
        28: "overflow",
        24: "thumb",
    }
