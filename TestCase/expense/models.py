from django.db import models

# Create your models here.

class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=55)
    amount = models.FloatField()
    Transaction_type = models.CharField(max_length=10 , choices=(("CREDIT" , "CREDIT"),("DEBIT" , "DEBIT")))
    deleted = models.BooleanField(default=False)
    
    
    def save(self, *args, **kwargs):
        if self.Transaction_type == "DEBIT" :
            self.amount = self.amount * -1
        return super().save(*args, **kwargs)