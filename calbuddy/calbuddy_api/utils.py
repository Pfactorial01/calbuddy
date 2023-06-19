import requests


def fetch_calorie_data(ingredients):
    try:
        response = requests.get(
            "https://api.edamam.com/api/nutrition-data",
            params={
                "app_id": "06c2db80",
                "app_key": "d28c5ed6b9453fc29d4f365855bba30c",
                "ingr": ingredients,
                "nutrition-type": "logging",
            },
        )
        return response.json().get("calories")
    except:
        return 0
