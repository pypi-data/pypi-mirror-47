from ..auth import Auth
from ..base_request import BaseRequest
from ..settings import Settings
from .config import Config
from .release import Release
from .. import exceptions

from datetime import datetime
import json


# TODO: support both app_id and app_name
class Application(object):
    """
    This class implements application model for balena python SDK.

    The returned objects properties are `__metadata, actor, app_name, application_type, commit, depends_on__application, device_type, id, is_accessible_by_support_until__date, should_track_latest_release, slug, user`.

    """

    def __init__(self):
        self.base_request = BaseRequest()
        self.settings = Settings()
        self.config = Config()
        self.auth = Auth()
        self.release = Release()

    def get_all(self):
        """
        Get all applications (including collaborator applications).

        Returns:
            list: list contains info of applications.

        Examples:
            >>> balena.models.application.get_all()
            '[{u'depends_on__application': None, u'should_track_latest_release': True, u'app_name': u'foo', u'application_type': {u'__deferred': {u'uri': u'/resin/application_type(5)'}, u'__id': 5}, u'__metadata': {u'type': u'', u'uri': u'/resin/application(12345)'}, u'is_accessible_by_support_until__date': None, u'actor': 12345, u'id': 12345, u'user': {u'__deferred': {u'uri': u'/resin/user(12345)'}, u'__id': 12345}, u'device_type': u'raspberrypi3', u'commit': None, u'slug': u'my_user/foo'}, {u'depends_on__application': None, u'should_track_latest_release': True, u'app_name': u'bar', u'application_type': {u'__deferred': {u'uri': u'/resin/application_type(5)'}, u'__id': 5}, u'__metadata': {u'type': u'', u'uri': u'/resin/application(12346)'}, u'is_accessible_by_support_until__date': None, u'actor': 12345, u'id': 12346, u'user': {u'__deferred': {u'uri': u'/resin/user(12345)'}, u'__id': 12345}, u'device_type': u'raspberrypi3', u'commit': None, u'slug': u'my_user/bar'}]'

        """

        return self.base_request.request(
            'my_application', 'GET', endpoint=self.settings.get('pine_endpoint')
        )['d']

    def get(self, name):
        """
        Get a single application.

        Args:
            name (str): application name.

        Returns:
            dict: application info.

        Raises:
            ApplicationNotFound: if application couldn't be found.
            AmbiguousApplication: when more than one application is returned.

        Examples:
            >>> balena.models.application.get('foo')
            '{u'depends_on__application': None, u'should_track_latest_release': True, u'app_name': u'foo', u'application_type': {u'__deferred': {u'uri': u'/resin/application_type(5)'}, u'__id': 5}, u'__metadata': {u'type': u'', u'uri': u'/resin/application(12345)'}, u'is_accessible_by_support_until__date': None, u'actor': 12345, u'id': 12345, u'user': {u'__deferred': {u'uri': u'/resin/user(12345)'}, u'__id': 12345}, u'device_type': u'raspberrypi3', u'commit': None, u'slug': u'my_user/foo'}'

        """

        params = {
            'filter': 'app_name',
            'eq': name
        }
        try:
            apps = self.base_request.request(
                'application', 'GET', params=params,
                endpoint=self.settings.get('pine_endpoint')
            )['d']
            if len(apps) > 1:
                raise exceptions.AmbiguousApplication(name)
            return apps[0]
        except IndexError:
            raise exceptions.ApplicationNotFound(name)

    def get_by_owner(self, name, owner):
        """
        Get a single application.

        Args:
            name (str): application name.
            owner (str):  owner's username.

        Returns:
            dict: application info.

        Raises:
            ApplicationNotFound: if application couldn't be found.
            AmbiguousApplication: when more than one application is returned.

        Examples:
            >>> balena.models.application.get_by_owner('foo', 'my_user')
            '{u'depends_on__application': None, u'should_track_latest_release': True, u'app_name': u'foo', u'application_type': {u'__deferred': {u'uri': u'/resin/application_type(5)'}, u'__id': 5}, u'__metadata': {u'type': u'', u'uri': u'/resin/application(12345)'}, u'is_accessible_by_support_until__date': None, u'actor': 12345, u'id': 12345, u'user': {u'__deferred': {u'uri': u'/resin/user(12345)'}, u'__id': 12345}, u'device_type': u'raspberrypi3', u'commit': None, u'slug': u'my_user/foo'}'

        """

        slug = '{owner}/{app_name}'.format(owner=owner.lower(), app_name=name.lower())

        params = {
            'filter': 'slug',
            'eq': slug
        }
        try:
            apps = self.base_request.request(
                'application', 'GET', params=params,
                endpoint=self.settings.get('pine_endpoint')
            )['d']
            if len(apps) > 1:
                raise exceptions.AmbiguousApplication(slug)
            return apps[0]
        except IndexError:
            raise exceptions.ApplicationNotFound(slug)

    def has(self, name):
        """
        Check if an application exists.

        Args:
            name (str): application name.

        Returns:
            bool: True if application exists, False otherwise.

        Examples:
            >>> balena.models.application.has('foo')
            True

        """

        params = {
            'filter': 'app_name',
            'eq': name
        }
        app = self.base_request.request(
            'application', 'GET', params=params,
            endpoint=self.settings.get('pine_endpoint')
        )['d']
        return bool(app)

    def has_any(self):
        """
        Check if the user has any applications.

        Returns:
            bool: True if user has any applications, False otherwise.

        Examples:
            >>> balena.models.application.has_any()
            True

        """

        apps = self.base_request.request(
            'application', 'GET', endpoint=self.settings.get('pine_endpoint')
        )['d']
        return bool(apps)

    def get_by_id(self, app_id):
        """
        Get a single application by application id.

        Args:
            app_id (str): application id.

        Returns:
            dict: application info.

        Raises:
            ApplicationNotFound: if application couldn't be found.

        Examples:
            >>> balena.models.application.get_by_id(12345)
            '{u'depends_on__application': None, u'should_track_latest_release': True, u'app_name': u'foo', u'application_type': {u'__deferred': {u'uri': u'/resin/application_type(5)'}, u'__id': 5}, u'__metadata': {u'type': u'', u'uri': u'/resin/application(12345)'}, u'is_accessible_by_support_until__date': None, u'actor': 12345, u'id': 12345, u'user': {u'__deferred': {u'uri': u'/resin/user(12345)'}, u'__id': 12345}, u'device_type': u'raspberrypi3', u'commit': None, u'slug': u'my_user/foo'}'

        """

        params = {
            'filter': 'id',
            'eq': app_id
        }
        try:
            return self.base_request.request(
                'application', 'GET', params=params,
                endpoint=self.settings.get('pine_endpoint')
            )['d'][0]
        except IndexError:
            raise exceptions.ApplicationNotFound(app_id)

    def create(self, name, device_type, app_type=None):
        """
        Create an application. This function only works if you log in using credentials or Auth Token.

        Args:
            name (str): application name.
            device_type (str): device type (display form).
            app_type (Optional[str]): application type.

        Returns:
            dict: application info.

        Raises:
            InvalidDeviceType: if device type is not supported.
            InvalidApplicationType: if app type is not supported.

        Examples:
            >>> balena.models.application.create('foo', 'Raspberry Pi 3', 'microservices-starter')
            '{u'depends_on__application': None, u'should_track_latest_release': True, u'app_name': u'foo', u'application_type': {u'__deferred': {u'uri': u'/resin/application_type(5)'}, u'__id': 5}, u'__metadata': {u'type': u'', u'uri': u'/resin/application(12345)'}, u'is_accessible_by_support_until__date': None, u'actor': 12345, u'id': 12345, u'user': {u'__deferred': {u'uri': u'/resin/user(12345)'}, u'__id': 12345}, u'device_type': u'raspberrypi3', u'commit': None, u'slug': u'my_user/foo'}'

        """

        device_types = self.config.get_device_types()
        device_slug = [device['slug'] for device in device_types
                       if device['name'] == device_type]
        if device_slug:

            data = {
                'app_name': name,
                'device_type': device_slug[0]
            }

            if app_type:

                params = {
                    'filter': 'slug',
                    'eq': app_type
                }

                app_type_detail = self.base_request.request(
                    'application_type', 'GET', params=params,
                    endpoint=self.settings.get('pine_endpoint'), login=True
                )['d']

                if not app_type_detail:
                    raise exceptions.InvalidApplicationType(app_type)

                data['application_type'] = app_type_detail[0]['id']

            return json.loads(self.base_request.request(
                'application', 'POST', data=data,
                endpoint=self.settings.get('pine_endpoint'), login=True
            ).decode('utf-8'))
        else:
            raise exceptions.InvalidDeviceType(device_type)

    def remove(self, name):
        """
        Remove application. This function only works if you log in using credentials or Auth Token.

        Args:
            name (str): application name.

        Examples:
            >>> balena.models.application.remove('Edison')
            'OK'

        """

        params = {
            'filter': 'app_name',
            'eq': name
        }
        return self.base_request.request(
            'application', 'DELETE', params=params,
            endpoint=self.settings.get('pine_endpoint'), login=True
        )

    def restart(self, name):
        """
        Restart application. This function only works if you log in using credentials or Auth Token.

        Args:
            name (str): application name.

        Raises:
            ApplicationNotFound: if application couldn't be found.

        Examples:
            >>> balena.models.application.restart('RPI1')
            'OK'

        """

        app = self.get(name)
        return self.base_request.request(
            'application/{0}/restart'.format(app['id']), 'POST',
            endpoint=self.settings.get('api_endpoint'), login=True
        )

    def get_config(self, app_id, version, **options):
        """
        Download application config.json.

        Args:
            app_id (str): application id.
            version (str): the OS version of the image.
            **options (dict): OS configuration keyword arguments to use. The available options are listed below:
                network (Optional[str]): the network type that the device will use, one of 'ethernet' or 'wifi' and defaults to 'ethernet' if not specified.
                appUpdatePollInterval (Optional[str]): how often the OS checks for updates, in minutes.
                wifiKey (Optional[str]): the key for the wifi network the device will connect to.
                wifiSsid (Optional[str]): the ssid for the wifi network the device will connect to.
                ip (Optional[str]): static ip address.
                gateway (Optional[str]): static ip gateway.
                netmask (Optional[str]): static ip netmask.

        Returns:
            dict: application config.json content.

        Raises:
            ApplicationNotFound: if application couldn't be found.

        """

        # Application not found will be raised if can't get app by id.
        self.get_by_id(app_id)

        if not version:
            raise exceptions.MissingOption('An OS version is required when calling application.get_config()')

        if 'network' not in options:
            options['network'] = 'ethernet'

        options['appId'] = app_id
        options['version'] = version

        return self.base_request.request(
            '/download-config', 'POST', data=options,
            endpoint=self.settings.get('api_endpoint')
        )

    def enable_rolling_updates(self, app_id):
        """
        Enable Rolling update on application.

        Args:
            app_id (str): application id.

        Returns:
            OK/error.

        Raises:
            ApplicationNotFound: if application couldn't be found.

        Examples:
            >> > balena.models.application.enable_rolling_updates('106640')
            'OK'
        """

        params = {
            'filter': 'id',
            'eq': app_id
        }
        data = {
            'should_track_latest_release': True
        }

        return self.base_request.request(
            'application', 'PATCH', params=params, data=data,
            endpoint=self.settings.get('pine_endpoint')
        )

    def disable_rolling_updates(self, app_id):
        """
        Disable Rolling update on application.

        Args:
            name (str): application id.

        Returns:
            OK/error.

        Raises:
            ApplicationNotFound: if application couldn't be found.

        Examples:
            >> > balena.models.application.disable_rolling_updates('106640')
            'OK'
        """

        params = {
            'filter': 'id',
            'eq': app_id
        }
        data = {
            'should_track_latest_release': False
        }

        return self.base_request.request(
            'application', 'PATCH', params=params, data=data,
            endpoint=self.settings.get('pine_endpoint')
        )

    def enable_device_urls(self, app_id):
        """
        Enable device urls for all devices that belong to an application

        Args:
            app_id (str): application id.

        Returns:
            OK/error.

        Examples:
            >> > balena.models.application.enable_device_urls('5685')
            'OK'

        """

        params = {
            'filter': 'belongs_to__application',
            'eq': app_id
        }
        data = {
            'is_web_accessible': True
        }

        return self.base_request.request(
            'device', 'PATCH', params=params, data=data,
            endpoint=self.settings.get('pine_endpoint')
        )

    def disable_device_urls(self, app_id):
        """
        Disable device urls for all devices that belong to an application.

        Args:
            app_id (str): application id.

        Returns:
            OK/error.

        Examples:
            >> > balena.models.application.disable_device_urls('5685')
            'OK'

        """

        params = {
            'filter': 'belongs_to__application',
            'eq': app_id
        }
        data = {
            'is_web_accessible': False
        }

        return self.base_request.request(
            'device', 'PATCH', params=params, data=data,
            endpoint=self.settings.get('pine_endpoint')
        )

    def grant_support_access(self, app_id, expiry_timestamp):
        """
        Grant support access to an application until a specified time.

        Args:
            app_id (str): application id.
            expiry_timestamp (int): a timestamp in ms for when the support access will expire.

        Returns:
            OK/error.

        Examples:
            >> > balena.models.application.grant_support_access('5685', 1511974999000)
            'OK'

        """

        if not expiry_timestamp or expiry_timestamp <= int((datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds() * 1000):
            raise exceptions.InvalidParameter('expiry_timestamp', expiry_timestamp)

        params = {
            'filter': 'id',
            'eq': app_id
        }

        data = {
            'is_accessible_by_support_until__date': expiry_timestamp
        }

        return self.base_request.request(
            'application', 'PATCH', params=params, data=data,
            endpoint=self.settings.get('pine_endpoint')
        )

    def revoke_support_access(self, app_id):
        """
        Revoke support access to an application.

        Args:
            app_id (str): application id.

        Returns:
            OK/error.

        Examples:
            >> > balena.models.application.revoke_support_access('5685')
            'OK'

        """

        params = {
            'filter': 'id',
            'eq': app_id
        }

        data = {
            'is_accessible_by_support_until__date': None
        }

        return self.base_request.request(
            'application', 'PATCH', params=params, data=data,
            endpoint=self.settings.get('pine_endpoint')
        )

    def generate_provisioning_key(self, app_id):
        """
        Generate a device provisioning key for a specific application.

        Args:
            app_id (str): application id.

        Returns:
            str: device provisioning key.

        Examples:
            >> > balena.models.application.generate_provisioning_key('5685')
            'GThZJps91PoJCdzfYqF7glHXzBDGrkr9'

        """

        # Make sure user has access to the app_id
        self.get_by_id(app_id)

        return self.base_request.request(
            '/api-key/application/{}/provisioning'.format(app_id),
            'POST',
            endpoint=self.settings.get('api_endpoint')
        )

    def set_to_release(self, app_id, full_release_hash):
        """
        Set an application to a specific commit.

        Args:
            app_id (str): application id.
            full_release_hash (str) : full_release_hash.

        Returns:
            OK/error.

        Examples:
            >> > balena.models.application.set_to_release('5685', '7dba4e0c461215374edad74a5b78f470b894b5b7')
            'OK'

        """

        params = {
            'filter': 'id',
            'eq': app_id
        }

        data = {
            'commit': full_release_hash,
            'should_track_latest_release': False
        }

        return self.base_request.request(
            'application', 'PATCH', params=params, data=data,
            endpoint=self.settings.get('pine_endpoint')
        )

    def will_track_new_releases(self, app_id):
        """
        Get whether the application is configured to receive updates whenever a new release is available.

        Args:
            app_id (str): application id.

        Returns:
            bool: is tracking the latest release.

        Examples:
            >> > balena.models.application.will_track_new_releases('5685')
            True

        """

        return bool(self.get_by_id(app_id)['should_track_latest_release'])

    def is_tracking_latest_release(self, app_id):
        """
        Get whether the application is up to date and is tracking the latest release for updates.

        Args:
            app_id (str): application id.

        Returns:
            bool: is tracking the latest release.

        Examples:
            >> > balena.models.application.is_tracking_latest_release('5685')
            True

        """

        app = self.get_by_id(app_id)
        latest_release = None

        try:
            latest_release = self.release.get_latest_by_application(app_id)
        except exceptions.ReleaseNotFound:
            pass

        return bool(app['should_track_latest_release']) and (not latest_release or app['commit'] == latest_release['commit'])

    def get_target_release_hash(self, app_id):
        """
        Get the hash of the current release for a specific application.

        Args:
            app_id (str): application id.

        Returns:
            str: The release hash of the current release.

        Examples:
            >>> balena.models.application.get_target_release_hash('5685')

        """

        return self.get_by_id(app_id)['commit']

    def track_latest_release(self, app_id):
        """
        Configure a specific application to track the latest available release.

        Args:
            app_id (str): application id.

        Examples:
            >>> balena.models.application.track_latest_release('5685')

        """

        latest_release = None

        try:
            latest_release = self.release.get_latest_by_application(app_id)
        except exceptions.ReleaseNotFound:
            pass

        params = {
            'filter': 'id',
            'eq': app_id
        }

        data = {
            'should_track_latest_release': True
        }

        if latest_release:
            data['commit'] = latest_release['commit']

        return self.base_request.request(
            'application', 'PATCH', params=params, data=data,
            endpoint=self.settings.get('pine_endpoint')
        )
