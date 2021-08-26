import uuid
from datetime import datetime

from pynamodb.attributes import (NumberAttribute, UnicodeAttribute,
                                 UTCDateTimeAttribute)
from pynamodb.models import Model

from data import Problem
from reader import all_problems, get_problems_from_file


def get_leetcode_problem(id: int) -> Problem:
    if len(all_problems) == 0:
        get_problems_from_file()
    return all_problems[id-1]


class RecordModel(Model):
    class Meta:
        table_name = 'lc-app'
        region = 'us-east-1'
    id = UnicodeAttribute(hash_key=True)  # Not use
    typ = UnicodeAttribute(range_key=True, default='lc-record')
    submit_time = UTCDateTimeAttribute()
    uid = UnicodeAttribute()
    pid = NumberAttribute()


def save_check_in_record(uid: str, pid: int):
    a = RecordModel(str(uuid.uuid4()),
                    uid=uid, pid=pid,
                    submit_time=datetime.now())
    a.save()
