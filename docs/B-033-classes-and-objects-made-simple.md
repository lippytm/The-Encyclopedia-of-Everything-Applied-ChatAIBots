# B-033: Classes and Objects Made Simple

### class, \_\_init\_\_, Methods, and the dataclasses Revolution

> *"Object-oriented programming is not about complexity — it's about bundling data and behavior together so that each piece of your program knows what it is and what it can do. A class is just a template. An object is a living instance of that template. Once you understand this, you can model anything."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Define classes with `__init__`, instance attributes, and methods
2. Understand `self` — what it is and why it exists
3. Use `@property`, `@classmethod`, and `@staticmethod`
4. Use `@dataclass` for clean, modern data modeling
5. Build a `bank-account.py` simulator with deposits, withdrawals, and history

**Prerequisite:** B-026 through B-032

**Build Artifact:** `~/developer-workspace/projects/python-foundations/bank_account.py`

**Credential:** `CCSLL-L1-B033-OOPEngineer` — on-chain on Base

---

## Chapter 1: Your First Class

```python
# A class is a blueprint. An object is an instance of that blueprint.

class Dog:
    """A simple dog class."""

    def __init__(self, name: str, breed: str) -> None:
        # __init__ runs when you create a new Dog
        # self refers to THIS specific dog instance
        self.name  = name
        self.breed = breed

    def speak(self) -> str:
        return f"{self.name} says: Woof!"

    def __repr__(self) -> str:
        """How the object shows in the REPL / print()."""
        return f"Dog(name={self.name!r}, breed={self.breed!r})"


# Create instances
rex   = Dog("Rex", "German Shepherd")
buddy = Dog("Buddy", "Labrador")

print(rex.name)        # Rex
print(buddy.speak())   # Buddy says: Woof!
print(rex)             # Dog(name='Rex', breed='German Shepherd')
print(type(rex))       # <class '__main__.Dog'>
```

---

## Chapter 2: Instance Attributes and Methods

```python
class Counter:
    """A counter that tracks its own value and history."""

    def __init__(self, start: int = 0) -> None:
        self.value   = start
        self._history: list[int] = [start]   # private by convention (leading _)

    def increment(self, amount: int = 1) -> None:
        self.value += amount
        self._history.append(self.value)

    def decrement(self, amount: int = 1) -> None:
        self.value -= amount
        self._history.append(self.value)

    def reset(self) -> None:
        self.value = 0
        self._history.append(0)

    def history(self) -> list[int]:
        return list(self._history)   # return a copy


c = Counter(10)
c.increment(5)
c.increment(3)
c.decrement(2)
print(c.value)      # 16
print(c.history())  # [10, 15, 18, 16]
```

---

## Chapter 3: @property, @classmethod, @staticmethod

```python
class Temperature:
    """Temperature with Celsius storage and Fahrenheit property."""

    def __init__(self, celsius: float) -> None:
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        """Read-only Celsius value."""
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < -273.15:
            raise ValueError("Temperature below absolute zero!")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        """Computed Fahrenheit — never stored, always calculated."""
        return self._celsius * 9/5 + 32

    @classmethod
    def from_fahrenheit(cls, fahrenheit: float) -> "Temperature":
        """Create a Temperature from Fahrenheit — alternate constructor."""
        return cls((fahrenheit - 32) * 5/9)

    @staticmethod
    def is_freezing(celsius: float) -> bool:
        """Static — doesn't need self or cls."""
        return celsius <= 0

    def __repr__(self) -> str:
        return f"Temperature({self._celsius:.1f}°C / {self.fahrenheit:.1f}°F)"


t1 = Temperature(100)
print(t1)                          # Temperature(100.0°C / 212.0°F)
print(t1.fahrenheit)               # 212.0

t2 = Temperature.from_fahrenheit(32)
print(t2)                          # Temperature(0.0°C / 32.0°F)

print(Temperature.is_freezing(5))  # False
print(Temperature.is_freezing(-1)) # True
```

---

## Chapter 4: Inheritance

```python
class Animal:
    def __init__(self, name: str) -> None:
        self.name = name

    def speak(self) -> str:
        raise NotImplementedError("Subclass must implement speak()")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name!r})"


class Cat(Animal):
    def speak(self) -> str:
        return f"{self.name} says: Meow!"


class Dog(Animal):
    def speak(self) -> str:
        return f"{self.name} says: Woof!"


animals = [Cat("Whiskers"), Dog("Rex"), Cat("Luna")]
for animal in animals:
    print(animal.speak())   # polymorphism — each speaks differently
```

---

## Chapter 5: dataclasses — Modern Python Data Modeling

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

# @dataclass auto-generates __init__, __repr__, __eq__
@dataclass
class Transaction:
    amount:      float
    description: str
    timestamp:   datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self) -> None:
        if self.amount == 0:
            raise ValueError("Transaction amount cannot be zero")


