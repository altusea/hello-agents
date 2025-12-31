from smolagents import CodeAgent, LiteLLMModel

from ulib.utils.env_reader import read_deepseek_api_key

api_key = read_deepseek_api_key()
api_base = "https://api.deepseek.com/v1"
model_id = "deepseek-chat"

model = LiteLLMModel(model_id=model_id, api_base=api_base, api_key=api_key)
agent = CodeAgent(tools=[], model=model, add_base_tools=True)


# Run the agent with a task
result = agent.run("Calculate the sum of numbers from 1 to 10")
print(result)
