from deepseek_r1_agent import DeepseekR1Agent
from deepseek_r1_agent.history_generator import DeepseekR1HistoryGenerator
from json_is_all_for_context.agent.agent_executor import AgentExecutor, SimpleAgentExecutor
from deepseek_r1_agent.functions.get_current_weather import GetCurrentWeather
from deepseek_r1_agent.functions.search_web import SearchWeb

agent = DeepseekR1Agent("../DeepSeek-R1-Distill-Qwen-14B-GGUF/DeepSeek-R1-Distill-Qwen-14B-Q4_0.gguf")
agent_executor = SimpleAgentExecutor(agent, DeepseekR1HistoryGenerator())
agent_executor.bind_functions([GetCurrentWeather(), SearchWeb()])

print(agent_executor.invoke("current president of korea."))
