from pydantic import BaseModel


class Agent(BaseModel):
    """
    An agent is a type of chain that has agency.
    It works following the ReAct framework, which is a combination of reasoning and acting.
    """
    pass


"""
curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-r1-distill-qwen-7b",
    "messages": [
      { "role": "system", "content": "Always answer in rhymes. Today is Thursday" },
      { "role": "user", "content": "What day is it today?" }
    ],
    "temperature": 0.7,
    "max_tokens": -1,
    "stream": false
}
"""
