from langchain.output_parsers import PydanticOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str
    quantity: int
    subtotal: float


class Receipt(BaseModel):
    store_name: str
    date: str = Field(
        ..., description="Write the date in ISO Format YYYY-MM-DDTHH:mm:ss"
    )
    items: list[Item]
    total: float


parser = PydanticOutputParser(pydantic_object=Receipt)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)


def parse_receipt_text(image_bytes: bytes) -> Receipt:
    import base64

    # Encode bytes to base64
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    message = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": f"parse this receipt in this image using the following format:\n {parser.get_format_instructions()}",
            },
            {
                "type": "image",
                "source_type": "base64",
                "data": encoded,
                "mime_type": "image/jpeg",
            },
        ],
    }
    raw_json = llm.invoke([message]).content
    return parser.invoke(raw_json)
