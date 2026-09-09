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
    },
    "swallow": {
        "name_kh": "ត្រចៀកកោង (Swallow)",
        "description": "សត្វស្លាបតូច ហើរលឿន ចេះធ្វើសំបុកនៅលើផ្ទះ",
        "image_path": "static/swallow.jpg"
    },
    "whale": {
        "name_kh": "ត្រីបាឡែន (Whale)",
        "description": "ថនិកសត្វក្នុងទឹកដ៏ធំ អាចហែលបានចម្ងាយឆ្ងាយ",
        "image_path": "static/whale.jpg"
    },
    "seagull": {
        "name_kh": "ត្រីសមុទ្រ (Seagull)",
        "description": "សត្វស្លាបសមុទ្រ ហើរបានឆ្ងាយ និងអាចហែលទឹកបាន",
        "image_path": "static/seagull.jpg"
    },
    "penguin": {
        "name_kh": "ភេនឃ្វីន (Penguin)",
        "description": "សត្វស្លាបមិនអាចហើរបាន ប៉ុន្តែហែលទឹកបានយ៉ាងពូកែ",
        "image_path": "static/penguin.jpg"
    }
}

def get_daily_content():
    """Get today's animal based on day of year."""
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    animal_keys = list(ANIMALS.keys())
    index = (day_of_year - 1) % len(animal_keys)
    return ANIMALS[animal_keys[index]]
