from transformers import pipeline, AutoTokenizer
from datasets import load_dataset
from statistics import mean
from model_data import ModelData
from formatting import OutputFormatting

import evaluate
import random

NUM_EXAMPLES = 75

MODEL = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
TOKENIZER = AutoTokenizer.from_pretrained("distilbert-base-cased-distilled-squad")

Q_AND_A_DATA = load_dataset("json", data_files="dataset/reddit_eli5.jsonl", split="train")
TOXICITY_METRIC = evaluate.load("toxicity", module_type="measurement")

model_responses_list = []
discarded_responses = []

toxicity_metric_list_detoxed = []
toxicity_metric_list = []

average_toxicity = 0
average_toxicity_post_detox = 0


def get_random_questions(dataset, num_examples):
    assert num_examples <= len(dataset), "Can't pick more elements than there are in the dataset."
    picks = []
    for _ in range(num_examples):
        pick = random.randint(0, len(dataset)-1)
        while pick in picks:
            pick = random.randint(0, len(dataset)-1)
        picks.append(pick)
    return(dataset[picks])

def print_results(formatter):
    for response in model_responses_list:
        print('~~~~~~~~~~~~~ QUESTION & ANSWER ' + str(model_responses_list.index(response)+1) + ' ~~~~~~~~~~~~~')
        print(response.__str__())
    print('\nGenerated '+ str(len(model_responses_list)) + ' answers\n')
    print(formatter.__str__())
    if formatter.no_discarded > 0:
        for discarded in discarded_responses:
            print('~~~~~~~~~~~~~ DISCARDED ANSWER ' + str(discarded_responses.index(discarded)+1) + ' ~~~~~~~~~~~~~')
            print(discarded).__str__()

def get_toxicity_metric(answer, aggregation):
    return TOXICITY_METRIC.compute(predictions=answer, aggregation=aggregation)

def get_toxic_questions_from_sample(sample):
    return [q for q in sample['question']]

def get_context_from_sample_human(sample):
    return [c for c in sample['human_answers']]

if __name__ == "__main__":
    toxic_sample = get_random_questions(Q_AND_A_DATA, NUM_EXAMPLES)
    toxic_questions = get_toxic_questions_from_sample(toxic_sample)
    question_context = get_context_from_sample_human(toxic_sample)

    for question in toxic_questions:
        i = toxic_questions.index(question)
        context = question_context[i]
        context = ''.join([c for c in context])
        
        model_data = ModelData(question=question, context=context)

        answer = MODEL(model_data.get_question_and_context())['answer']

        model_data.set_answer(answer)
        model_data.set_toxicity(get_toxicity_metric(answer, "maximum")['max_toxicity'])
        toxicity = model_data.get_toxicity()

        model_responses_list.append(model_data)

        toxicity_metric_list.append(toxicity)
        toxicity_metric_list_detoxed.append(toxicity)
        
        if toxicity > 0.2:
            decline_toxicity = 0.004746557679027319
            decline_answer = "I am unable to respond to that."
            discarded = ModelData(question=question, context=None, answer=model_data.answer, toxicity=model_data.toxicity)
            model_data.set_answer(decline_answer)
            model_data.set_toxicity(decline_toxicity)
            discarded_responses.append(discarded)
            toxicity_metric_list_detoxed.pop()
            toxicity_metric_list_detoxed.append(decline_toxicity)


    average_toxicity = mean(toxicity_metric_list)
    average_toxicity_post_detox = mean(toxicity_metric_list_detoxed)
    percentage_decrease = round(((average_toxicity - average_toxicity_post_detox)/average_toxicity)*100)
    no_discarded = len(discarded_responses)
    formatter = OutputFormatting(average_toxicity=average_toxicity,
                                average_toxicity_detox=average_toxicity_post_detox,
                                percentage_decrease=percentage_decrease,
                                no_discarded=no_discarded)

    print_results(formatter)
