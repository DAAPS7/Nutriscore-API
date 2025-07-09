from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/{foodname}")
def read_item(foodname: str):
    url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={foodname}&search_simple=1&action=process&json=1"
    response = requests.get(url)
    
    if response.status_code != 200:
        return {"error": "Failed to fetch data"}
    
    data = response.json()
    products = data.get("products", [])

    for product in products:
        if "product_name" in product and foodname.lower() in product["product_name"].lower():
            return {
                "food_name": product.get("product_name"),
                "nutriscore": product.get("nutriscore_grade", "unknown").upper()
            }

    return {"error": "Item not found"}
