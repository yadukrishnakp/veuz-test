from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from django.contrib.auth.models import Group as AuthGroup



class ACLBaseBackend:
    
    def get_user_permissions(self, user_obj, obj=None):
        return set()
    
    def get_role_permissions(self, roles):
        permissions = set()
        for role in roles:
            role_permissions = role.permissions.all()
            for role_permission in role_permissions:
                codename = f"auth.{role_permission.codename}"
                permissions.add(codename)
        return permissions
    

    def get_group_permissions(self, user_obj, obj=None):
        user_groups_field = get_user_model()._meta.get_field("user_groups")
        user_groups_query = "group__%s" % user_groups_field.related_query_name()
        
        roles = AuthGroup.objects.filter(**{user_groups_query: user_obj})
        permissions = self.get_role_permissions(roles)
        
        return set(permissions)
    

    def get_all_permissions(self, user_obj, obj=None):
        return {
            *self.get_user_permissions(user_obj, obj=obj),
            *self.get_group_permissions(user_obj, obj=obj),
        }

    def has_acl_perm(self, user_obj, perm, obj=None):
        return perm in self.get_all_permissions(user_obj, obj=obj)
    
