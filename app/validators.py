def get_valid_status(prompt):
    while True:
        status = input(prompt).strip()
        if status in VALID_STATUSES:
            return status
        print(f"Invalid status. Choose from {VALID_STATUSES}.")

