import json
from datetime import datetime
from time import sleep, time

import re
import requests

from config import Config
from exception import ZenAPIBaseException
from external import get_iss_location

ROUTERS = dict(MessagingRouter='messaging',
               EventsRouter='evconsole',
               ProcessRouter='process',
               ServiceRouter='service',
               DeviceRouter='device',
               NetworkRouter='network',
               TemplateRouter='template',
               DetailNavRouter='detailnav',
               ReportRouter='report',
               MibRouter='mib',
               ZenPackRouter='zenpack',
               JobsRouter='jobs')

DEFAULT_UID = '/zport/dmd/Devices'


def human_readable_size(num):
    """ Human readable data size.
    :param num: Number.
    :type num: int or float
    :return: Data size.
    :rtype: str
    """
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f %s" % (num, 'TB')


def human_readable_time(num):
    """ Human readable time interval from number of milliseconds.
    :param num: Milliseconds.
    :type num: int
    :return: Time interval.
    :rtype: str
    """
    multipliers = (('ms', 1000), ('sec', 60), ('min', 60), ('hours', 24), ('days', 7))
    for item in multipliers:
        symbol = item[0]
        multiplier = item[1]
        if num < multiplier:
            return "%3.1f %s" % (num, symbol)
        num /= multiplier
    return "%3.1f %s" % (num, 'weeks')


class ZenossAPIException(ZenAPIBaseException):
    """ ZenAPI Exception. """
    message = 'API Error'


class NoSuchJob(ZenAPIBaseException):
    """ Special exception for non-existing job. """
    message = 'No such job ID'


def get_uid(data):
    """ Quick extraction of the element with 'uid' key from the dictionary.
    :param data: dict
    :return: u'uid' element from dictionary
    :rtype: str
    """
    if u'uid' in data:
        return data[u'uid']
    else:
        return None


