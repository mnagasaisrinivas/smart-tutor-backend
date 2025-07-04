from langchain.output_parsers.structured import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate
from .openrouter_api_call import call_openrouter

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
    return parser.parse(call_openrouter(final_prompt))
