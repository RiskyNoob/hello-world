from faker import Faker
from faker.providers import BaseProvider
import datetime
import string

from random import choice
fake = Faker()

customer_type = [True, False]

class Person:
    name = None
    iban = None
    is_customer = None
    cus_id = None
    def __init__(self):
        self.name = fake.name()
        self.is_customer = choice(customer_type)
        self.iban = 'IB' + ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(17))
        if self.is_customer == True:
            self.cus_id = 'DMY' + ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(9))

    def toJSON(self):
        return {
            "name" : self.name,
            "is_customer" : str(self.is_customer),
            "iban" : self.iban ,  
            "cus_id" : str(self.cus_id)
        }



class PersonProvider(BaseProvider):
    def fake_person(self):
        return Person()

fake.add_provider(PersonProvider)

fake.fake_person().toJSON()