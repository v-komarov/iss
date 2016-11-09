import csv
import sys
from argparse import ArgumentParser

import re
from tabulate import tabulate

from config import Config
from exception import ZenAPIBaseException
from zenoss import ZenossAPI

DEFAULT_PATH = '/Devices'
DEFAULT_COLUMNS = 'u'

VERSION = '0.1b'

DESCRIPTION = u'Zenapitool {version} is a tool which provide useful command-line ' \
              u'interface to the Zenoss Core.'.format(version=VERSION)
EPILOG = u'Source: https://github.com/k-vinogradov/zenapitool. Bug-report: mail@k-vinogradov.ru'


class CmdException(ZenAPIBaseException):
    message = 'Zenoss API tool error'


def full_path(path):
    return '/zport/dmd{path}'.format(path=path)


def parser():
    """ Create parser and use it to parse command line arguments.
    :return: Parsed namespace.
    :rtype: ArgumentParser
    """
    local_arg_parser = ArgumentParser('Zenoss API command line tool')
    subparsers = local_arg_parser.add_subparsers()

    # Print version
    subparsers.add_parser('version', help=u'Get zenapitool\'s version number.')

    # Print default config
    subparsers.add_parser('default-config', help=u'Get default config')

    # Subparser for getting device list from Zenoss.

    device_list_parser = subparsers.add_parser('device-list', description=u'Zenapitool is a command-line tool which '
                                                                          u'provide')

    list_options_group = device_list_parser.add_argument_group(u'List Options', u'Device list filters and options')
    list_options_group.add_argument('-p', '--path', default=DEFAULT_PATH, type=full_path, help=u'Organizer path')
    list_options_group.add_argument('-n', '--name', dest='name', default=None, help=u'Device name pattern',
                                    metavar='NAME')
    list_options_group.add_argument('-a', '--ip', dest='ip_address', default=None, help=u'IP address pattern',
                                    metavar='IP')
    list_options_group.add_argument('--limit', default=None, help=u'Maximum device number.', metavar='NUM', type=int)

    filter_options_group = device_list_parser.add_argument_group(u'Filter Options')
    filter_options_group.add_argument('--filter', default=None, help=u'Additional filter conditions.'
                                                                     u' Available values: ' + filter_help())

    output_group = device_list_parser.add_argument_group(u'Output', u'Output format options')
    output_group.add_argument('-f', '--format', default='table', choices=['table', 'detail', 'csv', 'pipe'],
                              help=u'Output format')
    output_group.add_argument('-c', '--columns', default=DEFAULT_COLUMNS, dest='columns',
                              help=u'Device data fields: ' + filter_help())
    output_group.add_argument('-w', '--output-file', default=None, dest='output', help=u'Output file name')

    # Subparser for moving device to the new location.
    set_location_parser = subparsers.add_parser('set-location', help=u'Change device location')
    set_location_parser.add_argument('uid', help=u'Device unique identifier')
    set_location_parser.add_argument('location', help=u'Zenoss infrastructure location')
    set_location_parser.add_argument('-w', '--wait', action='store_true', help=u'Wait until moving job is completed.')

    # Subparser for collect device info
    collect_parser = subparsers.add_parser('collect-device', help=u'Remodel device')
    collect_parser.add_argument('uid', help=u'Device unique identifier')
    collect_parser.add_argument('-w', '--wait', action='store_true', help=u'Wait for modelling job finish.')

    return local_arg_parser


def filter_columns(device=None):
    """ List of the available filed keys.
    :param device: Device object
    :rtype: zenoss.Device
    :return: Available keys with params.
    :rtype: dict
    """
    columns = dict(
        u=(u'UID', device.get_uid if device else None, [], {}),
        n=(u'Device Name', device.get_device_name if device else None, [], {}),
        i=(u'IP Address', device.get_ip_address if device else None, [], {}),
        l=(u'Location Name', device.get_location_name if device else None, [], {}),
        c=(u'Device Class', device.get_device_class_name if device else None, [], {}),
        I=(u'ISS Location', device.get_iss_location if device else None, [], {}),
        S=(u'SNMP Location', device.get_snmp_location if device else None, [], {}),
        M=(u'Last Collected', device.get_last_collected if device else None, [], {}),
        m=(u'Collected days ago', device.get_last_collected_days if device else None, [], {}),
        C=(u'SNMP Community', device.get_snmp_community if device else None, [], {}),
        V=(u'SNMP Version', device.get_snmp_version if device else None, [], {}),
    )
    return columns


def filter_keys():
    """ Return available list keys.
    :return: List keys.
    :rtype: list
    """
    columns = filter_columns()
    return columns.keys()


def filter_help():
    """ Filter keys help string.
    :return: Help string.
    :rtype: str
    """
    columns = filter_columns()
    return ', '.join(['{key} - {title}'.format(key=key, title=columns[key][0]) for key in columns])


