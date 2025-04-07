### Compare coding accuracy of Large Language Models

This is an attempt to benchmark LLM's performance on coding tasks. 
Use hand-written problem set [Human-Eval](https://github.com/openai/human-eval) which contains problem desriptions and test cases,
described in paper "[Evaluating Large Language Models Trained on Code](https://arxiv.org/abs/2107.03374)".


The same prompt was used for every LLM and every problem:

  _Hello, this is a coding interview. I will give you a problem statement with sample test cases and a code snippet._
  _I expect you to write the most effective working code using python3. Here is the problem statement:_

  **Problem Description**  
  
  _Do not alter function signature in the code snippet. Output only valid source code which could be run as-is without any fixes, improvements or changes._


LLM makes only one attempt to generate code without any prior information about the problem and without knowing its test cases.
There is no mechanism to provide feedback or fix the code after it is generated.
Test set consisted of 32 problems from aforementioned dataset. Sample problem desription is as follows:
```
from typing import List

def below_zero(operations: List[int]) -> bool:
    """ You're given a list of deposit and withdrawal operations on a bank account that starts with
    zero balance. Your task is to detect if at any point the balance of account falls below zero, and
    at that point function should return True. Otherwise it should return False.
    >>> below_zero([1, 2, 3])
    False
    >>> below_zero([1, 2, -4, 5])
    True
    """
```

Output produced by gpt-4o-mini (temperature = 0.25):
```
from typing import List

def below_zero(operations: List[int]) -> bool:
    """ You're given a list of deposit and withdrawal operations on a bank account that starts with
    zero balance. Your task is to detect if at any point the balance of account falls below zero, and
    at that point function should return True. Otherwise it should return False.
    >>> below_zero([1, 2, 3])
    False
    >>> below_zero([1, 2, -4, 5])
    True
    """
    balance = 0
    for operation in operations:
        balance += operation
        if balance < 0:
            return True
    return False
```

### Results
Small data set (32 problems):
Temperature | gpt-4o | gpt-4o-mini | claude (sonnet 3.5)|
---- | ------------- | ------------ | --- |
0.25 | 31 / 32, 96%  | 30 / 32, 93% | --- |
0.5  | 30 / 32, 93%  | 30 / 32, 93% | --- |
0.75 | 31 / 32, 96%  | 29 / 32, 91% | --- |
1.0  | 32 / 32, 100% | 28 / 32, 88% | --- |

Large data set (64 problems):
Temperature | gpt-4o | gpt-4o-mini   | claude (sonnet 3.5)|
---- | ------------- | ------------- | ------------- |
0.25 |  61 / 64, 95% | 61 / 64, 95%  | 64 / 64, 100% |
0.5  |  61 / 64, 95% | 64 / 64, 100% | 64 / 64, 100% |
0.75 |  60 / 64, 93% | 60 / 64, 93%  | 64 / 64, 100% |
1.0  |  63 / 64, 98% | 63 / 64, 98%  | 63 / 64, 98%  |

##### Conclusions
LLMs are capable of solving easy problems, demonstrating >90% accuracy

### Future directions
1. Improve the initial prompt and tune it for each model separately.
2. Provide feedback on unsuccessful attempts to improve the result incrementally. That would make the process of solving to be much closer to real-life settings.
3. Prepare problem descriptions, making them more "suitable" for models to digest. 