class ZenossAPI:
    """ Working with Zenoss Core through JSON API. """

    def __init__(self):
        self.__conf = Config()
        self.__host = self.__conf.get_zenoss_host()
        self.__session = requests.Session()
        self.__session.auth = (self.__conf.get_zenoss_username(), self.__conf.get_zenoss_password())
        self.__session.verify = False
        self.__req_count = 0
        self.__log = self.__conf.get_logger(__name__)
        self.__limit = self.__conf.get_api_items_limit()
        self.__jobs_status_delay = self.__conf.get_api_job_status_delay()

    def __router_request(self, router, method, data=None, skip_success_check=False):
        """ Send JSON POST-request to the Zenoss API.
        :param router: Router's name.
        :type router: str
        :param method: Method's name.
        :type method: str
        :param data: Method's parameters.
        :type data: list
        :param skip_success_check: Don't check 'success' field in the response.
        :return: Dictionary contains the response.
        :rtype: dict
        """
        if router not in ROUTERS:
            raise ZenossAPIException('Router \'{}\' not available.'.format(router))

        req_data = json.dumps([dict(
            action=router,
            method=method,
            data=data,
            type='rpc',
            tid=self.__req_count)])

        self.__log.debug('Making request ({counter}) to router {router} with method {method}'.format(
            router=router,
            method=method,
            counter=self.__req_count + 1
        ))

        uri = '{host}/zport/dmd/{router}_router'.format(host=self.__host, router=ROUTERS[router])
        headers = {'Content-type': 'application/json; charset=utf-8'}
        start = time() * 1000
        response = self.__session.post(uri, data=req_data, headers=headers)
        end = time() * 1000
        self.__req_count += 1
        self.__log.debug('Received {size} in {time}'.format(
            size=human_readable_size(float(response.headers['content-length'])),
            time=human_readable_time(end - start)))

        if re.search('name="__ac_name"', response.content.decode("utf-8")):
            raise ZenossAPIException('Request failed. Bad username/password.')
        try:
            result = json.loads(response.content.decode("utf-8"))['result']
        except ValueError:
            raise ZenossAPIException(response.text)
        if (u'success' in result and result[u'success']) or skip_success_check:
            return result
        else:
            message = 'Request to the method {method} from the router {router} was unsuccessful. {reason}'.format(
                method=method, router=router, reason=result[u'msg'])
            raise ZenossAPIException(message)

    def get_detailed_info(self, uid):
        """ Returns detailed object info.
        :type uid: str
        :param uid: Unique identifier.
        :rtype: dict
        :return: Dictionary contains elements: collector, comments, description, device, deviceClass,
        events, firstSeen, groups, hwManufacturer, hwModel, icon, id, inspector_type, ipAddress, ipAddressString,
        lastChanged, lastCollected, links, location, locking, memory, meta_type, name, osManufacturer, osModel,
        priority, priorityLabel, productionState, productionStateLabel, pythonClass, rackSlot, serialNumber, severity,
        snmpAgent, snmpCommunity, snmpContact, snmpDescr, snmpLocation, snmpSysName, snmpVersion, status, systems,
        tagNumber, uid, uptime, uuid
        """
        data = [{'uid': uid}]
        response = self.__router_request('DeviceRouter', 'getInfo', data=data)
        return response[u'data']

    def get_devices(self, uid=DEFAULT_UID, start=0, limit=None, params=None):
        """ Retrieves a list of devices. This method supports pagination.
        :param uid: Unique identifier of the device or the infrastructure organizer.
        :type uid: str
        :param start: Query offset.
        :type start: int
        :param limit: Maximum number of devices which can be received in one response.
        :type limit: int
        :param params: Additional request params with elements: name, ipAddress, deviceClass, productionState
        :type params: dict
        :rtype: list of Device
        :return: List of Device objects
        """
        if not limit:
            limit = self.__conf.get_api_items_limit()
        data = [{'uid': uid, 'start': start, 'limit': limit, 'params': params}]
        response = self.__router_request('DeviceRouter', 'getDevices', data=data)
        devices = response[u'devices']
        hash_check = response[u'hash']
        map(lambda item: item.update({u'hash': hash_check}), devices)
        return [Device(d, api=self) for d in devices]

    def get_device_count(self, uid=DEFAULT_UID, params=None):
        """ Return total devices number.
        :param uid: Unique identifier of the device or the infrastructure organizer.
        :type uid: str
        :param params: Additional request params with elements: name, ipAddress, deviceClass, productionState
        :type params: dict
        :return: Number of the devices
        :rtype: int
        """
        data = [{'uid': uid, 'start': 1, 'limit': 0, 'params': params}]
        return int(self.__router_request('DeviceRouter', 'getDevices', data=data)[u'totalCount'])

    def get_all_devices(self, uid=DEFAULT_UID, params=None, limit=None):
        """ Return list of all devices.
        :param uid: Unique identifier of the device or the infrastructure organizer.
        :type uid: str
        :param params: Additional request params with elements: name, ipAddress, deviceClass, productionState
        :type params: dict
        :param limit: Max entries number.
        :type limit: int
        :return: List of Device objects
        :rtype: list of Device
        """
        if not params:
            params = {}
            self.__log.info('Getting full device list from {0}'.format(uid))
        else:
            params_str = ', '.join(['{key} {value},'.format(key=key, value=params[key]) for key in params])
            self.__log.info(
                'Getting device list from {uid} with parameters: {params}'.format(uid=uid, params=params_str))
        result = []
        total_count = self.get_device_count(uid, params)
        if limit and limit < total_count:
            total_count = limit
        if limit and limit < self.__limit:
            query_limit = limit
        else:
            query_limit = self.__limit
        while len(result) < total_count:
            self.__log.debug(
                'Getting next {limit} devices start from {start}'.format(limit=self.__limit, start=len(result)))
            result += self.get_devices(uid=uid, start=len(result), limit=query_limit, params=params)
            self.__log.debug('Loaded {0} devices of {1}'.format(len(result), total_count))
        self.__log.info('Total devices have got: {0}'.format(len(result)))
        return result

    def find_devices(self, uid=DEFAULT_UID, device_name=None, ip_address=None, limit=None):
        """ Find devices by organizer, name and IP address
        :param uid: unique identifier of the organizer
        :type uid: str
        :param device_name: device name
        :type device_name: str
        :param ip_address: IP address
        :type ip_address: str
        :param limit: Max entries number.
        :type limit: int
        :return: list of dicts with device info
        :rtype: list
        """
        params = {}
        if device_name:
            params['name'] = device_name
        if ip_address:
            params['ipAddress'] = ip_address
        self.__log.info(
            'Looking for devices with params {params} in the {uid}'.format(params=', '.join(params.values()), uid=uid))
        result = self.get_all_devices(uid=uid, params=params, limit=limit)
        self.__log.info('Found {0} device(s).'.format(len(result)))
        return result

    def get_jobs(self, start=0, limit=None, sort='scheduled', direct='ASC'):
        """ Return job list.
        :param start: Query offset.
        :type start: int
        :param limit: Maximum number of jobs which can be received in one response.
        :type limit: int
        :param direct: N/A
        :type direct: str
        :param sort: N/A
        :type sort: str
        :return: List of dictionaries with jobs' info.
        :rtype: list of dict
        """
        if not limit:
            limit = self.__limit
        data = [dict(start=start, limit=limit, sort=sort, dir=direct, page=0)]
        self.__log.debug(
            'Getting next {limit} jobs start from {start} sorted by {sorted} direct {dir}'.format(limit=limit,
                                                                                                  start=start,
                                                                                                  sorted=sort, dir=dir))
        return self.__router_request('JobsRouter', 'getJobs', data=data)[u'jobs']

    def get_jobs_count(self):
        """ Return total jobs number.
        :return: Total jobs count.
        :rtype: int
        """
        data = [dict(start=0, limit=0, sort='scheduled', dir='ASC', page=0)]
        return int(self.__router_request('JobsRouter', 'getJobs', data=data)[u'totalCount'])

    def get_all_jobs(self):
        """ Return full job list.
        :return: Full job list.
        :rtype: list of dict
        """
        self.__log.info('Getting full job list.')
        result = []
        total_count = self.get_jobs_count()
        while len(result) < total_count:
            result += self.get_jobs(start=len(result))
            self.__log.debug('Jobs were loaded: {} of {}.'.format(len(result), total_count))
        self.__log.info('Totally jobs have been got: {}'.format(len(result)))
        return result

    def get_job_detail(self, job_id):
        """ Job detail dictionary: content, logfile, maxLimit.
        :param job_id: Job unique identifier
        :type job_id: str
        :return: Dictionary: content, logfile, maxLimit.
        :rtype: dict
        """
        self.__log.info('Getting job {} detail.'.format(job_id))
        detail = self.__router_request('JobsRouter', 'detail', data=[{'jobid': job_id}, ], skip_success_check=True)
        if all(map(lambda x: x is None, detail.values())):
            raise NoSuchJob(job_id)
        else:
            return detail

    def get_job_log(self, job_id):
        """ Return job's log by job's unique identifier.
        :param job_id: Unique job identifier.
        :return: Log message list.
        :rtype: list
        """
        return self.get_job_detail(job_id)[u'content']

    def get_job_status(self, job_id):
        """ Return job status by unique identifier.
        :param job_id: Unique job identifier.
        :type job_id: str
        :return: Job's status.
        :rtype: str
        """
        self.__log.info('Getting {} job status.'.format(job_id))
        self.get_job_detail(job_id)
        total_count = self.get_jobs_count()
        counter = 0
        while counter < total_count:
            for job in self.get_jobs(start=counter):
                counter += 1
                if job[u'uuid'] == job_id:
                    return job[u'status']
        raise NoSuchJob(job_id)

    def get_job_statuses(self, job_ids):
        """ Return statuses of the multiple jobs.
        :param job_ids: list of str
        :return: Dictionary with job's id as a key and job's status as a value.
        :rtype: dict
        """
        self.__log.info('Getting status status is {} jobs.'.format(len(job_ids)))
        result = dict([(key, None) for key in job_ids])
        for job in self.get_all_jobs():
            if job[u'uuid'] in result:
                result[job[u'uuid']] = job[u'status']
        for job_id in job_ids:
            if job_id not in result:
                raise NoSuchJob(job_id)
        return result

    def is_job_exist(self, job_id):
        """ Check if job exists.
        :param job_id: Unique job identifier.
        :type job_id: str
        :return: True is job exits else False.
        :rtype: bool
        """
        try:
            self.get_job_detail(job_id)
        except NoSuchJob:
            return False
        else:
            return True

    def remodel_device(self, uid, wait=True):
        """ Remodel selected device by device unique identifier. Return job unique identifier
        for the remodel job, if it was posted False to the wait parameter, or the job's log
        if it was True.
        :param uid: Device unique identifier.
        :type uid: str
        :param wait: Wait until remodel job is finished.
        :type wait: bool
        :return: JobID or job's log.
        :rtype: str
        """
        self.__log.info('Submitting remodel job for the device {}'.format(uid))
        response = self.__router_request('DeviceRouter', 'remodel', data=[{'deviceUid': uid}])

        jobid = response[u'jobId']

        self.__log.info('Submit job {}'.format(jobid))

        if wait:

            # Wait till job is finished.

            status = self.get_job_status(jobid)
            start_time = datetime.now()
            while status != u'SUCCESS':
                if datetime.now() - start_time > self.__conf.get_jobs_waiting_timeout():
                    raise ZenossAPIException('Collect {uid} device job {jobid} timeout.'.format(uid=uid, jobid=jobid))
                self.__log.debug('Job {0} status is {1}'.format(jobid, status))
                sleep(self.__jobs_status_delay)
                status = self.get_job_status(jobid)
            self.__log.debug('Job {0} status is {1}'.format(jobid, status))

            self.__log.info('Job {} finished'.format(jobid))
            job_log = self.get_job_log(jobid)
            return ''.join(job_log)
        else:
            return jobid

    def move_devices(self, uids, target, hashcheck, wait=True):
        """ Move devices by IDs to the organizer with specific UID.
        :param uids: List of unique identifiers of devices.
        :type uids: list of str
        :param target: Organizer unique identifier.
        :type target: str
        :param hashcheck: Hash from get_devices() response.
        :type hashcheck: str
        :param wait: Wait until moving job is completed.
        :type wait: bool
        :return: List of moving jobs unique identifiers.
        :rtype: list
        """
        try:
            self.get_detailed_info(target)
        except ZenossAPIException:
            raise ZenossAPIException('Invalid target UID {}'.format(target))
        data = [dict(
            uids=uids,
            target=target,
            hashcheck=hashcheck
        )]
        self.__log.info(
            'Submitting jobs for move {dev_number} device(s) to {path}.'.format(dev_number=len(uids), path=target))
        response = self.__router_request('DeviceRouter', 'moveDevices', data=data)
        self.__log.info('{} job(s) submitted.'.format(len(response[u'new_jobs'])))
        if wait:
            job_descriptions = {}
            for item in response[u'new_jobs']:
                job_descriptions[item[u'uuid']] = item[u'description']
            incomplete = True
            start_time = datetime.now()
            while incomplete:
                incomplete = False
                if datetime.now() - start_time > self.__conf.get_jobs_waiting_timeout():
                    raise ZenossAPIException('Device moving jobs timeout.')
                job_statuses = self.get_job_statuses(job_descriptions.keys())
                for job in job_statuses:
                    if job_statuses[job] == u'SUCCESS':
                        self.__log.info(
                            'Job {uid} ({descr}) is completed.'.format(uid=job, descr=job_descriptions[job]))
                        del job_descriptions[job]
                    else:
                        incomplete = True
        return [item[u'uid'] for item in response[u'new_jobs']]

    def get_location_list(self):
        """ Return full list of locations.
        :return: List of locations
        :rtype: list
        """
        return map(lambda d: d.values()[0], self.__router_request('DeviceRouter', 'getLocations')[u'locations'])

    def does_uid_exist(self, uid, prefix='/zport/dmd/Devices'):
        """ Check if UID exists.
        :param uid: Unique identifier
        :type uid: str
        :param prefix: UID prefix
        :type prefix: str
        :return: True if UID exists else false.
        :rtype: bool
        """
        if uid[0:10] != '/zport/dmd/':
            uid = prefix + uid
        try:
            self.get_detailed_info(uid)
        except ZenossAPIException:
            return False
        else:
            return True

    def delete_jobs(self, job_ids):
        """ Remove the jobs by unique identifiers.
        :param job_ids: List of the unique job identifiers.
        :type job_ids: list of str
        :return: API response as dictionary
        :rtype: dict
        """
        data = [dict(jobids=job_ids)]
        return self.__router_request('JobsRouter', 'deleteJobs', data=data)


