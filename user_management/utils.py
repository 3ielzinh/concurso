"""
Helper functions for user access control to modules and categories
"""
from modules.models import Category


def get_user_allowed_categories(user):
    """
    Get all categories that a user has access to.
    Priority:
    1. If user has specific allowed_categories in UserModuleAccess, use those
    2. Otherwise, use plan-based access (is_premium)
    """
    # Check if user has custom module access configured
    if hasattr(user, 'module_access'):
        allowed_categories = user.module_access.allowed_categories.all()
        if allowed_categories.exists():
            # User has specific categories assigned
            return allowed_categories.filter(is_active=True)
    
    # Default to plan-based access
    queryset = Category.objects.filter(is_active=True)
    if not user.is_premium:
        queryset = queryset.filter(is_premium=False)
    
    return queryset


def user_can_access_category(user, category):
    """
    Check if a user can access a specific category
    """
    allowed_categories = get_user_allowed_categories(user)
    return category in allowed_categories


def user_can_access_module(user, module):
    """
    Check if a user can access a specific module
    """
    return user_can_access_category(user, module.category)


def user_can_access_subject(user, subject):
    """
    Check if a user can access a specific subject
    """
    return user_can_access_module(user, subject.module)
