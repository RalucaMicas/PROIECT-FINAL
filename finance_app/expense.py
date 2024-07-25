from dataclasses import dataclass

import typing as t

@dataclass
class Expense:
    name: str
    category: str
    amount: float
    val_optionala: t.Optional[int] = None
    obs_optionala: str = 'default'
    
    def __repr__(self) -> str:
        return f'<Cheltuiala: {self.name}, {self.category}, {self.amount:.2f} RON>'