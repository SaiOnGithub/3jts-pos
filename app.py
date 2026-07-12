import streamlit as st
import datetime

# Set layout to wide for better desktop and mobile scaling
st.set_page_config(page_title="3JT's Food Hub POS", layout="wide")

# Initialize our shopping cart using Streamlit's session memory
if "cart" not in st.session_state:
    st.session_state.cart = {}

# Menu Setup (Change prices here!)
MENU = {
    "Fried Chicken by Part": {
        "Whole Chicken": 220.00,
        "Half Chicken": 110.00,
        "Thigh": 35.00,
        "Wing": 25.00,
        "Neck": 10.00,
        "Breast": 55.00,
        "Drumstick": 25.00,
        "Half Breast": 25.00,
        "Backbone": 25.00,
    },
    "Rice Meal": {
        "Student Meal (1pc + 1pc Rice)": 50.00,
        "Meal 1 (2pc Reg + 1 Rice + Unli Sauce)": 79.00,
        "Meal 2 (2pc + Unli Rice + Unli Sauce)": 99.00
    },
    "Snacks": {
        "French Fries with Cheese Sauce": 99.00,
        "Nachos with Cheese Sauce": 99.00,
    },
    "Drinks": {
        "RC Soda": 15.00,
        "Coke Soda": 20.00,
        "Sprite Soda": 20.00
    }
}

st.title("3JT's Food Hub - POS System")
st.write("---")

# Layout: Split screen into Menu Area (Left) and Checkout Basket (Right)
col_menu, col_cart = st.columns([2, 1.3])

with col_menu:
    st.subheader("Menu Categories")

    # Generate clean, touch-friendly buttons for each item
    for category, items in MENU.items():
        with st.expander(category, expanded=True):
            # Create a clean grid layout for mobile/desktop tapping
            sub_cols = st.columns(3)
            for i, (item_name, price) in enumerate(items.items()):
                target_col = sub_cols[i % 3]  
                if target_col.button(f"{item_name}\n\n₱{price:.2f}", key=f"btn_{item_name}"):
                    # Logic to add to cart
                    if item_name in st.session_state.cart:
                        st.session_state.cart[item_name]['qty'] += 1
                    else:
                        st.session_state.cart[item_name] = {'price': price, 'qty': 1}

# 👉 FIXED: Moved 'with col_cart' completely outside of the menu loop!
with col_cart:
    st.subheader("Current Basket")

    if not st.session_state.cart:
        st.info("Basket is empty. Tap menu items to add them.")
        total_due = 0.0
    else:
        total_due = 0.0
        # Display items nicely inside the cart
        for item_name, info in list(st.session_state.cart.items()):
            item_total = info['price'] * info['qty']
            total_due += item_total

            c1, c2, c3 = st.columns([2, 1, 1])
            c1.write(f"**{item_name}**")
            c2.write(f"x{info['qty']} (₱{info['price']:.0f})")

            # Simple button to remove single items if clicked by mistake
            if c3.button("X", key=f"del_{item_name}"):
                del st.session_state.cart[item_name]   
                st.rerun()

        st.write("---")
        st.metric(label="TOTAL AMOUNT DUE", value=f"₱{total_due:.2f}")

        # Cash handling
        cash_received = st.number_input("Cash Received (₱)", min_value=0.0, step=5.0, value=0.0)

        # Initialize change so it always exists safely
        change = 0.0

        if cash_received > 0:
            if cash_received >= total_due:
                change = cash_received - total_due
                st.success(f"**Change to Return:** ₱{change:,.2f}")

                # Pay / Print trigger
                if st.button("Complete Order & Print Receipt", type="primary"):
                    st.toast("Processing order...")

                    # Generate text receipt pop-up style layout
                    receipt_text = f"""
============================================
                3JT's Food Hub
{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
============================================
"""
                    for name, info in st.session_state.cart.items():
                        receipt_text += f"\n {name[:20]:<20} x{info['qty']:<2} ₱{info['price']*info['qty']:>7.2f}"

                    receipt_text += f"""
---------------------------------------------
 Total Bill:                ₱{total_due:>7.2f}
 Cash Paid:                 ₱{cash_received:>7.2f}
 Change Due                 ₱{change:>7.2f}
============================================
        Thank you please come again!
============================================
"""
                    st.code(receipt_text, language="text")

                    # Wipe cart clean for next customer
                    st.session_state.cart = {}
                    st.button("Start Next Order")
            else:
                st.error("Insufficient cash amount entered")

        if st.button("Clear Entire Basket", type="secondary"):
            st.session_state.cart = {}
            st.rerun()