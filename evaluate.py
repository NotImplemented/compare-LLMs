import logging
import openai
import os
import json
import requests

from human_eval.data import write_jsonl, read_problems
from human_eval.evaluation import evaluate_functional_correctness
from retry_with_backoff import completions_with_backoff


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


openai_models = ['gpt-4o', 'o1', 'o3-mini', 'gpt-3.5-turbo']
air_models = ['chatgpt', 'deepseek', 'llama', 'claude']


def evaluate_score(file_name, model_name, temperature):
    total = 0
    passed = 0
    with open(file_name) as f:
        for line in f:
            total += 1
            result = json.loads(line)

            passed += result['passed']
    logging.info(f'{model_name.upper()}, temperature = {temperature}: {passed} / {total}, {int(passed * 100 / total)}%')


def generate_prompt(problem_description):
    return f'''Hello, this is a coding interview. I will give you a problem statement with sample
test cases and a code snippet. I expect you to write the most effective working
code using python3. Here is the problem statement: 

{problem_description}

Do not alter function signature in the code snippet. Output
only valid source code which could be run as-is without any fixes, 
improvements or changes.
'''


def generate_one_completion(problem_description, model_name):
    prompt = generate_prompt(problem_description)

    solution = completions_with_backoff(
        model=model_name,
        store=True,
        max_tokens=512,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    solution = solution.replace('```python', '').replace('```', '')
    return solution


def generate_one_completion_air(problem_description, model_name, temperature):

    print(problem_description)
    prompt = generate_prompt(problem_description)

    url = 'https://api.air.fail/public/text/' + model_name

    message = {"content": prompt, "info": {"version": "gpt4-o-mini", "temperature": temperature}}
    headers = {
        'Authorization': os.environ['AIR_KEY'], 
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=json.dumps(message))
    print(response)
    solution = response.json()[0]['content']
    solution = solution.replace('```python', '').replace('```', '')
    return solution


if __name__ == '__main__':  
    for model_name in ['chatgpt']:
        for temperature in [0.25, 0.5, 0.75, 1.0]:
            problems = read_problems()
            file_name = model_name + "_temp" + str(temperature) + "_samples.jsonl"
            logging.info(f'Model name: {model_name}, temperature: {temperature}, Total problems: {len(problems)}')
            
            if not os.path.isfile(file_name):
                samples = []
                for index, task_id in enumerate(problems):
                    logging.info(f'Processing problem #{index}')
                    samples.append(
                        dict(task_id=task_id, completion=generate_one_completion_air(problems[task_id]["prompt"], model_name, temperature))
                    )
                write_jsonl(file_name, samples)

            evaluate_functional_correctness(file_name, [1])
            evaluate_score(file_name + '_results.jsonl', model_name, temperature)