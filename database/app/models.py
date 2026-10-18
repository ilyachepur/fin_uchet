from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, DECIMAL, Date, ForeignKey, Enum, func
from sqlalchemy.orm import declarative_base
import datetime
import enum

Base = declarative_base()

# ENUM для типа категории 
class CategoryType(str, enum.Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"

# 1. Таблица Пользователи 
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=True)
    phone = Column(String(20), unique=True, nullable=True)
    yandex_id = Column(String(255), unique=True, nullable=True)
    vk_id = Column(String(255), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# 2. Таблица Проекты 
class BusinessProject(Base):
    __tablename__ = 'business_projects'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# 3. Таблица Категории 
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    name = Column(String(255), nullable=False)
    type = Column(Enum(CategoryType), nullable=False)
    is_system = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

# 4. Транзакции доходов
class IncomeTransaction(Base):
    __tablename__ = 'income_transactions'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    project_id = Column(Integer, ForeignKey('business_projects.id', ondelete='RESTRICT'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    amount = Column(DECIMAL(15, 2), nullable=False)
    
    date_fact = Column(Date, nullable=False)      
    date_period = Column(Date, nullable=False)    
    
    comment = Column(Text, nullable=True)
    attachment_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# 5. Транзакции расходов
class ExpenseTransaction(Base):
    __tablename__ = 'expense_transactions'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    project_id = Column(Integer, ForeignKey('business_projects.id', ondelete='RESTRICT'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    amount = Column(DECIMAL(15, 2), nullable=False)
    
    date_fact = Column(Date, nullable=False)
    date_period = Column(Date, nullable=False)
    
    comment = Column(Text, nullable=True)
    attachment_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
