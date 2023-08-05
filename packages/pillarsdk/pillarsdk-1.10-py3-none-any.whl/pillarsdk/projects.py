from .resource import List
from .resource import Find
from .resource import Create
from .resource import Post
from .resource import Update
from .resource import Delete
from .resource import Replace
from .exceptions import ResourceNotFound, ForbiddenAccess

from . import utils
from .nodes import Node
from .api import Api


class Project(List, Find, Create, Post, Update, Delete, Replace):
    """Project class wrapping the REST nodes endpoint
    """
    path = "projects"
    ensure_query_projections = {'permissions': 1, 'category': 1, 'user': 1}

    @classmethod
    def find_one(cls, params, api=None):
        """Get one resource starting from parameters different than the resource
        id. TODO if more than one match for the query is found, raise exception.
        """
        api = api or Api.Default()

        # Force delivery of only 1 result
        params['max_results'] = 1

        cls._ensure_projections(params, cls.ensure_query_projections)
        url = utils.join_url_params(cls.path, params)

        response = api.get(url)
        # Keep the response a dictionary, and cast it later into an object.
        if response.get('_items'):
            item = utils.convert_datetime(response['_items'][0])
            return cls(item)
        else:
            raise ResourceNotFound(response)

    @classmethod
    def find_by_url(cls, project_url, params=None, api=None):
        if params is None:
            params = {}
        params.setdefault('where', {}).setdefault('url', project_url)

        return cls.find_one(params, api=api)

    def update(self, attributes=None, api=None):
        api = api or self.api
        attributes = attributes or self.to_dict()
        etag = attributes['_etag']
        attributes.pop('allowed_methods', None)

        # Strip embedded image file properties and revert to ObjectId
        for prop in ['picture_square', 'picture_header']:
            if prop in attributes and type(attributes[prop]) is dict:
                attributes[prop] = attributes[prop]['_id']
        # Remove None attributes
        attributes = utils.remove_none_attributes(attributes)
        attributes = utils.remove_private_keys(attributes)

        url = utils.join_url(self.path, str(self['_id']))
        headers = utils.merge_dict(
            self.http_headers(),
            {'If-Match': str(etag)})
        new_attributes = api.put(url, attributes, headers)
        self.error = None
        self.merge(new_attributes)
        return self.success()

    def has_method(self, method):
        if self.allowed_methods is None:
            return False
        return method in self.allowed_methods

    def children(self, api=None):
        api = api or self.api
        children = Node.all({
            'where': '{"project" : "%s", "parent" : {"$exists": false}}'\
                % self._id,
            }, api=api)
        return children

    def get_node_type(self, node_type_name):
        return next((item for item in self.node_types if item.name \
            and item['name'] == node_type_name), None)

    def node_type_has_method(self, node_type_name, method, api=None):
        """Utility method that checks if a given node_type has the requested
        method.
        """
        api = api or Api.Default()
        url = utils.join_url('/p', str(self._id), node_type_name)

        # Perform the HTTP OPTIONS request.
        options = api.OPTIONS(url)

        # Obtain the Accept header, warning if it doesn't exist.
        try:
            accept_hdr = options.headers['Allowed']
        except KeyError:
            self.log.warning('OPTIONS call to %r did not return an Accept header.', url)
            return False

        methods = {meth.strip() for meth in accept_hdr.split(',')}
        return method in methods

    def _manage_user(self, user_id, action, api=None):
        """Add or remove a user to a project give its ObjectId."""
        api = api or self.api
        url = 'p/users'
        payload = {
            'project_id': str(self._id),
            'user_id': str(user_id),
            'action': action}
        headers = self.http_headers()
        return api.post(url, payload, headers)

    def add_user(self, user_id, api=None):
        """Add a user to a project given its ObjectId."""
        return self._manage_user(user_id, 'add', api)

    def remove_user(self, user_id, api=None):
        """Remove a user to a project given its ObjectId."""
        return self._manage_user(user_id, 'remove', api)

    def get_users(self, api=None):
        """Get all users that are member of the admin group for the project."""
        api = api or self.api
        params = {'project_id': str(self._id)}
        url = utils.join_url_params('p/users', params)
        headers = self.http_headers()
        response = api.get(url, headers=headers)
        return response

    def create(self, api=None):
        name = self.name or 'new project'

        headers = self.http_headers()
        response = api.post('p/create', headers=headers,
                            params={'name': name})
        self.merge(response)
