#!/usr/bin/env python
# coding: utf-8

# In[11]:


get_ipython().system('wget https://raw.githubusercontent.com/alexeygrigorev/minsearch/main/minsearch.py')


# In[1]:


import pandas as pd


# ## Ingestion

# In[2]:


df = pd.read_csv('./Find-a-Doctor/data/hip_surgeons.csv')


# In[3]:


import minsearch


# In[4]:


columns = df.columns.tolist()
print(columns)


# In[5]:


df.insert(0, 'id', df.index)
df


# In[6]:


index = minsearch.Index(
    text_fields=columns,
    keyword_fields=['id']
)


# In[7]:


documents = df.to_dict(orient='records')


# In[8]:


len(documents)


# In[9]:


documents[0]['id']


# In[11]:


del df['ID']


# In[8]:


index.fit(documents)


# In[11]:


query = 'Give me a list of 10 not recommended hip_surgeons from the USA'


# In[12]:


index.search(query)


# In[14]:


model = 'gpt-4o-mini'
response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": query}]
    )

print(response)


# ## RAG flow

# In[28]:


from openai import OpenAI

client = OpenAI()


# In[10]:


def search(query):
    boost = {}

    results = index.search(
        query=query,
        filter_dict={},
        boost_dict=boost,
        num_results=100
    )

    return results


# In[11]:


prompt_template = """
You're an active person with severe hip dysfunction looking for an HR surgeon. Answer the QUESTION based on the CONTEXT from the hip surgeon database.
Use only the facts from the CONTEXT when answering the QUESTION.

QUESTION: {question}

CONTEXT:
{context}
""".strip()

entry_template = """
orthopedic_surgeon_first_name: {orthopedic_surgeon_first_name}
orthopedic_surgeon_surname: {orthopedic_surgeon_surname}
jpg_doctor: {jpg_doctor}
numbers_hr: {number_hr}
adjusted: {adjusted}
number_thr: {number_thr}
number_bmhr: {number_bmhr}
type_of_hr_prosthesis: {type_of_hr_prosthesis}
type_of_thr_prosthesis: {type_of_thr_prosthesis}
operational_technique: {operational_technique}
anesthetic: {anesthetic}
cement_femur_side: {cement_femur_side}
this_joint_capsule_saved_all: {this_joint_capsule_saved_all}
city: {city}
country: {country}
patient-reported_positive_outcomes: {patient-reported_positive_outcomes}
patient-reported_complications: {patient-reported_complications}
cut_muscles_is_fixed_again: {cut_muscles_is_fixed_again}
complete_opera_report_is_given: {complete_opera_report_is_given}
hr_average_size: {hr_average_size}
hr_average_location: {hr_average_location}
assesses_x-ray: {assesses_x-ray}
x-ray_at_discharge: {x-ray_at_discharge}
two-sided_operation: {two-sided_operation}
foreign_patients: {foreign_patients}
address: {address}
street: {street}
local: {local}
postal_code: {postal_code}
phone_normal: {phone_normal}
phone_free_of_charge: {phone_free_of_charge}
fax: {fax}
mobile: {mobile}
email: {email}
homepage:{homepage}
""".strip()

def build_prompt(query, search_results):
    context = ""
    
    for doc in search_results:
        context = context + entry_template.format(**doc) + "\n\n"

    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt


# In[12]:


def llm(prompt, model='gpt-4o-mini'):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content


# In[13]:


def rag(query, model='gpt-4o-mini'):
    search_results = search(query)
    prompt = build_prompt(query, search_results)
  #  print(prompt)
    answer = llm(prompt, model=model)
    return answer


# In[19]:


question = 'Where is Dr. Thomas Gross located and is he recommended?'
answer = rag(question)
print(answer)


# ## Retrieval evaluation

# In[14]:


df_question = pd.read_csv('./Find-a-Doctor/data/ground-truth-retrieval.csv')


# In[21]:


df_question.head()


# In[15]:


ground_truth = df_question.to_dict(orient='records')


# In[23]:


ground_truth[0]


# In[16]:


def hit_rate(relevance_total):
    cnt = 0

    for line in relevance_total:
        if True in line:
            cnt = cnt + 1

    return cnt / len(relevance_total)

def mrr(relevance_total):
    total_score = 0.0

    for line in relevance_total:
        for rank in range(len(line)):
            if line[rank] == True:
                total_score = total_score + 1 / (rank + 1)

    return total_score / len(relevance_total)


# In[25]:


def minsearch_search(query):
    boost = {}

    results = index.search(
        query=query,
        filter_dict={},
        boost_dict=boost,
        num_results=10
    )

    return results


# In[17]:


