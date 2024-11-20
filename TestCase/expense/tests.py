from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from expense.models import Transaction
from expense.serializers import expenseSerializer

class ExpenseViewSetTest(TestCase):

    def setUp(self):
        """
        This method is called before each test.
        It creates a sample transaction to be used across the tests.
        """
        self.client = APIClient()
        self.url = '/expenses/'  
        
        self.transaction_data = {
            'title': 'Test Transaction',
            'Transaction_type': 'CREDIT',
            'amount': 100.00
        }

        self.transaction = Transaction.objects.create(**self.transaction_data)
        
        
        
        
    def test_create_expense(self):
        """
        Test case for creating a new expense entry.
        """
        response = self.client.post(self.url, self.transaction_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['data']['title'], self.transaction_data['title'])
        print("\nCreate Successfully.")
        print(self.transaction_data)
        

    def test_retrieve_expense(self):
        """
        Test case for retrieving an existing expense entry by ID.
        """
        response = self.client.get(f'{self.url}{self.transaction.id}/')  
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['data']['title'], self.transaction.title)
        print("\n\nData : " , self.transaction_data)
        
        
        

    def test_update_expense(self):
        """
        Test case for updating an existing expense entry.
        """
        updated_data = {'id': 1 , 'amount': 150.00}  
        
        response = self.client.patch(f'{self.url}{self.transaction.id}/', updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['data'], 'Data Successfully Updated!')
        
        self.transaction.refresh_from_db()  
        updated_data = self.assertEqual(self.transaction.amount, 150.00)
        
        print("\n\n Data Updated Successfully." )
        print({
        'id': self.transaction.id,
        'title': self.transaction.title,
        'transaction_type': self.transaction.Transaction_type,
        'amount': self.transaction.amount
        })
       
        
        
        

    def test_delete_expense(self):
        """
        Test case for deleting an expense entry (soft delete by marking 'deleted' = 1).
        """
        response = self.client.delete(f'{self.url}{self.transaction.id}/') 
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['data'], 'Data Deleted.')
        
        self.transaction.refresh_from_db()  
        self.assertEqual(self.transaction.deleted, 1)
        print("\n\nData Deleted Successfully.")
        print({
        'id': self.transaction.id,
        'title': self.transaction.title,
        'transaction_type': self.transaction.Transaction_type,
        'amount': self.transaction.amount
        })
        
        

    def test_list_expenses(self):
        response = self.client.get(reverse('expense-list'))
    
        print(f"\n\nResponse status: {response.status_code}")
        print(f"Response data: {response.data}")
    
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('success', response.data['results'])  
        self.assertEqual(response.data['results']['success'], True) 
