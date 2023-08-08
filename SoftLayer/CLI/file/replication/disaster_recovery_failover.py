"""Failover an inaccessible file volume to its available replicant volume."""
# :license: MIT, see LICENSE for more details.

import click
import SoftLayer
from SoftLayer.CLI import environment
from SoftLayer.CLI import exceptions
from SoftLayer.CLI import formatting


@click.command(cls=SoftLayer.CLI.command.SLCommand,
               epilog="""Failover an inaccessible file volume to its available replicant volume.
If a volume (with replication) becomes inaccessible due to a disaster event, this method can be used to immediately
failover to an available replica in another location. This method does not allow for failback via API.
After using this method, to failback to the original volume, please open a support ticket.
If you wish to test failover, please use replica-failover.
""")
@click.argument('volume-id')
@click.option('--replicant-id', help="ID of the replicant volume")
@environment.pass_env
def cli(env, volume_id, replicant_id):
    """Failover an inaccessible file volume to its available replicant volume.

    Example::
        slcli file disaster-recovery-failover 12345678 87654321
        This command performs failover operation for volume with ID 12345678 to replica volume with ID 87654321.
"""
    file_storage_manager = SoftLayer.FileStorageManager(env.client)

    click.secho("""WARNING : Failover an inaccessible file volume to its available replicant volume."""
                """If a volume (with replication) becomes inaccessible due to a disaster event,"""
                """this method can be used to immediately failover to an available replica in another location."""
                """This method does not allow for failback via the API."""
                """To failback to the original volume after using this method, open a support ticket."""
                """If you wish to test failover, use replica-failover instead.""", fg='red')

    if not formatting.confirm('Are you sure you want to continue?'):
        raise exceptions.CLIAbort('Aborted.')

    file_storage_manager.disaster_recovery_failover_to_replicant(
        volume_id,
        replicant_id
    )

    click.echo("Disaster Recovery Failover to replicant is now in progress.")
