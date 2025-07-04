from langchain.output_parsers.structured import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate
from .openrouter_api_call import call_openrouter


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
    parsed = parser.parse(call_openrouter(final_prompt))
    return parsed