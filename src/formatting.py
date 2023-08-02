class OutputFormatting:
  def __init__(self, average_toxicity, average_toxicity_detox, percentage_decrease, no_discarded):
    self.average_toxicity = average_toxicity
    self.average_toxicity_detox = average_toxicity_detox
    self.percentage_decrease = percentage_decrease
    self.no_discarded = no_discarded

  def __str__(self):
    return f'\nAVERAGE TOXICITY:\nBefore detox: {self.average_toxicity}\nAfter detox: {self.average_toxicity_detox}\n\nPercentage decrease: {self.percentage_decrease}%\n\nNo. responses discarded: {self.no_discarded}\n'
