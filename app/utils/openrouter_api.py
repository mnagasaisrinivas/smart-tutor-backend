import os
import requests
from langchain.output_parsers.structured import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def _call_openrouter(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "deepseek/deepseek-chat-v3-0324:free",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def get_structured_explanation(subject: str, question: str) -> str:
    schemas = [
        ResponseSchema(name="title", description="A short title for the explanation"),
        ResponseSchema(name="steps", description="Step-by-step explanation of the question", type = "list[string]"),
        ResponseSchema(name="summary", description="A brief summary of the concept")
    ]
    parser = StructuredOutputParser.from_response_schemas(schemas)

    prompt = PromptTemplate(
        template="""
You are a tutor. Explain the following {subject} question:

Question: {question}

Use this format:
{format_instructions}
        """,
        input_variables=["subject", "question"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    final_prompt = prompt.format(subject=subject, question=question)
    parsed = parser.parse(_call_openrouter(final_prompt))
    return parsed

def get_study_notes(subject: str, topic: str) -> str:
    schemas = [
        ResponseSchema(name="heading", description="Main heading for the topic"),
        ResponseSchema(name="bullet_points", description="Key points to study")
    ]
    parser = StructuredOutputParser.from_response_schemas(schemas)

    prompt = PromptTemplate(
        template="""
Create concise study notes for {subject} on the topic '{topic}'.
Use this structure:
{format_instructions}
        """,
        input_variables=["subject", "topic"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    final_prompt = prompt.format(subject=subject, topic=topic)
    parsed = parser.parse(_call_openrouter(final_prompt))
    return parsed

def get_practice_problems(subject: str, topic: str) -> list[str]:
    schemas = [ 
        ResponseSchema(name="practice_problems", description="List of practice problems", type = "list[string]"),
        ResponseSchema(name="explanations", description="Explanations for each practice problem", type = "list[string]"),
        ]
    parser = StructuredOutputParser.from_response_schemas(schemas)

    prompt = PromptTemplate(
        template="""
Generate practice problems for {subject} on the topic '{topic}'.
{format_instructions}
        """,
        input_variables=["subject", "topic"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    final_prompt = prompt.format(subject=subject, topic=topic)
    return parser.parse(_call_openrouter(final_prompt))

def get_quiz_questions(subject: str, topic: str) -> list[dict]:
    schemas = [ResponseSchema(name="questions", description="List of quiz questions with options and correctAnswer")]
    parser = StructuredOutputParser.from_response_schemas(schemas)

    prompt = PromptTemplate(
        template="""
Create a 5-question multiple choice quiz for the subject: {subject} on the topic {topic}.
Each question must include:
- id: numerically increasing id for the question
- question: string
- options: list of 4 strings
- correctAnswer: index of correct option (0-3)

{format_instructions}
        """,
        input_variables=["subject", "topic"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    final_prompt = prompt.format(subject=subject, topic=topic)
    return parser.parse(_call_openrouter(final_prompt))
