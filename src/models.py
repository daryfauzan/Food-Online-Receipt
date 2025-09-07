from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class ReceiptTable(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    store_name = Column(String, nullable=False)
    date = Column(String, nullable=False)
    total = Column(Float, nullable=False)

    items = relationship(
        "ItemTable", back_populates="receipt", cascade="all, delete-orphan"
    )


class ItemTable(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    receipt_id = Column(Integer, ForeignKey("receipts.id"), nullable=False)
    name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Float, nullable=False)

    receipt = relationship("ReceiptTable", back_populates="items")
