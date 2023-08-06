from __future__ import unicode_literals

import logging

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.utils import six
from djblets.util.decorators import augment_method_from
from djblets.webapi.decorators import (webapi_login_required,
                                       webapi_request_fields,
                                       webapi_response_errors)
from djblets.webapi.errors import (DOES_NOT_EXIST, INVALID_FORM_DATA,
                                   NOT_LOGGED_IN, PERMISSION_DENIED)
from djblets.webapi.resources.user import UserResource as DjbletsUserResource

from reviewboard.accounts.backends import get_enabled_auth_backends
from reviewboard.accounts.errors import UserQueryError
from reviewboard.avatars import avatar_services
from reviewboard.site.urlresolvers import local_site_reverse
from reviewboard.webapi.base import WebAPIResource
from reviewboard.webapi.decorators import webapi_check_local_site
from reviewboard.webapi.errors import USER_QUERY_ERROR
from reviewboard.webapi.resources import resources


logger = logging.getLogger(__name__)


class UserResource(WebAPIResource, DjbletsUserResource):
    """Creates and provides information on users.

    If a user's profile is private, the fields ``email``, ``first_name``,
    ``last_name``, and ``fullname`` will be omitted for non-staff users.
    """
    item_child_resources = [
        resources.api_token,
        resources.archived_review_request,
        resources.muted_review_request,
        resources.user_file_attachment,
        resources.watched,
    ]

    fields = dict({
        'avatar_html': {
            'type': six.text_type,
            'description': 'HTML for rendering the avatar at specified '
                           'sizes. This is only populated if using '
                           '``?render-avatars-at=...`` for GET requests or '
                           '``render_avatars_at=...`` for POST requests.',
            'added_in': '3.0.14',
        },
        'avatar_url': {
            'type': six.text_type,
            'description': 'The URL for an avatar representing the user, '
                           'if available.',
            'added_in': '1.6.14',
            'deprecated_in': '3.0',
        },
        'avatar_urls': {
            'type': six.text_type,
            'description': 'The URLs for an avatar representing the user, '
                           'if available.',
            'added_in': '3.0',
        },
        'is_active': {
            'type': bool,
            'description': 'Whether or not the user is active. Inactive users'
                           'are not able to log in or make changes to Review '
                           'Board.',
            'added_in': '2.5.9',
        },
    }, **DjbletsUserResource.fields)

    allowed_methods = ('GET', 'POST')

    hidden_fields = ('email', 'first_name', 'last_name', 'fullname')

    def get_queryset(self, request, local_site_name=None, *args, **kwargs):
        search_q = request.GET.get('q', None)
        include_inactive = \
            request.GET.get('include-inactive', '0').lower() in ('1', 'true')

        for backend in get_enabled_auth_backends():
            try:
                backend.populate_users(query=search_q,
                                       request=request)
            except Exception as e:
                logger.exception('Error when calling populate_users for auth '
                                 'backend %r: %s',
                                 backend, e)

        local_site = self._get_local_site(local_site_name)
        is_list = kwargs.get('is_list', False)

        # When accessing individual users (not is_list) on public local sites,
        # we allow accessing any username. This is so that the links on reviews
        # and review requests from non-members won't be 404. The list is still
        # restricted to members of the site to avoid leaking information.
        if local_site and (is_list or not local_site.public):
            query = local_site.users.all()
        else:
            query = self.model.objects.all()

        if is_list and not include_inactive:
            query = query.filter(is_active=True)

        if search_q:
            q = None

            # Auth backends may have special naming conventions for users that
            # they'd like to be represented in search. If any auth backends
            # implement build_search_users_query(), prefer that over the
            # built-in searching.
            for backend in get_enabled_auth_backends():
                try:
                    q = backend.build_search_users_query(query=search_q,
                                                         request=request)
                except Exception as e:
                    logger.exception(
                        'Error when calling build_search_users_query for '
                        'auth backend %r: %s',
                        backend, e)

                if q:
                    break

            if not q:
                q = Q(username__istartswith=search_q)

                if request.GET.get('fullname', None):
                    q = q | (Q(first_name__istartswith=search_q) |
                             Q(last_name__istartswith=search_q))

            query = query.filter(q)

        return query.extra(select={
            'is_private': ('SELECT is_private FROM accounts_profile '
                           'WHERE accounts_profile.user_id = auth_user.id')
        })

    def serialize_object(self, obj, request=None, *args, **kwargs):
        data = super(UserResource, self).serialize_object(
            obj, request=request, *args, **kwargs)

        if request:
            # Hide user info from anonymous users and non-staff users (if
            # his/her profile is private).
            if not obj.is_profile_visible(request.user):
                for field in self.hidden_fields:
                    try:
                        del data[field]
                    except KeyError:
                        # The caller may be using ?only-fields. We can ignore
                        # this.
                        pass

        return data

    def serialize_url_field(self, user, **kwargs):
        return local_site_reverse('user', kwargs['request'],
                                  kwargs={'username': user.username})

    def serialize_avatar_html_field(self, user, request=None, **kwargs):
        """Serialize the avatar_html field.

        Args:
            user (django.contrib.auth.models.User):
                The user the avatar is being serialized for.

            request (django.http.HttpRequest, optional):
                The HTTP request from the client.

            **kwargs (dict, unused):
                Additional keyword arguments.

        Returns:
            dict:
            Dictionaries, mapping sizes to renders.
        """
        if not avatar_services.avatars_enabled:
            return None

        renders = {}

        # Look for both the GET and PUT/POST/PATCH versions of this value.
        # If present, we'll render avatars at the sizes specified.
        avatar_sizes = request.GET.get('render-avatars-at',
                                       request.POST.get('render_avatars_at'))

        if avatar_sizes:
            norm_sizes = set()

            for size in avatar_sizes.split(','):
                try:
                    norm_sizes.add(int(size))
                except ValueError:
                    # A non-integer value was passed in. Ignore it.
                    pass

            avatar_sizes = norm_sizes

        if avatar_sizes:
            service = avatar_services.for_user(user)

            if service:
                for size in avatar_sizes:
                    try:
                        renders[six.text_type(size)] = \
                            service.render(request=request,
                                           user=user,
                                           size=size).strip()
                    except Exception as e:
                        logger.exception('Error rendering avatar at size %s '
                                         'for user %s: %s',
                                         size, user, e)

        return renders or None

    def serialize_avatar_url_field(self, user, request=None, **kwargs):
        urls = self.serialize_avatar_urls_field(user, request, **kwargs)

        if urls:
            return urls.get('1x')

        return None

    def serialize_avatar_urls_field(self, user, request=None, **kwargs):
        if avatar_services.avatars_enabled:
            service = avatar_services.for_user(user)

            if service:
                return service.get_avatar_urls(request, user, 48)

        return {}

    def has_access_permissions(self, *args, **kwargs):
        return True

    @webapi_check_local_site
    @webapi_response_errors(NOT_LOGGED_IN, PERMISSION_DENIED, DOES_NOT_EXIST,
                            USER_QUERY_ERROR)
    @webapi_request_fields(
        optional={
            'fullname': {
                'type': bool,
                'description': 'Specifies whether ``q`` should also match '
                               'the beginning of the first name or last name. '
                               'Ignored if ``q`` is not set.',
            },
            'include-inactive': {
                'type': bool,
                'description': 'If set, users who are marked as inactive '
                               '(their accounts have been disabled) will be '
                               'included in the list.',
            },
            'render-avatars-at': {
                'type': six.text_type,
                'description': 'A comma-separated list of avatar pixel sizes '
                               'to render. Renders for each specified size '
                               'be available in the ``avatars_html`` '
                               'dictionary. If not provided, avatars will not '
                               'be rendered.',
            },
            'q': {
                'type': six.text_type,
                'description': 'The string that the username (or the first '
                               'name or last name when using ``fullname``) '
                               'must start with in order to be included in '
                               'the list. This is case-insensitive.',
            },
        },
        allow_unknown=True
    )
    @augment_method_from(WebAPIResource)
    def get_list(self, *args, **kwargs):
        """Retrieves the list of users on the site.

        This includes only the users who have active accounts on the site.
        Any account that has been disabled (for inactivity, spam reasons,
        or anything else) will be excluded from the list.

        The list of users can be filtered down using the ``q`` and
        ``fullname`` parameters.

        Setting ``q`` to a value will by default limit the results to
        usernames starting with that value. This is a case-insensitive
        comparison.

        If ``fullname`` is set to ``1``, the first and last names will also be
        checked along with the username. ``fullname`` is ignored if ``q``
        is not set.

        For example, accessing ``/api/users/?q=bo&fullname=1`` will list
        any users with a username, first name or last name starting with
        ``bo``.

        Inactive users will not be returned by default. However by providing
        ``?include-inactive=1`` they will be returned.
        """
        try:
            return super(UserResource, self).get_list(*args, **kwargs)
        except UserQueryError as e:
            return USER_QUERY_ERROR.with_message(e.msg)

    @webapi_check_local_site
    @webapi_request_fields(
        optional={
            'render-avatars-at': {
                'type': six.text_type,
                'description': 'A comma-separated list of avatar pixel sizes '
                               'to render. Renders for each specified size '
                               'be available in the ``avatars_html`` '
                               'dictionary. If not provided, avatars will not '
                               'be rendered.',
            },
        },
    )
    @augment_method_from(WebAPIResource)
    def get(self, *args, **kwargs):
        """Retrieve information on a registered user.

        This mainly returns some basic information (username, full name,
        e-mail address) and links to that user's root Watched Items resource,
        which is used for keeping track of the groups and review requests
        that the user has "starred".
        """
        pass

    @webapi_login_required
    @webapi_check_local_site
    @webapi_response_errors(PERMISSION_DENIED, INVALID_FORM_DATA)
    @webapi_request_fields(
        required={
            'username': {
                'type': six.text_type,
                'description': 'The username of the user to create.',
            },
            'email': {
                'type': six.text_type,
                'description': 'The e-mail address of the user to create.',
            },
            'password': {
                'type': six.text_type,
                'description': 'The password of the user to create.',
            }
        },
        optional={
            'first_name': {
                'type': six.text_type,
                'description': 'The first name of the user to create.',
            },
            'last_name': {
                'type': six.text_type,
                'description': 'The last name of the user to create.',
            },
            'render_avatars_at': {
                'type': six.text_type,
                'description': 'A comma-separated list of avatar pixel sizes '
                               'to render. Renders for each specified size '
                               'be available in the ``avatars_html`` '
                               'dictionary. If not provided, avatars will not '
                               'be rendered.',
            },
        },
    )
    def create(self, request, username, email, password, first_name='',
               last_name='', local_site=None, *args, **kwargs):
        """Create a new user.

        The user will be allowed to authenticate into Review Board with the
        given username and password.

        Only administrators or those with the ``auth.add_user`` permission
        will be able to create users.

        This API cannot be used on :term:`Local Sites`.
        """
        if (not request.user.is_superuser and
            not request.user.has_perm('auth.add_user')):
            return PERMISSION_DENIED.with_message(
                'You do not have permission to create users.')

        if local_site:
            return PERMISSION_DENIED.with_message(
                'This API is not available for local sites.')

        try:
            validate_email(email)
        except ValidationError as e:
            return INVALID_FORM_DATA, {
                'fields': {
                    'email': [six.text_type(e)]
                },
            }

        try:
            # We wrap this in a transaction.atomic block because attempting to
            # create a user with a username that already exists will generate
            # an IntegrityError and break the current transaction.
            #
            # Unit tests wrap each test case in a transaction.atomic block as
            # well. If this is block is not here, the test case's transaction
            # will break and cause errors during test teardown.
            with transaction.atomic():
                user = User.objects.create_user(username, email, password,
                                                first_name=first_name,
                                                last_name=last_name)
        except IntegrityError:
            return INVALID_FORM_DATA, {
                'fields': {
                    'username': [
                        'A user with the requested username already exists.',
                    ]
                }
            }

        return 201, {
            self.item_result_key: user,
        }


user_resource = UserResource()
