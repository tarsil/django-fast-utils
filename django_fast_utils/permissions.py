"""
Provides a set pluggable permission tools.
"""

from guardian.shortcuts import assign_perm, remove_perm


def assign_user_perm(perm, user_or_group, obj, revoke=False):
    """Assigns permissions for a given object to a given django user or group

    Args:
      perm: permission to be assigned
      user_or_group: django user or group
      obj: object to assign to
      revoke: True if permissions of a given object is to be removed.

    Example:
        `assign_user_perm('is_super_user', user, cars)` (Default value = False)
    """
    if not revoke:
        assign_perm(perm, user_or_group, obj)
    else:
        remove_perm(perm, user_or_group, obj)
