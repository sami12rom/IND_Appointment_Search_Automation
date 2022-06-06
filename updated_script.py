from common_utilities.utilities.utilities import (check_appointments, generate_dates,
                                                  find_preferred_date, hold_booking,
                                                  make_booking)
import time

locations = ['DH', 'AM']
appt_type = 'VAA'
person_details = {'firstName': 'Oksana', 'lastName': 'Shevchenko',
                  'vNumber': '2913085646', 'email': 'ksyu.shevchenko@gmail.com', 'phone': '0620215000'}

preferred_dates = [x for x in generate_dates("2022-06-07", 4)]
booking = {}

while not booking:

    appointments_data = check_appointments(appt_type=appt_type, locations=locations)
    available_appointments = find_preferred_date(preferred_dates, appointments_data)
    booking_hold = hold_booking(available_appointments, 0)

    if booking_hold['status'] == "OK":
        booking = make_booking(booking_hold, person_details, appt_type)
    else:
        print('retry holding the booking')

    time.sleep(360)
