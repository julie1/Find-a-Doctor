import json

from time import time

from openai import OpenAI

import ingest


client = OpenAI()
index = ingest.load_index()

def search(query):
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
        'homepage': 1.45,}
     results = index.search(query=query, filter_dict={}, boost_dict=boost, num_results=10)

     return results


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


def llm(prompt, model="gpt-4o-mini"):
    response = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content

    token_stats = {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens,
    }

    return answer, token_stats


evaluation_prompt_template = """
You are an expert evaluator for a RAG system.
Your task is to analyze the relevance of the generated answer to the given question.
Based on the relevance of the generated answer, you will classify it
as "NON_RELEVANT", "PARTLY_RELEVANT", or "RELEVANT".

Here is the data for evaluation:

Question: {question}
Generated Answer: {answer}

Please analyze the content and context of the generated answer in relation to the question
and provide your evaluation in parsable JSON without using code blocks:

{{
  "Relevance": "NON_RELEVANT" | "PARTLY_RELEVANT" | "RELEVANT",
  "Explanation": "[Provide a brief explanation for your evaluation]"
}}
""".strip()


def evaluate_relevance(question, answer):
    prompt = evaluation_prompt_template.format(question=question, answer=answer)
    evaluation, tokens = llm(prompt, model="gpt-4o-mini")

    try:
        json_eval = json.loads(evaluation)
        return json_eval, tokens
    except json.JSONDecodeError:
        result = {"Relevance": "UNKNOWN", "Explanation": "Failed to parse evaluation"}
        return result, tokens


def calculate_openai_cost(model, tokens):
    openai_cost = 0

    if model == "gpt-4o-mini":
        openai_cost = (
            tokens["prompt_tokens"] * 0.00015 + tokens["completion_tokens"] * 0.0006
        ) / 1000
    else:
        print("Model not recognized. OpenAI cost calculation failed.")

    return openai_cost


def rag(query, model="gpt-4o-mini"):
    t0 = time()

    search_results = search(query)
    prompt = build_prompt(query, search_results)
    answer, token_stats = llm(prompt, model=model)

    relevance, rel_token_stats = evaluate_relevance(query, answer)

    t1 = time()
    took = t1 - t0

    openai_cost_rag = calculate_openai_cost(model, token_stats)
    openai_cost_eval = calculate_openai_cost(model, rel_token_stats)

    openai_cost = openai_cost_rag + openai_cost_eval

    answer_data = {
        "answer": answer,
        "model_used": model,
        "response_time": took,
        "relevance": relevance.get("Relevance", "UNKNOWN"),
        "relevance_explanation": relevance.get(
            "Explanation", "Failed to parse evaluation"
        ),
        "prompt_tokens": token_stats["prompt_tokens"],
        "completion_tokens": token_stats["completion_tokens"],
        "total_tokens": token_stats["total_tokens"],
        "eval_prompt_tokens": rel_token_stats["prompt_tokens"],
        "eval_completion_tokens": rel_token_stats["completion_tokens"],
        "eval_total_tokens": rel_token_stats["total_tokens"],
        "openai_cost": openai_cost,
    }

    return answer_data