class Device(object):
    """ Working with device """

    __SHORT_INFO_KEYS = [u'collector',
                         u'events',
                         u'groups',
                         u'hash',
                         u'hwManufacturer',
                         u'hwModel',
                         u'ipAddress',
                         u'ipAddressString',
                         u'location',
                         u'name',
                         u'osManufacturer',
                         u'osModel',
                         u'priority',
                         u'productionState',
                         u'pythonClass',
                         u'serialNumber',
                         u'systems',
                         u'tagNumber',
                         u'uid', ]
    __INFO_KEYS = [u'collector',
                   u'comments',
                   u'description',
                   u'device',
                   u'deviceClass',
                   u'events',
                   u'firstSeen',
                   u'groups',
                   u'hwManufacturer',
                   u'hwModel',
                   u'icon',
                   u'id',
                   u'inspector_type',
                   u'ipAddress',
                   u'ipAddressString',
                   u'lastChanged',
                   u'lastCollected',
                   u'links',
                   u'location',
                   u'locking',
                   u'memory',
                   u'meta_type',
                   u'name',
                   u'osManufacturer',
                   u'osModel',
                   u'priority',
                   u'priorityLabel',
                   u'productionState',
                   u'productionStateLabel',
                   u'pythonClass',
                   u'rackSlot',
                   u'serialNumber',
                   u'severity',
                   u'snmpAgent',
                   u'snmpCommunity',
                   u'snmpContact',
                   u'snmpDescr',
                   u'snmpLocation',
                   u'snmpSysName',
                   u'snmpVersion',
                   u'status',
                   u'systems',
                   u'tagNumber',
                   u'uid',
                   u'uptime',
                   u'uuid', ]

    def __init__(self, device, api=None):
        """
        :param device: Dictionary with device info or unique device identifier.
        :type device: dict or str
        :param api: Zenoss API
        :type api: ZenossAPI
        """
        if not api:
            self.__api = ZenossAPI()
        else:
            self.__api = api
        self.__short_info = None
        self.__info = None
        self.__hash = None
        if type(device) == dict:
            if 'uid' not in device or (u'meta_type' in device and device[u'meta_type'] != u'Device'):
                raise ZenossAPIException('Invalid data sent to the device object')
            if u'meta_type' in device:
                self.__info = device.copy()
                self.__uid = device[u'uid']
                self.__short_info = {}
                for key in self.__SHORT_INFO_KEYS:
                    self.__short_info[key] = device[key]
            else:
                self.__uid = device[u'uid']
                self.__short_info = device.copy()
            if u'hash' in device:
                self.__hash = device[u'hash']
        else:
            self.__uid = device

    def __str__(self):
        return 'Device <{}>'.format(self.__uid)

    def __unicode__(self):
        return unicode(self.__str__())

    def __repr__(self):
        return self.__str__()

    def __update(self, force=False):
        """ Reload device data from Zenoss
        :param force: Update device regardless device hash has changed or not.
        :type force: bool
        """

        new_data = self.__api.get_devices(uid=self.__uid)[0]
        if new_data.get_hash_check() != self.__hash or force:
            self.__uid = new_data.get_uid()
            self.__short_info = new_data.__get_short_info()
            self.__info = self.__api.get_detailed_info(self.__uid)
            self.__hash = new_data.get_hash_check()

    def __get_detailed_info(self):
        """ Return dictionary with detailed device info.
        :return: Detailed device info.
        :rtype: dict
        """
        if not self.__info:
            self.__update(force=True)
        return self.__info.copy()

    def __get_short_info(self):
        """ Return dictionary with device info.
        :return: Detailed info.
        :rtype: dict
        """
        if not self.__short_info:
            self.__update()
        return self.__short_info.copy()

    def __get_item(self, *args):
        """ Get device info item by path
        :param args: Item path elements.
        :return: Item value.
        :rtype: str
        """
        if args[0] in self.__SHORT_INFO_KEYS:
            info = self.__get_short_info()
        elif args[0] in self.__INFO_KEYS:
            info = self.__get_detailed_info()
        else:
            raise ZenossAPIException('Unknown item key \'{}\''.format('/'.join(args)))
        try:
            for key in args:
                info = info[key]
                if info is None:
                    return None
            return info
        except KeyError:
            return ZenossAPIException('Unknown item key \'{}\''.format('/'.join(args)))

    def __move_device(self, uid, control_method, wait=True):
        """ Move device to organizer by UID.
        :param uid: Unique organizer identifier.
        :type uid: str
        :param control_method: Method of function which return current organizer UID to check.
        :type control_method: types.MethodType
        :param wait: Wait for moving job finish.
        :type wait: bool
        """
        self.__update()
        if control_method() == uid:
            return None
        else:
            return self.__api.move_devices([self.__uid, ], uid, self.__hash, wait=wait)

    def get_data_item(self, path):
        """ Return device info item by path.
        :param path: Item path.
        :type path: str
        :return: Item value.
        :rtype: str
        """
        return self.__get_item(*path.split('/'))

    def get_hash_check(self):
        """ Return device hash from the get_devices method.
        :return: Hash
        :rtype: str
        """
        return self.__hash

    def get_iss_location(self):
        """ Return device location through GET-request to ISS.
        :return: Device location
        :rtype: str
        """
        return get_iss_location(self.get_data_item('ipAddressString'))

    def get_location_name(self):
        """ Return device location.
        :return: Device location.
        :rtype: str
        """
        return self.get_data_item('location/name')

    def get_location_uid(self):
        """ Return location UID.
        :return: Location UID.
        :rtype: str
        """
        return self.get_data_item('location/uid')

    def get_snmp_location(self):
        """ Value of the snmpLocation field.
        :return: Return value of the device snmpLocation field.
        :rtype: str
        """
        snmp_location = self.get_data_item('snmpLocation')
        if not snmp_location:
            return None
        snmp_location = re.sub(r'[, ]*gate.*', '', snmp_location)
        m_obj = re.search(r'[A-Z][\w\- ]+(,[^,]+){2}(?! gate)|[A-Z][\w\- ]+(,[^,]+){2}', snmp_location)
        if m_obj:
            location = m_obj.group()
            return '/' + re.sub(r' *, *', '/', location.strip())
        else:
            return None

    def set_location(self, uid, wait=True):
        """ Move device to the location with specific UID.
        :param uid: Location UID.
        :type uid: str
        :param wait: Wait for moving job finish.
        :type wait: bool
        :return: Moving job unique identifier.
        :rtype: str
        """
        prefix = u'/zport/dmd/Locations'
        if uid[:len(prefix)] != prefix:
            uid = prefix + uid
        result = self.__move_device(uid, self.get_location_uid, wait=wait)
        if wait:
            self.__update()
        return result

    def get_last_collected(self):
        """ Return last time device was collected.
        :return: Last time device was collected.
        :rtype: datetime
        """
        string = self.get_data_item('lastCollected')
        if string == u'Not Modeled':
            return None
        else:
            return datetime.strptime(string, u'%Y/%m/%d %H:%M:%S')

    def get_last_collected_days(self):
        """ Return how many days ago the device was collected.
        :return: Number of days
        :rtype: int
        """
        if self.get_last_collected():
            age = datetime.now() - self.get_last_collected()
            return age.days
        else:
            return -1

    def get_device_class_name(self):
        """ Return device class name.
        :return: Device class name
        :rtype: str
        """
        return self.get_data_item('deviceClass/name')

    def get_device_name(self):
        """ Return device name.
        :return: Device name.
        :rtype: str
        """
        return self.get_data_item('name')

    def get_ip_address(self):
        """ Return device IP address.
        :return: IP address.
        :rtype: str
        """
        return self.get_data_item('ipAddressString')

    def collect_device(self, wait=True):
        """ Collect device.
        :param wait: Wait for device modelling job finish.
        :type wait: bool
        :return: Modelling device job ID.
        :rtype: str
        """
        return self.__api.remodel_device(self.__uid, wait=wait)

    def get_uid(self):
        """ Device unique identifier.
        :return: Device UID.
        :rtype: str
        """
        return self.__uid

    def get_snmp_version(self):
        """ Device SNMP version
        :return: SNMP version
        :rtype: str
        """
        return self.get_data_item('snmpVersion')

    def get_snmp_community(self):
        """ Device SNMP community
        :return: SNMP Community
        :rtype: str
        """
        return self.get_data_item('snmpCommunity')