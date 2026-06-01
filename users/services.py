def normalize_phone(phone):
    if phone.startswith('8'):
        return '+7' + phone[1:]

    return phone
