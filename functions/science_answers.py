import wikipedia

def answer_science_question(question):
  """
  Attempts to answer a science-based question using Wikipedia.
  """
  try:
    summary = wikipedia.summary(question, sentences=2)
    return summary
  except wikipedia.exceptions.PageError:
    return "Sorry, I couldn't find information on that specific topic."
  except wikipedia.exceptions.DisambiguationError as e:
    return f"There are multiple pages related to '{question}'. Did you mean: {', '.join(e.options)}?"