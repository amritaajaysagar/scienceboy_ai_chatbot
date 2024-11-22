# Replace with your implementation using libraries like google-auth-oauthlib
# and google-auth-httplib2 for Google login

MAX_PROFILES = 5

def create_profile(name, age_group):
    """Creates a new profile with the given name and age group."""
    # Implement profile creation logic and return profile data
    pass

def get_profiles():
    """Retrieves all existing profiles."""
    # Implement profile retrieval logic and return profile data
    pass

def is_profile_full():
    """Checks if the maximum number of profiles has been reached."""
    return len(get_profiles()) >= MAX_PROFILES