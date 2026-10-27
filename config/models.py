import enum

from sqlalchemy import (
    Boolean, CheckConstraint, Column, Date, DateTime, Enum, ForeignKey,
    Integer, Numeric, String, Text, func,
)
from sqlalchemy.orm import relationship, validates

from .database import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint(
            "email IS NOT NULL OR phone_number IS NOT NULL",
            name="ck_user_email_or_phone_number",
        ),
    )

    id = Column(Integer, primary_key=True)
    username = Column(String(40), unique=True, nullable=False, index=True)
    full_name = Column(String(100), nullable=True)
    email = Column(String(255), unique=True, nullable=True)
    phone_number = Column(String(20), unique=True, nullable=True)
    password = Column(Text, nullable=False)

    is_staff = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(),
        onupdate=func.now(), nullable=False,
    )

    given_debts = relationship(
        "Qarz", foreign_keys="Qarz.lender_id",
        back_populates="lender", lazy="selectin",
    )  # bergan qarzlari
    received_debts = relationship(
        "Qarz", foreign_keys="Qarz.borrower_id",
        back_populates="borrower", lazy="selectin",
    )  # olgan qarzlari

    @validates("email")
    def _normalize_email(self, key, value):
        return value.strip().lower() if value else None

    def __repr__(self):
        return f"<User id={self.id} username={self.username!r}>"


class Valyuta(str, enum.Enum):
    UZS = "UZS"
    USD = "USD"


class QarzStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    PAID = "PAID"
    CANCELLED = "CANCELLED"


class Qarz(Base):
    __tablename__ = "qarzlar"
    __table_args__ = (
        CheckConstraint("lender_id <> borrower_id", name="ck_qarz_different_users"),
        CheckConstraint("miqdor > 0", name="ck_qarz_miqdor_positive"),
    )

    id = Column(Integer, primary_key=True)
    lender_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    borrower_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    miqdor = Column(Numeric(14, 2), nullable=False)
    valyuta = Column(Enum(Valyuta), default=Valyuta.UZS, nullable=False)
    status = Column(Enum(QarzStatus), default=QarzStatus.ACTIVE, nullable=False, index=True)
    qaytarish_muddati = Column(Date, nullable=False, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(),
        onupdate=func.now(), nullable=False,
    )

    lender = relationship("User", foreign_keys=[lender_id], back_populates="given_debts")
    borrower = relationship("User", foreign_keys=[borrower_id], back_populates="received_debts")
    tolovlar = relationship(
        "Tolov", back_populates="qarz",
        cascade="all, delete-orphan", lazy="selectin",
    )

    @property
    def qoldiq(self):
        return self.miqdor - sum((t.miqdor for t in self.tolovlar), 0)

    def __repr__(self):
        return f"<Qarz id={self.id} {self.miqdor} {self.valyuta.value}>"


class Tolov(Base):
    __tablename__ = "tolovlar"
    __table_args__ = (
        CheckConstraint("miqdor > 0", name="ck_tolov_miqdor_positive"),
    )

    id = Column(Integer, primary_key=True)
    qarz_id = Column(Integer, ForeignKey("qarzlar.id", ondelete="CASCADE"), nullable=False, index=True)
    miqdor = Column(Numeric(14, 2), nullable=False)
    paid_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    qarz = relationship("Qarz", back_populates="tolovlar")