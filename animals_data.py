# animals_data.py
import datetime

# Your master list of animals
ANIMALS = {
    "ឥន្ទ្រី": {
        "name_kh": "ឥន្ទ្រី (Eagle)",
        "description": "សត្វស្លាបធំ ហើរខ្ពស់ និងមានក្រញ៉ាំមុត...",
        "image_path": "static/eagle.jpg" # Path to your image
    },
    "ផ្សោត": {
        "name_kh": "ផ្សោត (Dolphin)",
        "description": "ថនិកសត្វក្នុងទឹក ឆ្លាតវៃ និងចេះលោត...",
        "image_path": "static/dolphin.jpg"
    },
    # Add more animals...
}

# Simple daily logic: rotates through the list based on the date
def get_daily_content():
    # Get today's day of the year (1-366)
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    animal_keys = list(ANIMALS.keys())
    # Use modulo to cycle through the list
    index = (day_of_year - 1) % len(animal_keys)
    return ANIMALS[animal_keys[index]]