def filter_headers(keys):
    """ Return list of filter headers
    :param keys: Filed keys.
    :type keys: str or list
    :return: Headers
    :rtype: list
    """
    result = []
    columns = filter_columns()
    for key in keys:
        if key in columns:
            result.append(columns[key][0])
        else:
            raise CmdException('Invalid field key \'{}\'.'.format(key))
    return result


def filter_values(device, keys):
    """ Return filed values by filed keys.
    :param device: Device object.
    :type device: zenoss.Device
    :param keys: Keys string
    :type keys: str or dict
    :return: Field/value dictionary.
    :rtype: dict
    """
    columns = filter_columns(device)
    result = {}
    for key in keys:
        if key in columns:
            method = columns[key][1]
            arguments = columns[key][2]
            kwargs = columns[key][3]
            result[key] = method(*arguments, **kwargs)
        else:
            raise CmdException('Invalid field key \'{}\'.'.format(key))
    return result


def column_values(device, keys):
    """ Return field value list.
    :param device: Device object.
    :type device: zenoss.Device
    :param keys: Keys string
    :type keys: str or list
    :return: Field values.
    :rtype: list
    """
    values = filter_values(device, keys)
    return [values[key] for key in keys]


def device_list(arg_list):
    api = ZenossAPI()
    params = dict(uid=arg_list.path, device_name=arg_list.name, ip_address=arg_list.ip_address, limit=arg_list.limit)
    if arg_list.output:
        output = open(arg_list.output, 'w')
    else:
        output = sys.stdout

    if arg_list.filter:
        filter_template = arg_list.filter
        filter_key_list = re.findall(r'(?<={)[a-zA-Z](?=})', arg_list.filter)
        filter_headers(filter_key_list)
    else:
        filter_key_list = None
        filter_template = None

    devices = api.find_devices(**params)

    header = filter_headers(arg_list.columns)
    table = []
    for device in devices:
        if arg_list.filter:
            # noinspection PyTypeChecker
            filter_params = filter_values(device, filter_key_list)
            adopted_template = filter_template
            for key in filter_params:
                param_type = type(filter_params[key])
                if param_type is str or param_type is unicode:
                    adopted_template = adopted_template.replace('{' + key + '}', '\'{' + key + '}\'')
            # noinspection PyArgumentList
            check = eval(adopted_template.format(**filter_params))
            if type(check) is bool:
                if not check:
                    continue
            elif type(check) is not bool:
                raise CmdException(
                    'Invalid filter condition result\'s type \'{}\' instead of boolean.'.format(type(check)))
        table.append(column_values(device, arg_list.columns))
    if arg_list.format == 'table':
        output.write(tabulate(table, header))
        output.write('\n')
    elif arg_list.format == 'csv':
        writer = csv.writer(output)
        writer.writerow(header)
        writer.writerows(table)
    elif arg_list.format == 'detail':
        for device in table:
            device_info = []
            for field in header:
                device_info.append([field, ' : ', device[header.index(field)]])
            output.write(tabulate(device_info, tablefmt="plain"))
            output.write('\n')
            output.write('\n')
    elif arg_list.format == 'pipe':
        for row in table:
            adopted_row = map(lambda s: '' if s is None else s, row)
            output.write('\t'.join(adopted_row) + '\n')
    output.close()


def set_location(arg_list):
    uid = arg_list.uid
    target = arg_list.location
    wait = arg_list.wait
    api = ZenossAPI()
    devices = api.get_devices(uid=uid)
    if len(devices) > 1:
        raise CmdException('There are more than one devices for uid {}'.format(uid))
    elif len(devices) == 0:
        raise CmdException('There are no devices for uid {}'.format(uid))
    else:
        if target not in api.get_location_list():
            raise CmdException('Invalid zenoss location {}'.format(target))
        else:
            device = devices[0]
            print 'Move device {0} to the location {1}.'.format(device.get_uid(), target)
            jobid = device.set_location(target, wait)
            if not wait:
                print 'Job {} was committed.'.format(jobid)


def collect_device(arg_list):
    uid = arg_list.uid
    wait = arg_list.wait
    api = ZenossAPI()
    devices = api.get_devices(uid=uid)
    if len(devices) > 1:
        raise CmdException('There are more than one devices for uid {}'.format(uid))
    elif len(devices) == 0:
        raise CmdException('There are no devices for uid {}'.format(uid))
    else:
        device = devices[0]
        jobid = device.collect_device(wait=wait)
        if wait:
            print jobid
        else:
            print 'Zenmodeler job id {}'.format(jobid)


if __name__ == '__main__':
    arg_parser = parser()
    try:
        args = arg_parser.parse_args()
        if sys.argv[1] == 'device-list':
            device_list(args)
        elif sys.argv[1] == 'default-config':
            sys.stdout.write(Config().default_config())
        elif sys.argv[1] == 'set-location':
            set_location(args)
        elif sys.argv[1] == 'version':
            print 'Zenoss API tool version {}'.format(VERSION)
        elif sys.argv[1] == 'collect-device':
            collect_device(args)
        else:
            parser().print_help()
    except CmdException as e:
        arg_parser.error(e.value)
        sys.exit(1)