@dataclass
class BookRecord:
    book_id:     str
    title:       str
    credential:  str
    level:       int = 1
    g13_approved: bool = False
    tags:        List[str] = field(default_factory=list)

    def activate(self) -> None:
        self.g13_approved = True

    def __repr__(self) -> str:
        status = "✅" if self.g13_approved else "⏳"
        return f"{status} [{self.book_id}] {self.title}"


b = BookRecord("B-033", "Classes and Objects Made Simple", "CCSLL-L1-B033-OOPEngineer")
print(b)           # ⏳ [B-033] Classes and Objects Made Simple
b.activate()
print(b)           # ✅ [B-033] Classes and Objects Made Simple
```

---

## Chapter 6: The Build — Bank Account Simulator

```python
#!/usr/bin/env python3
"""
bank_account.py — B-033 Build Artifact

A bank account simulator demonstrating:
- Classes with __init__, methods, properties
- Transaction history as a list of dataclasses
- Custom exceptions for business logic violations
- @property for computed balance
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List


class InsufficientFundsError(Exception):
    """Raised when a withdrawal exceeds the account balance."""
    def __init__(self, requested: float, available: float) -> None:
        self.requested = requested
        self.available = available
        super().__init__(
            f"Cannot withdraw ${requested:.2f} — only ${available:.2f} available"
        )


class NegativeAmountError(ValueError):
    """Raised when a deposit or withdrawal amount is negative."""
    pass


@dataclass
class Transaction:
    type:        str        # "deposit" | "withdrawal"
    amount:      float
    description: str
    timestamp:   str = field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
    balance_after: float = 0.0


class BankAccount:
    """A bank account with full transaction history."""

    def __init__(self, owner: str, initial_balance: float = 0.0) -> None:
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self.owner = owner
        self._balance = initial_balance
        self._transactions: List[Transaction] = []
        if initial_balance > 0:
            self._record("deposit", initial_balance, "Initial deposit")

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float, description: str = "Deposit") -> float:
        if amount <= 0:
            raise NegativeAmountError(f"Deposit amount must be positive, got {amount}")
        self._balance += amount
        self._record("deposit", amount, description)
        return self._balance

    def withdraw(self, amount: float, description: str = "Withdrawal") -> float:
        if amount <= 0:
            raise NegativeAmountError(f"Withdrawal amount must be positive, got {amount}")
        if amount > self._balance:
            raise InsufficientFundsError(amount, self._balance)
        self._balance -= amount
        self._record("withdrawal", amount, description)
        return self._balance

    def _record(self, type_: str, amount: float, description: str) -> None:
        self._transactions.append(Transaction(
            type=type_,
            amount=amount,
            description=description,
            balance_after=self._balance,
        ))

    def statement(self) -> None:
        print(f"\n{'=' * 52}")
        print(f"  Account Statement — {self.owner}")
        print(f"{'=' * 52}")
        print(f"  {'Date':<22} {'Type':<12} {'Amount':>9} {'Balance':>9}")
        print(f"  {'-' * 50}")
        for t in self._transactions:
            sign = "+" if t.type == "deposit" else "-"
            print(f"  {t.timestamp:<22} {t.type:<12} {sign}${t.amount:>7.2f}  ${t.balance_after:>8.2f}")
        print(f"  {'-' * 50}")
        print(f"  {'Current Balance:':<35} ${self.balance:>8.2f}")
        print(f"{'=' * 52}\n")


def main() -> None:
    account = BankAccount("Charles Lipshay", initial_balance=1000.00)
    account.deposit(500.00, "Phase 2 course revenue")
    account.withdraw(150.00, "Server costs")
    account.deposit(250.00, "Credential mint fees")
    account.withdraw(75.00, "ElevenLabs subscription")
    account.statement()

    # Demonstrate error handling
    try:
        account.withdraw(10000.00, "Impossible withdrawal")
    except InsufficientFundsError as e:
        print(f"✅ Caught: {e}")

    try:
        account.deposit(-50.00)
    except NegativeAmountError as e:
        print(f"✅ Caught: {e}")


if __name__ == "__main__":
    main()
```

```bash
python3 ~/developer-workspace/projects/python-foundations/bank_account.py
```

---

## Chapter 7: Proof of Work

```bash
echo "=== B-033 Verification ==="
python3 -c "
from dataclasses import dataclass

@dataclass
class Book:
    id: str
    title: str
    approved: bool = False

b = Book('B-033', 'Classes and Objects Made Simple')
print('Before:', b)
b.approved = True
print('After:', b)
print('✅ dataclass works')
"
python3 ~/developer-workspace/projects/python-foundations/bank_account.py
```

---

## Further Reading

- 📄 [`docs/B-034-testing-your-code.md`](B-034-testing-your-code.md) — Testing the BankAccount class with pytest
- 📄 [`docs/B-028-functions-that-do-one-thing-well.md`](B-028-functions-that-do-one-thing-well.md) — Functions as building blocks of classes
- 🏠 [`README.md`](../README.md) — Encyclopedia home