def evaluate(ground_truth, search_function):
    relevance_total = []

    for q in tqdm(ground_truth):
        doc_id = q['id']
        results = search_function(q)
        relevance = [d['id'] == doc_id for d in results]
        relevance_total.append(relevance)

    return {
        'hit_rate': hit_rate(relevance_total),
        'mrr': mrr(relevance_total),
    }


# In[18]:


from tqdm.auto import tqdm


# In[28]:


evaluate(ground_truth, lambda q: minsearch_search(q['question']))


# ## Finding the best parameters

# In[19]:


df_validation = df_question[:100]
df_test = df_question[100:]


# In[20]:


import random

def simple_optimize(param_ranges, objective_function, n_iterations=10):
    best_params = None
    best_score = float('-inf')  # Assuming we're minimizing. Use float('-inf') if maximizing.

    for _ in range(n_iterations):
        # Generate random parameters
        current_params = {}
        for param, (min_val, max_val) in param_ranges.items():
            if isinstance(min_val, int) and isinstance(max_val, int):
                current_params[param] = random.randint(min_val, max_val)
            else:
                current_params[param] = random.uniform(min_val, max_val)
        
        # Evaluate the objective function
        current_score = objective_function(current_params)
        
        # Update best if current is better
        if current_score > best_score:  # Change to > if maximizing
            best_score = current_score
            best_params = current_params
    
    return best_params, best_score


# In[21]:


gt_val = df_validation.to_dict(orient='records')


# In[22]:


def minsearch_search(query, boost=None):
    if boost is None:
        boost = {}

    results = index.search(
        query=query,
        filter_dict={},
        boost_dict=boost,
        num_results=10
    )

    return results


# In[26]:


param_ranges = {
    'orthopedic_surgeon_first_name': (0.0, 3.0),
    'orthopedic_surgeon_surname': (0.0, 3.0),
    'jpg_doctor': (0.0, 3.0),
    'numbers_hr': (0.0, 3.0),
    'adjusted': (0.0, 3.0),
    'number_thr': (0.0, 3.0),
    'number_bmhr': (0.0, 3.0),
    'type_of_hr_prosthesis': (0.0, 3.0),
    'type_of_thr_prosthesis': (0.0, 3.0),
    'operational_technique': (0.0, 3.0),
    'anesthetic': (0.0, 3.0),
    'cement_femur_side': (0.0, 3.0),
    'this_joint_capsule_saved_all': (0.0, 3.0),
    'city': (0.0, 3.0),
    'country': (0.0, 3.0),
    'patient-reported_positive_outcomes': (0.0, 3.0),
    'patient-reported_complications': (0.0, 3.0),
    'cut_muscles_is_fixed_again': (0.0, 3.0),
    'complete_opera_report_is_given': (0.0, 3.0),
    'hr_average_size': (0.0, 3.0),
    'hr_average_location': (0.0, 3.0),
    'assesses_x-ray': (0.0, 3.0),
    'x-ray_at_discharge': (0.0, 3.0),
    'two-sided_operation': (0.0, 3.0),
    'foreign_patients': (0.0, 3.0),
    'address': (0.0, 3.0),
    'street': (0.0, 3.0),
    'local': (0.0, 3.0),
    'postal_code': (0.0, 3.0),
    'phone_normal': (0.0, 3.0),
    'phone_free_of_charge': (0.0, 3.0),
    'fax': (0.0, 3.0),
    'mobile': (0.0, 3.0),
    'email': (0.0, 3.0),
    'homepage': (0.0, 3.0),
}

def objective(boost_params):
    def search_function(q):
        return minsearch_search(q['question'], boost_params)

    results = evaluate(gt_val, search_function)
    return results['mrr']


# In[27]:


simple_optimize(param_ranges, objective, n_iterations=20)


# In[28]:


def minsearch_improved(query):
    boost = {
        'orthopedic_surgeon_first_name': 0.45,
        'orthopedic_surgeon_surname': 2.87,
        'jpg_doctor': 0.56,
        'numbers_hr': 0.92,
        'adjusted': 1.28,
        'number_thr': 1.23,
        'number_bmhr': 0.96,
        'type_of_hr_prosthesis': 1.66,
        'type_of_thr_prosthesis': 2.72,
        'operational_technique': 2.27,
        'anesthetic': 1.78,
        'cement_femur_side': 2.20,
        'this_joint_capsule_saved_all': 1.23,
        'city': 1.36,
        'country': 1.24,
        'patient-reported_positive_outcomes': 1.26,
        'patient-reported_complications': 2.74,
        'cut_muscles_is_fixed_again': 2.17,
        'complete_opera_report_is_given': 0.06,
        'hr_average_size': 2.13,
        'hr_average_location': 2.57,
        'assesses_x-ray': 0.35,
        'x-ray_at_discharge': 0.66,
        'two-sided_operation': 1.32,
        'foreign_patients': 2.07,
        'address': 0.55,
        'street': 2.71,
        'local': 2.66,
        'postal_code': 0.36,
        'phone_normal': 1.70,
        'phone_free_of_charge': 2.77,
        'fax': 1.36,
        'mobile': 1.77,
        'email': 0.08,
        'homepage': 1.45,
    }

    results = index.search(
        query=query,
        filter_dict={},
        boost_dict=boost,
        num_results=10
    )

    return results

