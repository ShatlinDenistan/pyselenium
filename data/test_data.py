import random
from collections import namedtuple

from data.db_config import SERVICES_12, TAKE2WEEKLY
from utils.db import get_data_for_query

Seller = namedtuple("Seller", "id key")
MAX_ROW = 1000
NUM_OF_RECORDS = 1

SELLER_DATA = {
    "DRAKEN": Seller(
        id=29854454,
        key="",
    ),
    "Carrol Boyes": Seller(
        id=29826602,
        key="",
    ),
    "Lunae  Store": Seller(
        id=29845619,
        key="",
    ),
    "Reader's Warehouse": Seller(
        id=9991,
        key="",
    ),
    "Lekker Local": Seller(
        id=29826806,
        key="",
    ),
    "Zia": Seller(
        id=29842557,
        key="",
    ),
    "Global Goods": Seller(
        id=29831969,
        key="",
    ),
    "Binuns Online": Seller(
        id=29824440,
        key="",
    ),
    "BROTHERS": Seller(
        id=29851632,
        key="",
    ),
    "Best Online Deals": Seller(
        id=29841488,
        key="",
    ),
    "Marketplace Inc": Seller(
        id=10944,
        key="",
    ),
}
SELECTED_SELLER = "Carrol Boyes"


def get_high_return_offer_test_data():
    """get_high_return_offer_test_data"""
    return [
        59911370,
        56132027,
    ]


def get_seller_for_test():
    return str(SELLER_DATA[SELECTED_SELLER].id)


def get_seller_auth_key():
    return f"Key {SELLER_DATA[SELECTED_SELLER].key}"


def get_facilities():
    return ["CPT2", "JHB", "JHB2", "JHB3", "CPT"]


def get_due_date_filter_values():
    return [
        "All",
        "Late",
        "Urgent",
        "Due in 1 working day",
        "Due in 2 working days",
        "Due in 3 working days",
        "Due in 4 working days",
        "Due in 5 working days",
        "Due in 6 working days",
        "Due in 7 working days",
    ]


def get_address(facility):
    query = f"SELECT street, suburb, city, province,postal_code, country_code, business_name, complex_details FROM facility_service.address  a left join facility_service.facility f on a.facility_id =f.facility_id where f.code  ='{facility}'"
    data_frame = get_data_for_query(query, SERVICES_12)
    address = "".join(f"{data_frame[column].values[0]}," for column in data_frame)
    return address[:-1]


def get_data(source_query):
    record_list = []
    built_query = ""
    for i in range(NUM_OF_RECORDS):
        random_row = random.randint(0, MAX_ROW)
        query = f"({source_query} LIMIT 1 OFFSET {random_row})"

        if i < NUM_OF_RECORDS - 1:
            query += " union "

        built_query += query

    data_frame = get_data_for_query(built_query, TAKE2WEEKLY)
    record_list = [int(row["record"]) for index, row in data_frame.iterrows()]
    return record_list
