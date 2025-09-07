import io

import pytesseract
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from PIL import Image
from pydantic import BaseModel


def scan_receipt(image_bytes: bytes) -> str:
    image = Image.open(io.BytesIO(image_bytes))

    return pytesseract.image_to_string(image)


class Item(BaseModel):
    name: str
    quantity: int
    subtotal: float


class Receipt(BaseModel):
    store_name: str
    date: str
    items: list[Item]
    total: float


parser = PydanticOutputParser(pydantic_object=Receipt)

prompt = PromptTemplate(
    template=(
        "Extract the receipt information from the text below.\n\n"
        "Text:\n{receipt_text}\n\n"
        "{format_instructions}"
    ),
    input_variables=["receipt_text"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)


def parse_receipt_text(receipt_text: str) -> Receipt:
    """
    Parse raw OCR text into a structured Receipt Pydantic object.
    """
    chain = prompt | llm | parser
    return chain.invoke({"receipt_text": receipt_text})
