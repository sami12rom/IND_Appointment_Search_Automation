import json
from common_utilities.api.api_call import RESTAPI
from datetime import datetime, timedelta

rest = RESTAPI()


def check_appointments(appt_type: str, locations: list):
    '''
    search for appointment availability in IND
    type: VAA for sticker on passport or DOC for Document
    location: DH for Den Haag or AM for Amsterdam
    '''
    available_appointments = {}
    for location in locations:
        result = rest.api_call(
            method='GET', url=f"https://oap.ind.nl/oap/api/desks/{location}/slots/?productKey={appt_type}&persons=1")
        try:
            available_appointments[location] = json.loads(result[5:])['data']
        except Exception as e:
            print(e)
            available_appointments[location] = result
    return available_appointments


def generate_dates(required_date, added_days):
    for add_one in range(added_days):
        yield (datetime.strptime(required_date, '%Y-%m-%d') + timedelta(days=add_one)).strftime('%Y-%m-%d')


def remove_none_values(dictionary: dict) -> dict:
    """Function that removes all values that are none, including values that are empty dicts"""
    cleaned_dict = {}
    for key, value in dictionary.items():
        for location in value:
            if isinstance(location, dict):
                cleaned_again = remove_none_values(location)
                if cleaned_again != {}:
                    cleaned_dict[key] = cleaned_again
            elif location is not None:
                cleaned_dict[key] = location

    return cleaned_dict


def find_preferred_date(preferred_dates: list, appointments_data: dict):
    requested_date = []
    for key, value in appointments_data.items():
        for appoint in value:
            appoint['location'] = key
            if appoint['date'] in preferred_dates:
                requested_date.append(appoint)
    if requested_date:
        return requested_date
    else:
        print('No available appointments, soonest available:')
        print(value[:5])


def hold_booking(available_appointments: dict, option: int):
    if available_appointments:
        location = available_appointments[option]['location']
        key = available_appointments[option]['key']
        data = json.dumps(available_appointments[option])
        result = rest.api_call(method='POST', url=f"https://oap.ind.nl/oap/api/desks/{location}/slots/{key}",
                               data=data)
        transformed_result = json.loads(result[5:])
        transformed_result['location'] = location
        return transformed_result
    else:
        transformed_result = {}
        transformed_result['status'] = 'No hold done'
        return transformed_result


def make_booking(booking_hold: dict, person_details: dict, appt_type: str):
    data = booking_hold['data']
    body = {
        "bookableSlot": {**data, "booked": 'false'},
        "appointment":
        {"productKey": f"{appt_type}", **data, "email": f"{person_details['email']}",
         "phone": f"{person_details['phone']}", "language": "en",
         "customers":
         [{"vNumber": f"{person_details['vNumber']}", "firstName": f"{person_details['firstName']}",
           "lastName": f"{person_details['lastName']}"}]}}
    body['appointment'].pop('key')
    body['appointment'].pop('parts')

    book = rest.api_call(
        method='POST', url=f"https://oap.ind.nl/oap/api/desks/{booking_hold['location']}/appointments/",
        data=json.dumps(body))
    print(body)
    return json.loads(book[5:])
