from faker import Faker
import random
from typing import List, Dict, Any
import datetime

# Initialize Faker with multiple locales for more diversity
fake = Faker(['en_US', 'en_GB', 'es_ES', 'fr_FR', 'de_DE'])

# Field generator functions
def generate_name():
    return fake.name()

def generate_email():
    return fake.email()

def generate_phone():
    return fake.phone_number()

def generate_address():
    return fake.street_address()

def generate_city():
    return fake.city()

def generate_state():
    return fake.state()

def generate_zip():
    return fake.postcode()

def generate_country():
    return fake.country()

def generate_company():
    return fake.company()

def generate_job_title():
    return fake.job()

def generate_age():
    return random.randint(18, 90)

def generate_birthdate():
    return fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat()

def generate_salary():
    # Generate a salary between $30,000 and $200,000
    return round(random.uniform(30000, 200000), 2)

def generate_username():
    return fake.user_name()

def generate_password():
    return fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)

def generate_credit_card():
    return fake.credit_card_number()

def generate_timestamp():
    # Generate a timestamp within the last year
    return fake.date_time_between(start_date='-1y', end_date='now').isoformat()

def generate_device_id():
    return fake.uuid4()

def generate_reading():
    # Simulate a sensor reading
    return round(random.uniform(0, 100), 2)

def generate_location():
    return f"{fake.latitude()},{fake.longitude()}"

def generate_status():
    return random.choice(['active', 'inactive', 'pending', 'error', 'success'])

# Field generator mapping
FIELD_GENERATORS = {
    'name': generate_name,
    'email': generate_email,
    'phone': generate_phone,
    'address': generate_address,
    'city': generate_city,
    'state': generate_state,
    'zip': generate_zip,
    'country': generate_country,
    'company': generate_company,
    'job_title': generate_job_title,
    'age': generate_age,
    'birthdate': generate_birthdate,
    'salary': generate_salary,
    'username': generate_username,
    'password': generate_password,
    'credit_card': generate_credit_card,
    'timestamp': generate_timestamp,
    'device_id': generate_device_id,
    'reading': generate_reading,
    'location': generate_location,
    'status': generate_status,
}

def generate_fake_data(fields: List[str], row_count: int, biased: bool = False) -> List[Dict[str, Any]]:
    """
    Generate realistic synthetic data using Faker.

    Args:
        fields: List of field names to generate
        row_count: Number of rows to generate
        biased: Whether to generate biased data (to simulate edge cases)

    Returns:
        List of dictionaries containing the generated data
    """
    result = []

    # Check if all requested fields are supported
    unsupported_fields = [field for field in fields if field not in FIELD_GENERATORS]
    if unsupported_fields:
        raise ValueError(f"Unsupported fields: {', '.join(unsupported_fields)}")

    # Create seed values for biased data generation
    biased_values = {}
    if biased:
        # For biased data, we'll make some values more common
        biased_threshold = 0.3  # 30% of data will be biased

        # Create biased values for each field
        for field in fields:
            if field == 'status':
                # Make 'active' status much more common
                biased_values[field] = 'active'
            elif field == 'country':
                # Make 'United States' more common
                biased_values[field] = 'United States'
            elif field == 'age':
                # Bias towards younger ages
                biased_values[field] = random.randint(18, 25)
            elif field == 'salary':
                # Bias towards lower salaries
                biased_values[field] = round(random.uniform(30000, 50000), 2)

    # Generate the data
    for _ in range(row_count):
        row = {}

        for field in fields:
            # Determine if this row should use biased values for this field
            use_biased = biased and field in biased_values and random.random() < biased_threshold

            if use_biased:
                row[field] = biased_values[field]
            else:
                # Use the appropriate generator function
                generator_func = FIELD_GENERATORS[field]
                row[field] = generator_func()

        result.append(row)

    return result