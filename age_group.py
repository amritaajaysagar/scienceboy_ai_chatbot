AGE_GROUPS = {
    "child": "Child (0-12)",
    "teen": "Teenager (13-19)",
    "adult": "Adult (20-64)",
    "senior": "Senior (65+)"
}

def get_age_groups():
    """Returns a list of available age groups."""
    return list(AGE_GROUPS.values())

def get_age_group_code(age_group_name):
    """Returns the age group code for a given age group name."""
    for code, name in AGE_GROUPS.items():
        if name == age_group_name:
            return code
    return None