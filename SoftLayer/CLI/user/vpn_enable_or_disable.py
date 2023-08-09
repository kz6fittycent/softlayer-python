"""Enable or Disable vpn for a user."""
# :license: MIT, see LICENSE for more details.


import click

import SoftLayer
from SoftLayer.CLI import environment
from SoftLayer.CLI import helpers
from SoftLayer.CLI import exceptions
from SoftLayer.CLI import formatting


@click.command(cls=SoftLayer.CLI.command.SLCommand, )
@click.argument('user')
@environment.pass_env
def vpn_enable(env, user):
    """Enable vpn for a user.
    
    Example::
        slcli user vpn-enable 1234567
    """

    mgr = SoftLayer.UserManager(env.client)
    user_id = helpers.resolve_id(mgr.resolve_ids, user, 'username')

    if not (env.skip_confirmations or
            formatting.confirm(f'This will enable vpn with the id {user_id}. '
                               'Continue?')):
        raise exceptions.CLIAbort('Aborted.')
    
    result = mgr.vpn_enable_or_disable(user_id, True)
    message = f"{user} vpn is successfully enabled"

    if result:
        click.secho(message, fg='green')
    else:
        click.secho(f"{user} vpn enable is not successful", fg='red')




@click.command(cls=SoftLayer.CLI.command.SLCommand, )
@click.argument('user')
@environment.pass_env
def vpn_disable(env, user):
    """Disable vpn for a user.

    Example::
        slcli user vpn-disable 1234567
    """

    mgr = SoftLayer.UserManager(env.client)
    user_id = helpers.resolve_id(mgr.resolve_ids, user, 'username')

    if not (env.skip_confirmations or
            formatting.confirm(f'This will disable vpn with the id {user_id}. '
                               'Continue?')):
        raise exceptions.CLIAbort('Aborted.')
    
    result = mgr.vpn_enable_or_disable(user_id, False)
    message = f"{user} vpn is successfully disabled"

    if result:
        click.secho(message, fg='green')
    else:
        click.secho(f"{user} vpn disable is not successfully", fg='red')