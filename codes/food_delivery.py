# Smart Food Delivery Order Tracking Application
FILE_NAME = "orders.txt"
# Each food order:
# [Order ID, Customer, Food, Quantity, Unit Price, Status]

def create_sample_orders():
    """
    Creating sample orders in a list of lists.
    """
    orders = [
        [1001, "Amit", "Veg Burger", 2, 120.0, "Delivered"],
        [1002, "Priya", "Pizza", 1, 350.0, "Preparing"],
        [1003, "Rahul", "Biryani", 2, 220.0, "Placed"],
        [1004, "Neha", "Pasta", 1, 180.0, "Out for Delivery"],
        [1005, "Arjun", "Sandwich", 3, 90.0, "Delivered"],
    ]
    return orders


def find_order_index(orders, order_id):
    """
    Find the index of an order in the list based on the order ID.
    """
    for i in range(len(orders)):
        if orders[i][0] == order_id:
            return i
    return -1


def next_order_id(orders):
    """
    Returns the next available order ID.
    """
    if len(orders) == 0:
        return 1001
    highest_id = orders[0][0]
    for order in orders:
        if order[0] > highest_id:
            highest_id = order[0]
    return highest_id + 1


def calculate_order_total(order):
    """
    Calculates the total price of an order based on quantity and unit price.
    """
    return order[3] * order[4]


# Place and View Orders
def place_order(orders, customer, food, quantity, price):
    """
    Places a new order in the orders list after validating the input.
    """
    customer = customer.strip()
    food = food.strip()
    if customer == "" or food == "":
        print("Customer and food item are required.")
        return False
    if quantity <= 0 or price < 0:
        print("Quantity must be positive and price cannot be negative.")
        return False
    order = [next_order_id(orders), customer, food, quantity, price, "Placed"]
    orders.append(order)
    print("Order placed successfully!")
    print("Your order ID is:", order[0])
    print("Order total: Rs.", calculate_order_total(order))
    return True


def display_orders(orders):
    """
    Displays all orders in a formatted table.
    """
    if len(orders) == 0:
        print("No orders available.")
        return
    print("-" * 105)
    print(
        f"{'ID':<8}{'CUSTOMER':<16}{'FOOD':<22}"
        f"{'QTY':<7}{'PRICE':<12}{'TOTAL':<12}{'STATUS':<22}"
    )
    print("-" * 105)
    for order in orders:
        total = calculate_order_total(order)
        print(
            f"{order[0]:<8}"
            f"{order[1][:15]:<16}"
            f"{order[2][:21]:<22}"
            f"{order[3]:<7}"
            f"{order[4]:<12.2f}"
            f"{total:<12.2f}"
            f"{order[5]:<22}"
        )
    print("-" * 105)


def view_single_order(orders, order_id):
    """
    Checks if an order exists and displays its details if found.
    """
    index = find_order_index(orders, order_id)
    if index == -1:
        print("Order not found.")
    else:
        order = orders[index]
        print("Order ID :", order[0])
        print("Customer :", order[1])
        print("Food     :", order[2])
        print("Quantity :", order[3])
        print("Price    : Rs.", order[4])
        print("Total    : Rs.", calculate_order_total(order))
        print("Status   :", order[5])


# Step 3 - Update status and cancel orders
def update_order_status(orders, order_id):
    """
    Updates the status of an existing order based on user input.
    Enforces forward-only delivery progression.
    """
    index = find_order_index(orders, order_id)
    if index == -1:
        print("Order not found.")
        return False
    order = orders[index]
    current_status = order[5]
    print("Current status:", current_status)
    print("1. Preparing")
    print("2. Out for Delivery")
    print("3. Delivered")
    choice = input("Choose new status: ").strip()
    if choice == "1":
        new_status = "Preparing"
    elif choice == "2":
        new_status = "Out for Delivery"
    elif choice == "3":
        new_status = "Delivered"
    else:
        print("Invalid choice.")
        return False

    # Enforce forward-only delivery progression.
    if current_status == "Placed" and new_status == "Preparing":
        order[5] = new_status
    elif current_status == "Preparing" and new_status == "Out for Delivery":
        order[5] = new_status
    elif current_status == "Out for Delivery" and new_status == "Delivered":
        order[5] = new_status
    elif current_status == new_status:
        print("Order already has this status.")
        return False
    else:
        print("Invalid status transition.")
        return False
    print("Order status updated to:", order[5])
    return True


