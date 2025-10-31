import os
import requests
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
import litellm

# ---------------------------------------------------------------------
# 1. Load environment variables
# ---------------------------------------------------------------------
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# ---------------------------------------------------------------------
# 2. Configure LiteLLM globally for OpenRouter
# ---------------------------------------------------------------------
litellm.api_key = OPENROUTER_API_KEY
litellm.api_base = "https://openrouter.ai/api/v1"
model_name = "openrouter/mistralai/mistral-7b-instruct"

# ---------------------------------------------------------------------
# 3. Define Agents
# ---------------------------------------------------------------------
planner = Agent(
    role="Planner",
    goal="Create a structured 3-step plan with goals and deliverables.",
    backstory="A strategic AI project planner who designs clear blueprints.",
    allow_delegation=True,
    llm=model_name,
)

specialist = Agent(
    role="Specialist",
    goal="Execute the Planner’s 3-step plan and summarize the results clearly.",
    backstory="A detail-oriented AI engineer capable of executing complex plans.",
    llm=model_name,
)

weather_agent = Agent(
    role="Weather Expert",
    goal="Provide accurate weather updates for any city.",
    backstory="You specialize in weather forecasting using OpenWeather API.",
    llm=model_name,
)

chat_agent = Agent(
    role="Chat Assistant",
    goal="Engage in helpful and friendly conversation.",
    backstory="You are a general-purpose AI assistant.",
    llm=model_name,
)

# ---------------------------------------------------------------------
# 4. Define Tasks
# ---------------------------------------------------------------------
plan_task = Task(
    description="Given the topic, create a 3-step plan with goals and deliverables.",
    expected_output="A structured plan with 3 steps, each having a goal and deliverable.",
    agent=planner,
)

execute_task = Task(
    description="Take the Planner’s 3-step plan and write a short summary of what was achieved.",
    expected_output="A 3-point summary explaining the outcomes for each step.",
    agent=specialist,
)

weather_task = Task(
    description="Get the current weather for a specified city using OpenWeather API.",
    expected_output="A short weather summary including temperature and conditions.",
    agent=weather_agent,
)

chat_task = Task(
    description="Respond to general user queries in a helpful and concise way.",
    expected_output="A friendly and informative response.",
    agent=chat_agent,
)

# ---------------------------------------------------------------------
# 5. Weather Utility Functions
# ---------------------------------------------------------------------
def is_weather_query(user_input):
    keywords = ["weather", "temperature", "forecast", "rain", "sunny", "climate"]
    return any(word in user_input.lower() for word in keywords)

def extract_city(user_input):
    words = user_input.split()
    for i, word in enumerate(words):
        if word.lower() in ["in", "at", "for"] and i + 1 < len(words):
            return words[i + 1]
    return None

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        return f"The weather in {city.title()} is {desc} with a temperature of {temp}°C (feels like {feels_like}°C)."
    else:
        return f"Could not fetch weather for '{city}'. Check the city name."

# ---------------------------------------------------------------------
# 6. Chat Dispatcher
# ---------------------------------------------------------------------
def chat_with_crewai(user_input):
    if is_weather_query(user_input):
        city = extract_city(user_input)
        if city:
            return get_weather(city)
        else:
            return "Please specify a city to get the weather information."
    elif "plan" in user_input.lower() or "project" in user_input.lower():
        topic = user_input
        crew = Crew(agents=[planner, specialist], tasks=[plan_task, execute_task], process=Process.sequential)
        result = crew.kickoff(inputs={"topic": topic})
        return result
    else:
        crew = Crew(agents=[chat_agent], tasks=[chat_task], process=Process.sequential)
        result = crew.kickoff(inputs={"user_input": user_input})
        return result

# ---------------------------------------------------------------------
# 7. Main Loop
# ---------------------------------------------------------------------
if __name__ == "__main__":
    print("CrewAI chatbot is ready. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Bot: Goodbye.")
            break
        reply = chat_with_crewai(user_input)
        print(f"Bot: {reply}")
