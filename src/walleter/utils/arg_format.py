"""
Custom formatter for argparse usage
"""
# Standard
import argparse


class ArgFormatter(argparse.HelpFormatter):
    """
    Modify the way argparse creates usage text. Based on
    http://stackoverflow.com/questions/26985650 with some additional
    modifications
    """

    # use defined argument order to display usage
    def _format_usage(self, usage, actions, groups, prefix):

        # Actions without -h listed
        core_actions = []
        for act in actions:
            try:
                opt_str = act.option_strings[0]
            except IndexError:
                opt_str = None

            if act.dest == 'help' and opt_str == '-h':
                continue
            core_actions.append(act)

        if prefix is None:
            prefix = 'usage: '

        # if usage is specified, use that
        if usage is not None:
            usage = usage % dict(prog=self._prog)

        # if no optionals or positionals are available, usage is just prog
        elif usage is None and not actions:
            usage = '%(prog)s' % dict(prog=self._prog)

        # Help text gets appended first, so if it is there, move it

        elif usage is None:
            prog = '%(prog)s' % dict(prog=self._prog)
            # build full usage string
            action_usage = self._format_actions_usage(core_actions, groups)
            usage = ' '.join([s for s in [prog, action_usage] if s])

        return '%s%s\n\n' % (prefix, usage)
