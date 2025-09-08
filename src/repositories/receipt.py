from sqlalchemy.orm import Session

from models import ItemTable, ReceiptTable
from services.scanner import Item, Receipt


def add(session: Session, receipt: Receipt) -> int:
    """Add a receipt and return its ID."""
    db_receipt = ReceiptTable(
        store_name=receipt.store_name,
        date=receipt.date,
        total=receipt.total,
        items=[
            ItemTable(
                name=item.name, quantity=item.quantity, subtotal=item.subtotal
            )
            for item in receipt.items
        ],
    )
    session.add(db_receipt)
    session.commit()
    session.refresh(db_receipt)
    return db_receipt.id


def get_by_date(session: Session, date: str) -> list[Receipt]:
    """Retrieve all receipts by date."""
    results = (
        session.query(ReceiptTable).filter(ReceiptTable.date == date).all()
    )

    receipts: list[Receipt] = []
    for r in results:
        receipts.append(
            Receipt(
                store_name=r.store_name,
                date=r.date,
                total=r.total,
                items=[
                    Item(name=i.name, quantity=i.quantity, subtotal=i.subtotal)
                    for i in r.items
                ],
            )
        )
    return receipts