def cancel_order(orders, order_id):
    """
    Cancels an existing order if it is in a cancellable state.
    """
    index = find_order_index(orders, order_id)
    if index == -1:
        print("Order not found.")
        return False
    order = orders[index]
    if order[5] == "Placed" or order[5] == "Preparing":
        order[5] = "Cancelled"
        print("Order cancelled successfully.")
        return True
    print("Only Placed or Preparing orders can be cancelled.")
    return False


# Search and filter
def search_by_customer(orders, customer):
    """Searches for orders by customer name (case-insensitive)."""
    results = []
    for order in orders:
        if customer.lower() in order[1].lower():
            results.append(order)
    display_orders(results)


def search_by_food(orders, food):
    """Searches for orders by food item name (case-insensitive)."""
    results = []
    for order in orders:
        if food.lower() in order[2].lower():
            results.append(order)
    display_orders(results)


def filter_by_status(orders, status):
    """Filters orders by their status."""
    results = []
    for order in orders:
        if order[5].lower() == status.lower():
            results.append(order)
    display_orders(results)


def filter_by_minimum_total(orders, minimum_total):
    """Filters orders by a minimum total value."""
    results = []
    for order in orders:
        if calculate_order_total(order) >= minimum_total:
            results.append(order)
    display_orders(results)


# Dashboard and reports
def show_dashboard(orders):
    """Displays a summary of orders, including counts and revenue."""
    total_orders = len(orders)
    delivered = 0
    pending = 0
    cancelled = 0
    delivered_revenue = 0.0
    active_order_value = 0.0

    for order in orders:
        status = order[5]
        total = calculate_order_total(order)
        if status == "Delivered":
            delivered += 1
            delivered_revenue += total
        elif status == "Cancelled":
            cancelled += 1
        else:
            pending += 1
            active_order_value += total

    print("\n========== FOOD DELIVERY DASHBOARD ==========")
    print("Total orders          :", total_orders)
    print("Pending / active      :", pending)
    print("Delivered orders      :", delivered)
    print("Cancelled orders      :", cancelled)
    print("Delivered revenue     : Rs.", round(delivered_revenue, 2))
    print("Active order value    : Rs.", round(active_order_value, 2))
    print("=============================================\n")


def show_high_value_orders(orders, minimum_total):
    """Displays orders with a total value greater than or equal to the specified minimum total."""
    results = []
    for order in orders:
        if calculate_order_total(order) >= minimum_total:
            results.append(order)
    print("Orders at or above Rs.", minimum_total)
    display_orders(results)


def show_most_expensive_order(orders):
    """Cancelled orders are ignored: they are not real sales."""
    best = None
    for order in orders:
        if order[5] == "Cancelled":
            continue
        if best is None or calculate_order_total(order) > calculate_order_total(best):
            best = order
    if best is None:
        print("No active or delivered orders available.")
        return
    print("Most expensive order:")
    display_orders([best])


def show_sales_report(orders):
    total_delivered = 0.0
    total_cancelled = 0.0
    total_active = 0.0
    for order in orders:
        amount = calculate_order_total(order)
        if order[5] == "Delivered":
            total_delivered += amount
        elif order[5] == "Cancelled":
            total_cancelled += amount
        else:
            total_active += amount

    print("\n========== SALES REPORT ==========")
    print("Delivered revenue : Rs.", round(total_delivered, 2))
    print("Cancelled value   : Rs.", round(total_cancelled, 2))
    print("Active order value: Rs.", round(total_active, 2))
    print("==================================")


# ---------------------------------------------------------------
# Step 6 - Demonstrate all 11 list methods
# ---------------------------------------------------------------
def demonstrate_list_methods():
    foods = ["Pizza", "Burger", "Pasta"]
    print("\nOriginal list:", foods)

    foods.append("Biryani")  # 1. append()
    print("1. append:", foods)

    foods.extend(["Sandwich", "Noodles"])  # 2. extend()
    print("2. extend:", foods)

    foods.insert(1, "Dosa")  # 3. insert()
    print("3. insert:", foods)

    foods.remove("Pasta")  # 4. remove()
    print("4. remove:", foods)

    removed = foods.pop()  # 5. pop()
    print("5. pop removed:", removed)
    print("   Current list:", foods)

    print("6. index of Burger:", foods.index("Burger"))  # 6. index()

    foods.append("Pizza")
    print("7. count of Pizza:", foods.count("Pizza"))  # 7. count()

    foods.sort()  # 8. sort()
    print("8. sort:", foods)

    foods.reverse()  # 9. reverse()
    print("9. reverse:", foods)

    copied_foods = foods.copy()  # 10. copy()
    print("10. copy:", copied_foods)

    copied_foods.clear()  # 11. clear()
    print("11. clear:", copied_foods)


