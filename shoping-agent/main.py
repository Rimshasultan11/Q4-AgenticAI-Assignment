from agents import Agent, Runner, function_tool
import rich
from connection import config
import requests

# ✅ Tool 1: List All Products
@function_tool
def list_all_products() -> str:
    url = "https://hackathon-apis.vercel.app/api/products"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if not data:
            return "❌ Product list is empty."

        result = ""
        for i, p in enumerate(data, 1):
            title = p.get("title", "N/A")
            price = p.get("price", "N/A")
            category = p.get("category", "N/A")
            result += f"\n{i}. 🛍️ {title}\n   💸 {price}\n   📦 {category}\n"
        return result

    except requests.exceptions.RequestException as e:
        return f"⚠️ Error fetching product list: {str(e)}"

# ✅ Tool 2: Search Products
@function_tool
def search_product(query: str) -> str:
    url = "https://hackathon-apis.vercel.app/api/products"
    params = {"query": query}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if not data:
            return "❌ No products found for your search."

        result = ""
        for i, p in enumerate(data, 1):
            title = p.get("title", "N/A")
            price = p.get("price", "N/A")
            category = p.get("category", "N/A")

            result += f"\n{i}. 🛍️ {title}\n   💸 {price}\n   📦 {category}\n"
        return result

    except requests.exceptions.RequestException as e:
        return f"⚠️ Error while searching: {str(e)}"

# ✅ Tool 3: Order a Product
@function_tool
def order_product(product_name: str) -> str:
    # Simulated order system (you can integrate real API here)
    return f"✅ Your order for '{product_name}' has been placed successfully! 🛒📦"

# ✅ Agent Setup
agent = Agent(
    name="ShoppingAgent",
    instructions="You are a helpful any query and shopping assistant. You can list, search, and order products and any thing.",
    tools=[list_all_products, search_product, order_product],
)

# ✅ CLI Loop
if __name__ == "__main__":
    while True:
       rich.print("\n 🛍️ [bold underline magenta] Welcome to Shopping Assistant! \n")
       rich.print("1. 🔍 [bold green] Search Product")
       rich.print("2. 📋 [bold green] Show All Products")
       rich.print("3. 🛒 [bold green] Order a Product")
       rich.print("4. ❌ [bold green] Exit")
       choice = input("\nEnter your choice (1 to 4): ").strip()

       if choice == "1":
            query = input("🔍 Enter product name to search: ")
            result = Runner.run_sync(agent, input=f"search_product('{query}')", run_config=config)
            rich.print("\n 🧾 [b cyan] Search Results:")
            rich.print(result.final_output)

       elif choice == "2":
            result = Runner.run_sync(agent, input="list_all_products()", run_config=config)
            rich.print("\n 🛒 [b cyan] All Products:")
            print(result.final_output)

       elif choice == "3":
            product = input("🛒 Enter the exact product name to order: ")
            result = Runner.run_sync(agent, input=f"order_product('{product}')", run_config=config)
            rich.print(result.final_output)

       elif choice == "4":
            rich.print("👋 [bold green] Thank you for using Shopping Agent. Goodbye!")
            break

       else:
            rich.print("⚠️  [yellow] Invalid choice! Please enter 1, 2, 3, or 4.")
