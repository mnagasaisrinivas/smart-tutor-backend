from langchain.output_parsers.structured import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate
from .openrouter_api_call import call_openrouter

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
    return parser.parse(call_openrouter(final_prompt))