# Plain-text file storage
def save_orders(orders):
    """
    Saves the current list of orders to a text file, replacing any existing content.
    """
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        for order in orders:
            customer = order[1].replace("|", "/").replace("\n", " ")
            food = order[2].replace("|", "/").replace("\n", " ")
            line = (
                f"{order[0]}|{customer}|{food}|{order[3]}|" f"{order[4]}|{order[5]}\n"
            )
            file.write(line)
    print("Orders saved successfully.")


def load_orders():
    orders = []
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            for line in file:
                fields = line.strip().split("|")
                if len(fields) != 6:
                    continue
                try:
                    order = [
                        int(fields[0]),
                        fields[1],
                        fields[2],
                        int(fields[3]),
                        float(fields[4]),
                        fields[5],
                    ]
                    orders.append(order)
                except ValueError:
                    print("Skipping invalid order record.")
    except FileNotFoundError:
        orders = create_sample_orders()
        save_orders(orders)
    return orders


# Interactive console menu
def read_integer(message):
    try:
        return int(input(message))
    except ValueError:
        print("Please enter a valid integer.")
        return None


def read_price(message):
    """
    Checks if the input is a valid float and not negative. Returns None if invalid.
    """
    try:
        value = float(input(message))
        if value < 0:
            print("Price cannot be negative.")
            return None
        return value
    except ValueError:
        print("Please enter a valid amount.")
        return None


def search_menu(orders):
    """
    Menu for searching and filtering orders based on different criteria.
    """
    print("\n--- SEARCH ORDERS ---")
    print("1. Search by customer")
    print("2. Search by food")
    print("3. Search by order ID")
    print("4. Filter by status")
    print("5. Filter by minimum order value")
    choice = input("Enter choice: ").strip()

    if choice == "1":
        search_by_customer(orders, input("Customer name: "))
    elif choice == "2":
        search_by_food(orders, input("Food name: "))
    elif choice == "3":
        order_id = read_integer("Order ID: ")
        if order_id is not None:
            view_single_order(orders, order_id)
    elif choice == "4":
        status = input("Status: ").strip()
        filter_by_status(orders, status)
    elif choice == "5":
        minimum = read_price("Minimum order total: ")
        if minimum is not None:
            filter_by_minimum_total(orders, minimum)
    else:
        print("Invalid choice.")


def show_menu():
    print("""
=========================================
      FOOD DELIVERY ORDER TRACKING
=========================================
1.  Dashboard
2.  View all orders
3.  Place a new order
4.  View one order
5.  Update order status
6.  Cancel an order
7.  Search and filter orders
8.  Sort orders by ID
9.  Sort orders by total value
10. Show sales report
11. Demonstrate list methods
12. Save orders
13. Show most expensive order
0.  Save and exit
=========================================
""")


def main():
    orders = load_orders()

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            show_dashboard(orders)
        elif choice == "2":
            display_orders(orders)
        elif choice == "3":
            customer = input("Customer name: ")
            food = input("Food item: ")
            quantity = read_integer("Quantity: ")
            price = read_price("Price per item: ")
            if quantity is not None and price is not None:
                if place_order(orders, customer, food, quantity, price):
                    save_orders(orders)
        elif choice == "4":
            order_id = read_integer("Order ID: ")
            if order_id is not None:
                view_single_order(orders, order_id)
        elif choice == "5":
            order_id = read_integer("Order ID: ")
            if order_id is not None:
                if update_order_status(orders, order_id):
                    save_orders(orders)
        elif choice == "6":
            order_id = read_integer("Order ID: ")
            if order_id is not None:
                if cancel_order(orders, order_id):
                    save_orders(orders)
        elif choice == "7":
            search_menu(orders)
        elif choice == "8":
            orders.sort(key=lambda order: order[0])
            display_orders(orders)
        elif choice == "9":
            orders.sort(key=lambda order: calculate_order_total(order), reverse=True)
            display_orders(orders)
        elif choice == "10":
            show_sales_report(orders)
        elif choice == "11":
            demonstrate_list_methods()
        elif choice == "12":
            save_orders(orders)
        elif choice == "13":
            show_most_expensive_order(orders)
        elif choice == "0":
            save_orders(orders)
            print("Thank you for using the application.")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