evaluate(ground_truth, lambda q: minsearch_improved(q['question']))


# ## RAG evaluation

# In[19]:


prompt2_template = """
You are an expert evaluator for a RAG system.
Your task is to analyze the relevance of the generated answer to the given question.
Based on the relevance of the generated answer, you will classify it
as "NON_RELEVANT", "PARTLY_RELEVANT", or "RELEVANT".

Here is the data for evaluation:

Question: {question}
Generated Answer: {answer_llm}

Please analyze the content and context of the generated answer in relation to the question
and provide your evaluation in parsable JSON without using code blocks:

{{
  "Relevance": "NON_RELEVANT" | "PARTLY_RELEVANT" | "RELEVANT",
  "Explanation": "[Provide a brief explanation for your evaluation]"
}}
""".strip()


# In[30]:


len(ground_truth)


# In[20]:


record = ground_truth[0]
question = record['question']
answer_llm = rag(question)


# In[32]:


record


# In[33]:


print(answer_llm)


# In[34]:


prompt = prompt2_template.format(question=question, answer_llm=answer_llm)
print(prompt)


# In[21]:


import json


# In[22]:


df_sample = df_question.sample(n=200, random_state=1)


# In[23]:


sample = df_sample.to_dict(orient='records')


# In[38]:


evaluations = []

for record in tqdm(sample):
    question = record['question']
    answer_llm = rag(question) 

    prompt = prompt2_template.format(
        question=question,
        answer_llm=answer_llm
    )

    evaluation = llm(prompt)
    evaluation = json.loads(evaluation)

    evaluations.append((record, answer_llm, evaluation))


# In[39]:


df_eval = pd.DataFrame(evaluations, columns=['record', 'answer', 'evaluation'])

df_eval['id'] = df_eval.record.apply(lambda d: d['id'])
df_eval['question'] = df_eval.record.apply(lambda d: d['question'])

df_eval['relevance'] = df_eval.evaluation.apply(lambda d: d['Relevance'])
df_eval['explanation'] = df_eval.evaluation.apply(lambda d: d['Explanation'])

del df_eval['record']
del df_eval['evaluation']


# In[40]:


df_eval.relevance.value_counts(normalize=True)


# In[41]:


df_eval.to_csv('./Find-a-Doctor//data/rag-eval-gpt-4o-mini.csv', index=False)


# In[42]:


df_eval[df_eval.relevance == 'NON_RELEVANT']


# In[27]:


# Importing Necessary Libraries

import os
from tqdm.auto import tqdm
from groq import Groq
from litellm import completion
# Instantiation of Groq Client

client = Groq(

    api_key=os.environ.get("GROQ_SECRET_ACCESS_KEY"),

)



# In[25]:


evaluation_groq = []
for record in tqdm(sample):
    question = record['question']
    answer_llm = rag(question, model="groq/llama3-8b-8192") 

    prompt = prompt2_template.format(
        question=question,
        answer_llm=answer_llm
    )

    evaluation = llm(prompt)
    evaluation = json.loads(evaluation)
    
    evaluations_groq.append((record, answer_llm, evaluation))


# In[33]:


evaluations_gpt4o = []

for record in tqdm(sample):
    question = record['question']
    answer_llm = rag(question, model='gpt-4o') 

    prompt = prompt2_template.format(
        question=question,
        answer_llm=answer_llm
    )

    evaluation = llm(prompt)
    evaluation = json.loads(evaluation)
    
    evaluations_gpt35turbo.append((record, answer_llm, evaluation))


# In[101]:


df_eval = pd.DataFrame(evaluations_gpt4o, columns=['record', 'answer', 'evaluation'])

df_eval['id'] = df_eval.record.apply(lambda d: d['id'])
df_eval['question'] = df_eval.record.apply(lambda d: d['question'])

df_eval['relevance'] = df_eval.evaluation.apply(lambda d: d['Relevance'])
df_eval['explanation'] = df_eval.evaluation.apply(lambda d: d['Explanation'])

del df_eval['record']
del df_eval['evaluation']


# In[102]:


df_eval.relevance.value_counts()


# In[103]:


df_eval.relevance.value_counts(normalize=True)


# In[104]:


df_eval.to_csv('../data/rag-eval-gpt-4o.csv', index=False)


# In[ ]:




