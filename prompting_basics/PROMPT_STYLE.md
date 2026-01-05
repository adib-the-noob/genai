
# Prompt Styles Guide

## Alpaca Format
```
Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{instruction}

### Input:
{input}

### Response:
{response}
```

## OpenAI / ChatML Format
```json
{
    "messages": [
        {"role": "system", "content": "{system_prompt}"},
        {"role": "user", "content": "{user_message}"},
        {"role": "assistant", "content": "{response}"}
    ]
}
```

## Llama 2 Chat Format
```
<s>[INST] <<SYS>>
{system_prompt}
<</SYS>>

{user_message} [/INST] {response} </s>
```

## Mistral Format
```
[INST] {instruction} [/INST] {response}
```

## Claude Format
```
Human: {user_message}