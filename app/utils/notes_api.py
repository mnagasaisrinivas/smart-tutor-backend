from langchain.output_parsers.structured import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate
from .openrouter_api_call import call_openrouter


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
    parsed = parser.parse(call_openrouter(final_prompt))
    return parsed