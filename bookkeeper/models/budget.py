from dataclasses import dataclass
from datetime import datetime, timedelta

from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.models.expense import Expense


@dataclass
class Budget:
    """
    Класс бюджета. Содержит в себе:
    # time - период, за который рассчитываются траты
    # sum - потраченная сумма
    # budget - предел трат за период
    # pk - ключ
    """

    time: str = 'Empty'
    sum: float = 0
    budget: float = 0
    pk: int = 0

    def __init__(self,
                 pk: int = 0,
                 time: str = 'Empty',
                 spent_sum: float = 0,
                 budget: float = 0):
        if time not in ['День', 'Неделя', 'Месяц', 'Empty']:
            raise ValueError('Неизвестный тип периода!')

        self.time = time
        self.sum = spent_sum
        self.budget = budget
    def update_spented_sum(self, expenses_repo: AbstractRepository[Expense]) -> None:
        """
        # Обновление бюджета из-за изменения трат
        Parameters
        ----------
        expenses_repo
        Returns
        -------
        """
        date_short = datetime.now().isoformat()[:10]
        if self.time == 'День':
            expenses_in_time = expenses_repo.get_all(
                where={'expense_date': f'LIKE \'{date_short}%\''})
        elif self.time == 'Неделя':
            weekday_now = datetime.now().weekday()
            day_now = datetime.fromisoformat(date_short)
            first_week_day = day_now - timedelta(days=weekday_now)
            expenses_in_time = []
            for j in range(7):
                weekday = first_week_day + timedelta(days=j)
                day_expenses = expenses_repo.get_all(
                    where={'expense_date': f'LIKE \'{weekday.isoformat()[:10]}%\''})
                if day_expenses is not None:
                    expenses_in_time = expenses_in_time + day_expenses
        elif self.time == 'Месяц':
            expenses_in_time = expenses_repo.get_all(
                where={'expense_date': f'LIKE \'{date_short[:7]}%\''})
        if (expenses_in_time == []) | (expenses_in_time is None):
            self.sum = 0
        else:
            self.sum = sum([float(expense.amount) for expense in expenses_in_time])