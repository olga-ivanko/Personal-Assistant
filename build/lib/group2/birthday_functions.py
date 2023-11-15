from datetime import datetime
from . import service_addressbook 

def func_birthdays_within_days():
    
    
    try:
        days = int(input("Enter number of days: "))
    except ValueError:
        return "Invalid number of days. Please enter an integer"

    current_date = datetime.now().date()

    matching_birthdays = []
    for record in service_addressbook.book.values():
        if record.birthday.value != "unknown":
            days_to_birthday = record.days_to_birthday()
            if 0 <= days_to_birthday <= days:
                matching_birthdays.append(record)

    if not matching_birthdays:
        return f"No contact with birthdays for the next {days} days."

    result = ""
    for record in matching_birthdays:
        result += f"{record}\n"
    return result

