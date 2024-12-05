from django.db import models

class CurrentBalance(models.Model):
    current_balance = models.FloatField(default=0)

    def __str__(self)->str:
        return f"The current balance is {self.current_balance}"

class TrackingHistory(models.Model):
    current_balance = models.ForeignKey(CurrentBalance, on_delete=models.CASCADE)
    amount = models.FloatField()
    expense_type = models.CharField(choices=(('CREDIT','CREDIT'), ('DEBIT', 'DEBIT')), max_length=100)
    description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"The amount is {self.amount} for {self.description} expense type is {self.expense_type}"



