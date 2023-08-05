# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.contrib import auth
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from protector.internals import DEFAULT_ROLE, \
    ADD_PERMISSION_PERMISSION, VIEW_RESTRICTED_OBJECTS, \
    VIEW_PERMISSION_NAME, get_user_ctype
from protector.helpers import get_view_permission
from protector.managers import GenericUserToGroupManager, OwnerToPermissionManager, \
    OwnerPermissionManager, UserGroupManager, GroupUserManager, RestrictedManager, \
    GenericGroupManager


#  Form a from clause for all permission related to their owners
#  role of user in group must not be empty
#  if permission roles is empty than it is applied to all roles in group


class GenericGlobalPerm(models.Model):
    """
        This model is for defining template-like permissions
        e.g. Every blog moderator could edit his blog
    """
    content_type = models.ForeignKey(
        ContentType, related_name='global_perms', verbose_name=_('content type'),
        on_delete=models.CASCADE, null=True
    )
    roles = models.IntegerField(verbose_name=_('roles'), default=DEFAULT_ROLE)
    permission = models.ForeignKey(
        to=Permission, verbose_name=_('permission'), on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _('global group permission')
        verbose_name_plural = _('global group permissions')
        unique_together = ('content_type', 'permission')


class GenericUserToGroup(models.Model):
    """
        This models is used for linking user to any possible group
        User can have only one link to group
        In case of multiple roles bitmasks is used
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='generic_group_relations', on_delete=models.CASCADE
    )
    roles = models.IntegerField(verbose_name=_('roles'), blank=True, null=True)
    group_id = models.PositiveIntegerField(verbose_name=_('group id'))
    group_content_type = models.ForeignKey(
        verbose_name=_('group content type'), to=ContentType, on_delete=models.CASCADE
    )
    group = GenericForeignKey('group_content_type', 'group_id')
    date_joined = models.DateTimeField(verbose_name=_('date joined'), auto_now_add=True)
    responsible = models.ForeignKey(
        verbose_name=_('responsible'),
        to=settings.AUTH_USER_MODEL, related_name='created_group_relations',
        blank=True, null=True, on_delete=models.SET_NULL
    )

    objects = GenericUserToGroupManager()

    class Meta:
        verbose_name = _('user to group link')
        verbose_name_plural = _('user to group links')
        unique_together = ('group_id', 'group_content_type', 'user')

    def __unicode__(self):
        return "{app}.{model}.{group_id} - {username}".format(
            app=self.group_content_type.app_label,
            model=self.group_content_type.model,
            group_id=self.group_id,
            username=self.user.username
        )


class OwnerToPermission(models.Model):
    """
        This model is two-way generic many-to-many link from owner_object to owned object
        Multiple links from owner to object is supported i.e. different permissions
    """
    ADD_PERMISSION = ADD_PERMISSION_PERMISSION
    object_id = models.PositiveIntegerField(
        verbose_name=_('object id'), null=True
    )
    content_type = models.ForeignKey(
        verbose_name=_('object type'),
        to=ContentType, related_name='restriction_group_relations',
        null=True,
        on_delete=models.CASCADE
    )
    content_object = GenericForeignKey('content_type', 'object_id')
    owner_object_id = models.PositiveIntegerField(verbose_name=_('owner id'))
    owner_content_type = models.ForeignKey(
        verbose_name=_('owner type'),
        to=ContentType, related_name='restricted_object_relations',
        on_delete=models.CASCADE
    )
    owner = GenericForeignKey('owner_content_type', 'owner_object_id')
    permission = models.ForeignKey(
        verbose_name=_('permission'),
        to=Permission, related_name='generic_restriction_relations',
        on_delete=models.CASCADE
    )
    date_issued = models.DateTimeField(verbose_name=_('date issued'), auto_now_add=True)
    responsible = models.ForeignKey(
        verbose_name=_('responsible'),
        to=settings.AUTH_USER_MODEL, related_name='created_permission_relations',
        blank=True, null=True,
        on_delete=models.SET_NULL
    )
    roles = models.IntegerField(verbose_name=_('roles'), default=DEFAULT_ROLE)

    objects = OwnerToPermissionManager()

    class Meta:
        verbose_name = _('owner to permission link')
        verbose_name_plural = _('owner to permission links')
        index_together = (
            ['owner_content_type', 'owner_object_id'],
            ['content_type', 'object_id', 'permission']
        )
        unique_together = (
            'content_type', 'object_id',
            'owner_content_type', 'owner_object_id',
            'permission'
        )
        permissions = (
            (ADD_PERMISSION_PERMISSION, _('add permission')),
            (VIEW_RESTRICTED_OBJECTS, _('view restricted objects')),
        )

    def __unicode__(self):
        if self.object_id is None:
            ctype = None
        else:
            ctype = self.content_type
        result = "{app}.{model}.{pk} ".format(
            app=self.owner_content_type.app_label,
            model=self.owner_content_type.model,
            pk=self.owner_object_id,
        )
        if self.object_id is not None:  # real object not global permission
            result += "- {app}.{model}.{pk}. ".format(
                app=ctype.app_label if ctype else '',
                model=ctype.model if ctype else '',
                pk=self.object_id or '',
            )
        if self.roles:
            result += "Roles {roles}. ".format(roles=self.roles)
        result += "Permission {perm}".format(perm=self.permission.codename)
        return result

    def save(self, *args, **kwargs):
        if self.owner_content_type == get_user_ctype():
            # Here is a bit of denormalization
            # User is a part of group of his own
            # This is done to drastically improve perm checking performance
            GenericUserToGroup.objects.get_or_create(
                group_id=self.owner_object_id,
                group_content_type=self.owner_content_type,
                user_id=self.owner_object_id,
                roles=1
            )
        super(OwnerToPermission, self).save(*args, **kwargs)


class GenericPermsMixin(models.Model):
    """
        Mixin is can be used to easily retrieve all owners of permissions to this object
    """
    permission_relations = GenericRelation(
        OwnerToPermission, content_type_field='owner_content_type',
        object_id_field='owner_object_id'
    )

    permissions = None

    def __init__(self, *args, **kwargs):
        super(GenericPermsMixin, self).__init__(*args, **kwargs)
        self.permissions = OwnerPermissionManager(self)

    class Meta:
        abstract = True


class UserGenericPermsMixin(GenericPermsMixin):
    """
        Mixin is used for replacing standard user authorization mechanism
        Also mimics all methods of standard user and is completely compatible
    """
    is_superuser = models.BooleanField(
        verbose_name=_('superuser status'), default=False,
        help_text=_('Designates that user has all perms')
    )

    @property
    def groups(self):
        return UserGroupManager(self)

    class Meta:
        abstract = True

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True

        for backend in auth.get_backends():
            if not hasattr(backend, 'has_perm'):
                continue
            try:
                if backend.has_perm(self, perm, obj):
                    return True
            except PermissionDenied:
                return False
        return False

    def has_perms(self, perm_list, obj=None):
        """
        Returns True if the user has each of the specified permissions. If
        object is passed, it checks if the user has all required perms for this
        object.
        """
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_module_perms(self, app_label):
        """
        Returns True if the user has any permissions in the given app label.
        Uses pretty much the same logic as has_perm, above.
        """
        if self.is_active and self.is_superuser:
            return True

        for backend in auth.get_backends():
            if not hasattr(backend, 'has_module_perms'):
                continue
            try:
                if backend.has_module_perms(self, app_label):
                    return True
            except PermissionDenied:
                return False
        return False


class AbstractGenericGroup(GenericPermsMixin):
    """
        Base model for all Groups
        Inherit your model from that to enable generic group features
    """
    PARTICIPANT = 1
    ROLES = (
        (PARTICIPANT, _('Participant')),
    )
    DEFAULT_ROLE = PARTICIPANT

    """
        You could define a list of pairs "field_name, roles"
        Field name should be a foreign key to user
        to auto add this user to this group.
        This is useful for cases like auto assign permissions to post author
    """
    MEMBER_FOREIGN_KEY_FIELDS = []

    users_relations = GenericRelation(
        GenericUserToGroup, content_type_field='group_content_type',
        object_id_field='group_id'
    )

    objects = GenericGroupManager()

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(AbstractGenericGroup, self).__init__(*args, **kwargs)
        self.users = GroupUserManager(self)

    def save(self, *args, **kwargs):
        super(AbstractGenericGroup, self).save(*args, **kwargs)
        self._update_member_foreign_key()

    def _update_member_foreign_key(self):
        for field, roles in self.MEMBER_FOREIGN_KEY_FIELDS:
            self.users.add(getattr(self, field), roles=roles)

    def get_roles(self, user):
        try:
            user_roles = self.users_relations.values('roles').get(user=user)['roles']
        except GenericUserToGroup.DoesNotExist:
            return []
        else:
            return get_roles_from_mask(user_roles)


def get_roles_from_mask(mask):
    counter = 0
    result = []
    for val in reversed(bin(mask)[2:]):
        if int(val) == 1:
            result.append(pow(2, counter))
        counter += 1
    return result


class Restriction(MPTTModel, models.Model):
    """
        This model contains resriction hierarchy
    """
    object_id = models.PositiveIntegerField(verbose_name=_('object id'), blank=False, null=False)
    content_type = models.ForeignKey(
        to=ContentType, verbose_name=_('content type'), blank=False, null=False,
        on_delete=models.CASCADE
    )
    restricted_object = GenericForeignKey('content_type', 'object_id')

    parent = TreeForeignKey(
        'self', verbose_name=_('parent object'),
        null=True, blank=True, related_name='children',
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = _('Object restriction')
        verbose_name_plural = _('Objects restrictions')
        unique_together = (('object_id', 'content_type'), )

    def __unicode__(self):
        return '{app}.{model} {pk}'.format(
            app=self.content_type.app_label,
            model=self.content_type.model,
            pk=self.object_id
        )


class Restricted(models.Model):
    """
        Inherit your model from that to enable visiblity restrictions
    """
    VIEW_PERMISSION_NAME = VIEW_PERMISSION_NAME

    restriction_id = models.PositiveIntegerField(
        verbose_name=_('restriction id'), blank=True, null=True
    )
    restriction_content_type = models.ForeignKey(
        verbose_name=_('restriction content type id'),
        to=ContentType, blank=True, null=True, related_name="%(app_label)s_%(class)s_restrictions",
        on_delete=models.SET_NULL
    )
    restriction = GenericForeignKey('restriction_content_type', 'restriction_id')

    objects = RestrictedManager()

    class Meta:
        abstract = True

    @classmethod
    def get_view_permission(cls):
        return get_view_permission()

    def get_parent_object(self):
        return None

    def get_restriction_obj(self):
        return Restriction.objects.get_or_create(
            object_id=self.pk,
            content_type=ContentType.objects.get_for_model(self)
        )[0]

    def get_restriction_descendants(self):
        ctype_dict = {}
        restriction_obj = self.get_restriction_obj()
        descendants = restriction_obj.get_descendants()
        ctype_dict = {}
        for restriction in descendants:
            ctype_id = restriction.content_type_id
            if ctype_id not in ctype_dict:
                ctype_dict[ctype_id] = []
            ctype_dict[ctype_id].append(restriction.object_id)
        return ctype_dict

    def restrict(self):
        # method restricts all objects down by restriction hierarchy
        if self.restriction != self:
            current_restriction_id = self.restriction_id
            current_restriction_ctype_id = self.restriction_content_type_id
            self.restriction = self
            if self.pk is not None:
                ctype_dict = self.get_restriction_descendants()
                for ctype_id, object_ids in ctype_dict.items():
                    ctype = ContentType.objects.get_for_id(ctype_id)
                    objs = ctype.model_class().objects.filter(
                        pk__in=object_ids, restriction_id=current_restriction_id,
                        restriction_content_type_id=current_restriction_ctype_id
                    )
                    objs.update(
                        restriction_id=self.id,
                        restriction_content_type=ContentType.objects.get_for_model(self)
                    )
            self.save()

    def unrestrict(self):
        if self.restriction is None:
            return
        ctype_dict = self.get_restriction_descendants()
        current_restriction_id = self.restriction_id
        current_restriction_ctype_id = self.restriction_content_type_id
        for ctype_id, object_ids in ctype_dict.items():
            ctype = ContentType.objects.get_for_id(ctype_id)
            objs = ctype.model_class().objects.filter(
                pk__in=object_ids, restriction_id=current_restriction_id,
                restriction_content_type_id=current_restriction_ctype_id
            )
            # take only objects that restricted by same object as self
            objs.update(
                restriction_id=None,
                restriction_content_type=None
            )
        self.restriction = None
        self.save()

    def is_visible(self, user=None):
        return self.restriction is None or (user is not None and user.has_perm(
            VIEW_PERMISSION_NAME, self.restriction
        ))

    def is_restricted(self):
        return self.restriction_id is not None

    def inherit_restriction(self):
        parent_object = self.get_parent_object()
        if parent_object is not None and isinstance(parent_object, Restricted):
            self.restriction_id = parent_object.restriction_id
            self.restriction_content_type_id = parent_object.restriction_content_type_id

    def generate_restriction(self):
        parent_object = self.get_parent_object()
        if parent_object is not None and isinstance(parent_object, Restricted):
            parent_restriction = Restriction.objects.get(
                object_id=parent_object.id,
                content_type=ContentType.objects.get_for_model(parent_object)
            )
        else:
            parent_restriction = None
        self_restriction, created = Restriction.objects.get_or_create(
            object_id=self.pk,
            content_type=ContentType.objects.get_for_model(self),
            defaults={'parent': parent_restriction}
        )

    def save(self, *args, **kwargs):
        created = self.pk is None
        if created:
            self.inherit_restriction()
        super(Restricted, self).save(*args, **kwargs)
        if created and self.pk is not None:
            self.generate_restriction()
            # Create a corresponding restriction object and link it to parent

    def add_viewer(self, viewer, responsible=None, roles=None):
        roles = roles or DEFAULT_ROLE
        otp, created = OwnerToPermission.objects.get_or_create(
            object_id=self.pk,
            content_type=ContentType.objects.get_for_model(self),
            owner_object_id=viewer.pk,
            owner_content_type=ContentType.objects.get_for_model(viewer),
            permission=get_view_permission(),
            defaults={'responsible': responsible, 'roles': roles}
        )
        if not created and otp.roles != roles:
            otp.roles |= roles
            otp.save()


class PermissionInfo(models.Model):
    permission = models.OneToOneField(to=Permission, related_name='info', on_delete=models.CASCADE)
    description = models.TextField(verbose_name=_('description'), blank=True, null=True)

    class Meta:
        verbose_name = _('permission info')
        verbose_name_plural = _('permissions info')
