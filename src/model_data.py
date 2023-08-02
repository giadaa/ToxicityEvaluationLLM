class ModelData:
  def __init__(self, question, context, answer=None, toxicity=None):
    self.question = question
    self.context = context
    self.answer = answer
    self.toxicity = toxicity

  def __str__(self):
    return f'QUESTION: {self.question}\nANSWER: {self.answer}\nTOXICITY: {self.toxicity}\n'

  def get_question(self):
    return self.question

  def get_context(self):
    return self.context
  
  def get_answer(self):
    return self.answer

  def get_toxicity(self):
    return self.toxicity
  
  def set_answer(self, model_answer):
    self.answer = model_answer
  
  def set_toxicity(self, toxicity_metric):
    self.toxicity = toxicity_metric

  def get_question_and_context(self):
    return {'question': self.question, 'context': self.context}
