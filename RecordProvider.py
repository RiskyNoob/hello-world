from faker import Faker
from faker.providers import BaseProvider
import datetime
import string

from random import choice

fake = Faker()

statuses = ["New", "Status1", "Status2", "Status3",  "Closed"]
class Record:
    created_date = None
    record_id = None
    status = None
    closed_date = None

    def __init__(self):
        self.created_date = fake.date_between(start_date="-1y", end_date="-30d")
        self.record_id =  'C' + ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(9))
        self.status = choice(statuses)
        self.closed_date = None
        if self.status == "Closed":
            self.closed_date = fake.date_between(start_date=self.created_date, end_date="-10d")

    def toJSON(self):
        return {
            "created_date" : str(self.created_date),
            "record_id" : self.record_id,
            "status" : self.status,
            "closed_date" : str(self.closed_date)
        }




class RecordProvider(BaseProvider):
    def fake_record(self):
        return Record()

fake.add_provider(RecordProvider)

fake.fake_record().toJSON()