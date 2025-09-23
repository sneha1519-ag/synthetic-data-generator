import random
import string
import uuid
from typing import List, Dict, Any
import datetime

def generate_random_string(length=10):
    """Generate a random string of fixed length."""
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def generate_random_email():
    """Generate a random email address."""
    username = generate_random_string(random.randint(5, 10))
    domain = generate_random_string(random.randint(5, 8))
    tld = random.choice(['com', 'org', 'net', 'io', 'co'])
    return f"{username}@{domain}.{tld}"

def generate_random_phone():
    """Generate a random phone number."""
    return ''.join(random.choice(string.digits) for _ in range(10))

def generate_random_number(min_val=0, max_val=100):
    """Generate a random number within the specified range."""
    return random.randint(min_val, max_val)

def generate_random_decimal(min_val=0, max_val=100, precision=2):
    """Generate a random decimal number within the specified range."""
    value = random.uniform(min_val, max_val)
    return round(value, precision)

def generate_random_boolean():
    """Generate a random boolean value."""
    return random.choice([True, False])

def generate_random_date():
    """Generate a random date within the last 10 years."""
    days = random.randint(0, 365 * 10)
    date = datetime.datetime.now() - datetime.timedelta(days=days)
    return date.strftime('%Y-%m-%d')

def generate_random_timestamp():
    """Generate a random timestamp within the last year."""
    seconds = random.randint(0, 365 * 24 * 60 * 60)
    timestamp = datetime.datetime.now() - datetime.timedelta(seconds=seconds)
    return timestamp.isoformat()

def generate_random_uuid():
    """Generate a random UUID."""
    return str(uuid.uuid4())

def generate_random_status():
    """Generate a random status."""
    return random.choice(['active', 'inactive', 'pending', 'error', 'success'])

def generate_random_coordinates():
    """Generate random geographic coordinates."""
    lat = random.uniform(-90, 90)
    lng = random.uniform(-180, 180)
    return f"{lat:.6f},{lng:.6f}"

# Field generator mapping
RANDOM_GENERATORS = {
    'name': lambda: generate_random_string(random.randint(5, 15)),
    'email': generate_random_email,
    'phone': generate_random_phone,
    'address': lambda: generate_random_string(random.randint(10, 30)),
    'city': lambda: generate_random_string(random.randint(5, 15)),
    'state': lambda: generate_random_string(2).upper(),
    'zip': lambda: ''.join(random.choice(string.digits) for _ in range(5)),
    'country': lambda: generate_random_string(random.randint(5, 10)),
    'company': lambda: generate_random_string(random.randint(5, 20)),
    'job_title': lambda: generate_random_string(random.randint(5, 15)),
    'age': lambda: generate_random_number(18, 90),
    'birthdate': generate_random_date,
    'salary': lambda: generate_random_decimal(30000, 200000, 2),
    'username': lambda: generate_random_string(random.randint(5, 10)),
    'password': lambda: generate_random_string(random.randint(8, 16)),
    'credit_card': lambda: ''.join(random.choice(string.digits) for _ in range(16)),
    'timestamp': generate_random_timestamp,
    'device_id': generate_random_uuid,
    'reading': lambda: generate_random_decimal(0, 100, 2),
    'location': generate_random_coordinates,
    'status': generate_random_status,
}

def generate_random_data(fields: List[str], row_count: int) -> List[Dict[str, Any]]:
    """
    Generate completely randomized synthetic data.

    Args:
        fields: List of field names to generate
        row_count: Number of rows to generate

    Returns:
        List of dictionaries containing the generated data
    """
    result = []

    # Check if all requested fields are supported
    unsupported_fields = [field for field in fields if field not in RANDOM_GENERATORS]
    if unsupported_fields:
        raise ValueError(f"Unsupported fields: {', '.join(unsupported_fields)}")

    # Generate the data
    for _ in range(row_count):
        row = {}

        for field in fields:
            # Use the appropriate generator function
            generator_func = RANDOM_GENERATORS[field]
            row[field] = generator_func()

        result.append(row)

    return result