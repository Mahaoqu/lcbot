import uuid
from datetime import datetime

from pynamodb.attributes import (NumberAttribute, UnicodeAttribute,
                                 UTCDateTimeAttribute)
from pynamodb.models import Model
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection


from data import Problem
from reader import all_problems, get_problems_from_file


def get_leetcode_problem(id: int) -> Problem:
    if len(all_problems) == 0:
        get_problems_from_file()
    return all_problems[id-1]


class TypeIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index
    """
    class Meta:
        # index_name is optional, but can be provided to override the default name
        index_name = 'typ-submit_time-index'
        read_capacity_units = 1
        write_capacity_units = 1
        # All attributes are projected
        projection = AllProjection()

    # This attribute is the hash key for the index
    # Note that this attribute must also exist
    # in the model
    typ = UnicodeAttribute(hash_key=True)

class RecordModel(Model):
    class Meta:
        table_name = 'lc-app'
        region = 'us-east-1'
    id = UnicodeAttribute(hash_key=True)  # Not use
    typ = UnicodeAttribute(range_key=True, default='lc-record')
    type_index = TypeIndex()
    submit_time = UTCDateTimeAttribute()
    uid = UnicodeAttribute()
    pid = NumberAttribute()


def save_check_in_record(uid: str, pid: int):
    a = RecordModel(str(uuid.uuid4()),
                    uid=uid, pid=pid,
                    submit_time=datetime.now())
    a.save()


def get_records_after(d: datetime):
    records = []
    for i in RecordModel.type_index.query('lc-record', RecordModel.submit_time > d):
        records.append((i.uid, i.pid, i.submit_time))

    return records

    