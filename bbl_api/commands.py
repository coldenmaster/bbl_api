# file_path: frappe-bench/apps/flags/flags/commands.py
import click
from bbl_api.socket_server.tcp_server import start_tcp_server

from bbl_api.utils import print_green, print_purple, print_red

@click.command('wtt-flags')
@click.argument('state', type=click.Choice(['on', 'off']))
def wtt_flags(state):
    print_purple('wtt_flags: ' + state)


@click.command('wt-start-tcp-server')
@click.option("-p", "--port", default=8002, help="Port to run the TCP server on")
def wt_start_tcp_server(port):
    print_purple(f'Port to run the TCP server on: {port}')
    start_tcp_server(port)


commands = [
    wtt_flags,
    wt_start_tcp_server,
]
