LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    # Add more languages with their codes and display names
}

def get_language_options():
  """
  Returns a list of available languages with their codes and display names.
  """
  return [{"code": code, "name": LANGUAGES[code]} for code in LANGUAGES]

def get_language_by_code(code):
  """
  Returns the display name of a language given its code.
  """
  if code in LANGUAGES:
    return LANGUAGES[code]
  else:
    return None