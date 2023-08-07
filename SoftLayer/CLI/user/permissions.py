"""List A users permissions."""
import click

import SoftLayer
from SoftLayer.CLI import environment
from SoftLayer.CLI import formatting
from SoftLayer.CLI import helpers


@click.command(cls=SoftLayer.CLI.command.SLCommand, )
@click.argument('identifier')
@environment.pass_env
def cli(env, identifier):
    """User Permissions."""

    mgr = SoftLayer.UserManager(env.client)
    user_id = helpers.resolve_id(mgr.resolve_ids, identifier, 'username')
    object_mask = "mask[id, permissions, isMasterUserFlag, roles]"

    user = mgr.get_user(user_id, object_mask)
    all_permissions = mgr.get_all_permissions()
    user_permissions = perms_to_dict(user['permissions'])

    if user['isMasterUserFlag']:
        click.secho('This account is the Master User and has all permissions enabled', fg='green')

    env.fout(roles_table(user))
    env.fout(permission_table(user_permissions, all_permissions))


def perms_to_dict(perms):
    """Takes a list of permissions and transforms it into a dictionary for better searching"""
    permission_dict = {}
    for perm in perms:
        permission_dict[perm['keyName']] = True
    return permission_dict


def permission_table(user_permissions, all_permissions):
    """Creates a table of available permissions"""

    table = formatting.Table(['Description', 'KeyName', 'Assigned'])
    table.align['KeyName'] = 'l'
    table.align['Description'] = 'l'
    table.align['Assigned'] = 'l'
    for perm in all_permissions:
        assigned = user_permissions.get(perm['keyName'], False)
        if (perm['keyName'] == 'ACCOUNT_SUMMARY_VIEW' or perm['keyName'] == 'REQUEST_COMPLIANCE_REPORT' or
           perm['keyName'] == 'COMPANY_EDIT' or perm['keyName'] == 'ONE_TIME_PAYMENTS' or
           perm['keyName'] == 'UPDATE_PAYMENT_DETAILS' or perm['keyName'] == 'EU_LIMITED_PROCESSING_MANAGE'
           or perm['keyName'] == 'TICKET_ADD' or perm['keyName'] == 'TICKET_EDIT'
           or perm['keyName'] == 'TICKET_SEARCH' or perm['keyName'] == 'TICKET_VIEW'
           or perm['keyName'] == 'TICKET_VIEW_ALL'):
            table.add_row(["", "", ""])
        else:
            table.add_row([perm['name'], perm['keyName'], assigned])
    return table


def roles_table(user):
    """Creates a table for a users roles"""
    table = formatting.Table(['id', 'Role Name', 'Description'])
    for role in user['roles']:
        table.add_row([role['id'], role['name'], role['description']])
    return table
