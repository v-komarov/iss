import logging
from ConfigParser import ConfigParser
from datetime import timedelta

import os

from exception import ZenAPIBaseException

DEFAULT_FILENAME = 'zenapitool.conf'
DEFAULTS = {
    'connection': dict(
        host=('http://127.0.0.1:8080/', 'Zenoss host URL.'),
        username=('admin', 'Zenoss username.'),
        password=('zenoss', 'Zenoss password.')
    ),
    'api': dict(
        limit=('1000', 'Limit object number received by a request.'),
        job_status_delay=('10', 'Time delay between checking job status in the "waiting" requests.')
    ),
    'logs': dict(
        enable_logging=('yes', 'Enable text log.'),
        path=(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zenapitool.log'), 'Text log filename.'),
        level=('debug', 'Log message level.'),
        console_echo=('no', 'Print log message on the screen.'),
    ),
    'jobs': dict(
        waiting_timeout=('300', 'Job\'s finish waiting timeout in the "waiting" requests.'),
    ),
}


class ConfigError(ZenAPIBaseException):
    """
    Config error exception.
    """
    message = 'Configuration error'


class Config(object):
    """
    Generate and parse zenapitool configuration
    """

    def __init__(self, path=DEFAULT_FILENAME):
        """

        :param path: Absolute path to the config file.
        :type path: str
        """
        config = ConfigParser()
        for section in DEFAULTS:
            config.add_section(section)
            for option in DEFAULTS[section]:
                # noinspection PyTypeChecker
                config.set(section, option, DEFAULTS[section][option][0])

        config.read([DEFAULT_FILENAME, path])
        self.__config = config

    def __get_option(self, path, option_type=str):
        """ Option's value with specific type.
        :param path: Path section/option.
        :type path: str
        :param option_type: Type of the option.
        :type option_type: type
        :rtype: str or bool or int or float
        :return: Option's value.
        """
        if len(path.split('/')) != 2:
            raise ConfigError('Invalid configuration item {}'.format(path))
        else:
            section = path.split('/')[0]
            option = path.split('/')[1]
        value = self.__config.get(section, option)
        if option_type == bool:
            if value.upper() == 'YES':
                return True
            elif value.upper() == 'NO':
                return False
            else:
                ConfigError('Invalid type {t} of the value {v}.'.format(t=option_type, v=value))
        else:
            try:
                return option_type(value)
            except ValueError:
                raise ConfigError('Invalid type {t} of the value {v}.'.format(t=option_type, v=value))

    # noinspection PyTypeChecker
    @staticmethod
    def default_config():
        """ Default config.

        :return: String contains default configuration
        :rtype: str
        """
        conf = ''
        for section in DEFAULTS:
            conf += '[{}]\n\n'.format(section)
            for option in DEFAULTS[section]:
                conf += '# {comment}\n{option} = {value}\n\n'.format(
                    comment=DEFAULTS[section][option][1],
                    option=option,
                    value=DEFAULTS[section][option][0]
                )
        return conf

    def get_zenoss_host(self):
        """ Zenoss host URL.
        :return: URL.
        :rtype: str
        """
        return self.__get_option('connection/host', str)

    def get_zenoss_username(self):
        """ Zenoss username.
        :return: Username.
        :rtype: str
        """
        return self.__get_option('connection/username', str)

    def get_zenoss_password(self):
        """ Zenoss password.
        :return: Password.
        :rtype: str
        """
        return self.__get_option('connection/password', str)

    def get_api_items_limit(self):
        """ Items per request limit.
        :return: Request limit.
        :rtype: int
        """
        return self.__get_option('api/limit', int)

    def get_api_job_status_delay(self):
        """ Time delay between checking job status in the "waiting" requests.
        :return: time delay in seconds
        :rtype: int
        """
        return self.__get_option('api/job_status_delay', int)

    def get_jobs_waiting_timeout(self):
        """ Job's finish waiting timeout in the "waiting" requests.
        :return: Timeout
        :rtype: timedelta
        """
        seconds = self.__get_option('jobs/waiting_timeout', int)
        return timedelta(seconds=seconds)

    def get_logger(self, name):
        """ Configured logger with specific name
        :param name: logger's name
        :type name: str
        :return: logger
        :type: logging.Logger
        """
        logger = logging.getLogger(name)

        # Check if logging is global disabled
        if not self.__get_option('logs/enable_logging', bool):
            nh = logging.NullHandler()
            logger.addHandler(nh)
            logger.setLevel(logging.CRITICAL)
            return logger

        # Set level
        level = self.__get_option('logs/level', str)
        if level.upper() in ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET', ]:
            level = getattr(logging, level.upper())
            logger.setLevel(level)
        else:
            raise ConfigError('Invalid logging level "{}"'.format(level))

        # Set logger params
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', )
        file_handler = logging.FileHandler(self.__get_option('logs/path', str))
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)
        logger.addHandler(file_handler)

        # Check is console echo is enabled
        if self.__get_option('logs/console_echo', bool):
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            console_handler.setLevel(level)
            logger.addHandler(console_handler)

        return logger
