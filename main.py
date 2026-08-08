from pydantic import BaseModel
from langchain.agents import create_agent
from dotenv import load_dotenv,find_dotenv
from langchain.tools import tool
import requests
import os

load_dotenv(find_dotenv())

token = os.environ["TOPAS_TOKEN"]

class Answer(BaseModel):
    summary: str
    confidence: float

@tool
def find_grade(employee_name: str) -> str:
    """Find the grade of an Employee.

    Args:
        query: name of the Employee
    """
    return "G3.2"

@tool
def find_all_employees() -> int:
    """Make a REST API call to get Count all the Employees of Company 'Incture'
    Args:
        No args API call
    """
    url = 'https://topas-backend.cherrywork.com/master/getAllEmployeesV2'

    try:
        response = requests.get(url, timeout=10, headers={ "Authorization": f"Bearer {token}"})
        if response.status_code != 200:
            return "find_all_employees API call failed."
        api_response = response.json()
        # return api_response["data"]
        return len(api_response["data"])
    except requests.exceptions.RequestException as e:
        return f"Network error connecting to the API: {str(e)}"

@tool
def find_employee_details(employee_code: str) -> str:
    """Make a REST API call to get the employee details
    Args:
        employee_code: 8 Letter Employee Code
    """
    return None

tools = [find_all_employees]

agent = create_agent(model="openai:gpt-4.1", tools=tools, response_format=Answer, system_prompt="You are a helpful assistant. Be concise and accurate.")
result = agent.invoke({"messages": [{"role": "user", "content": "How many employees are there in Incture"}]})

print(result["structured_response"])