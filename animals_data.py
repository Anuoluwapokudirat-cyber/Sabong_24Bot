import datetime

# Your master list of animals
ANIMALS = {
    "eagle": {
        "name_kh": "ឥន្ទ្រី (Eagle)",
        "description": "សត្វស្លាបធំ ហើរខ្ពស់ មានក្រញ៉ាំមុត និងភ្នែកមុតល្អ",
        "image_path": "static/eagle.jpg"
    },
    "dolphin": {
        "name_kh": "ផ្សោត (Dolphin)",
        "description": "ថនិកសត្វក្នុងទឹក ឆ្លាតវៃ ចេះលោត និងមានសមត្ថភាពទំនាក់ទំនងល្អ",
        "image_path": "static/dolphin.jpg"
    }
}

def get_daily_content():
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    animal_keys = list(ANIMALS.keys())
    index = (day_of_year - 1) % len(animal_keys)
    return ANIMALS[animal_keys[index]]
