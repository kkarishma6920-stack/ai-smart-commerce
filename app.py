import streamlit as st

from utils.chatbot import get_chat_response
from utils.recommender import recommend_products
from utils.cart import (
    add_to_cart,
    remove_from_cart,
    update_quantity,
    get_cart_total
)
from utils.offers import generate_offer
from utils.analytics import get_product_stats
from utils.agent import run_shopping_agent


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Smart Commerce",
    page_icon="🛍️",
    layout="wide"
)


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "cart" not in st.session_state:
    st.session_state.cart = {}


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🛍️ AI Smart Commerce")

st.sidebar.write(
    "AI Growth & Agentic Commerce"
)

st.sidebar.divider()

st.sidebar.markdown(
    """
### 🚀 Capabilities

✅ AI Shopping Assistant

✅ AI Shopping Agent

✅ Smart Product Search

✅ Personalized Recommendations

✅ Customer Support

✅ Shopping Cart

✅ Personalized Offers

✅ Checkout Assistance

✅ Growth Analytics
"""
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigate",
    [
        "🤖 AI Shopping Assistant",
        "🧠 AI Shopping Agent",
        "🛒 Shopping Cart",
        "📊 Growth Dashboard"
    ]
)


# =========================================================
# AI SHOPPING ASSISTANT
# =========================================================

if page == "🤖 AI Shopping Assistant":

    st.title(
        "🤖 AI Smart Commerce Assistant"
    )

    st.subheader(
        "AI-powered Product Discovery • "
        "Recommendations • Agentic Shopping • "
        "Personalized Offers"
    )

    st.write(
        "Your AI-powered shopping assistant for "
        "product discovery, recommendations, "
        "customer support and purchase assistance."
    )

    st.divider()

    # =====================================================
    # CHAT
    # =====================================================

    st.subheader(
        "💬 Customer Support"
    )

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

    user_message = st.chat_input(
        "Ask a question..."
    )

    if user_message:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_message
            }
        )

        with st.chat_message("user"):

            st.markdown(
                user_message
            )

        response = get_chat_response(
            user_message
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        with st.chat_message("assistant"):

            st.markdown(
                response
            )

    st.divider()

    # =====================================================
    # SMART PRODUCT SEARCH
    # =====================================================

    st.subheader(
        "🔎 Smart Product Search"
    )

    search_query = st.text_input(
        "Search for products",
        placeholder="Example: laptop under 60000",
        key="search_box"
    )

    if search_query:

        results = recommend_products(
            search_query,
            top_n=3
        )

        if results is None or results.empty:

            st.warning(
                "❌ No matching products found."
            )

        else:

            st.subheader(
                "🎯 Product Recommendations"
            )

            for _, product in results.iterrows():

                st.markdown(
                    f"""
### 🛍️ {product['name']}

**Brand:** {product['brand']}

**Price:** ₹{product['price']:,.0f}

**Rating:** ⭐ {product['rating']}/5

**Stock:** {product['stock']} available

{product['description']}
"""
                )

                if st.button(
                    "🛒 Add to Cart",
                    key=f"search_add_{product['product_id']}"
                ):

                    st.session_state.cart = add_to_cart(
                        st.session_state.cart,
                        product
                    )

                    st.success(
                        f"✅ {product['name']} added to cart!"
                    )

                st.divider()


# =========================================================
# AI SHOPPING AGENT
# =========================================================

elif page == "🧠 AI Shopping Agent":

    st.title(
        "🧠 AI Shopping Agent"
    )

    st.write(
        "Tell the AI agent what you want to buy. "
        "It will understand your requirement, "
        "find products, recommend options and "
        "generate a personalized offer."
    )

    st.divider()

    # =====================================================
    # USER REQUEST
    # =====================================================

    agent_request = st.text_input(
        "What do you want to buy?",
        placeholder=(
            "Example: Find me a laptop under 60000"
        )
    )

    if st.button(
        "🚀 Ask AI Shopping Agent",
        type="primary",
        use_container_width=True
    ):

        if not agent_request.strip():

            st.warning(
                "Please tell the AI agent what "
                "you want to buy."
            )

        else:

            with st.spinner(
                "🤖 AI Agent is analyzing your request..."
            ):

                result = run_shopping_agent(
                    agent_request
                )

            st.markdown(
                result["message"]
            )

            # =================================================
            # PRODUCTS
            # =================================================

            if result["success"]:

                # ---------------------------------------------
                # PERSONALIZED OFFER
                # ---------------------------------------------

                if result["offer"]:

                    offer = result["offer"]

                    st.success(
                        f"🎁 {offer['title']}\n\n"
                        f"{offer['message']}"
                    )

                st.subheader(
                    "🎯 Agent Recommendations"
                )

                products = result["products"]

                for _, product in products.iterrows():

                    col1, col2 = st.columns(
                        [4, 1]
                    )

                    with col1:

                        st.markdown(
                            f"""
### 🛍️ {product['name']}

**Brand:** {product['brand']}

**Price:** ₹{product['price']:,.0f}

**Rating:** ⭐ {product['rating']}/5

**Stock:** {product['stock']} available

{product['description']}
"""
                        )

                    with col2:

                        st.write("")

                        if st.button(
                            "🛒 Add",
                            key=f"agent_add_{product['product_id']}"
                        ):

                            st.session_state.cart = add_to_cart(
                                st.session_state.cart,
                                product
                            )

                            st.success(
                                "Added!"
                            )

                    st.divider()


# =========================================================
# SHOPPING CART
# =========================================================

elif page == "🛒 Shopping Cart":

    st.title(
        "🛒 Shopping Cart"
    )

    cart = st.session_state.cart

    if not cart:

        st.info(
            "🛒 Your cart is empty."
        )

        st.write(
            "Search for products and click "
            "**Add to Cart**."
        )

    else:

        st.subheader(
            "Your Products"
        )

        st.divider()

        for product_id, item in list(
            cart.items()
        ):

            col1, col2, col3, col4 = st.columns(
                [4, 2, 2, 1]
            )

            with col1:

                st.markdown(
                    f"**{item['name']}**"
                )

            with col2:

                st.write(
                    f"₹{item['price']:,.0f}"
                )

            with col3:

                quantity = st.number_input(
                    "Quantity",
                    min_value=1,
                    max_value=20,
                    value=item["quantity"],
                    key=f"qty_{product_id}"
                )

                if quantity != item["quantity"]:

                    update_quantity(
                        cart,
                        product_id,
                        quantity
                    )

                    st.rerun()

            with col4:

                if st.button(
                    "🗑️",
                    key=f"remove_{product_id}"
                ):

                    remove_from_cart(
                        cart,
                        product_id
                    )

                    st.rerun()

            st.divider()

        total = get_cart_total(
            cart
        )

        st.subheader(
            f"💰 Total: ₹{total:,.2f}"
        )

        if st.button(
            "✅ Proceed to Checkout",
            type="primary",
            use_container_width=True
        ):

            st.success(
                "🎉 Order placed successfully!"
            )

            st.info(
                "Demo checkout completed successfully."
            )

            st.session_state.cart = {}


# =========================================================
# GROWTH DASHBOARD
# =========================================================

elif page == "📊 Growth Dashboard":

    st.title(
        "📊 AI Growth Dashboard"
    )

    st.write(
        "Commerce analytics and growth insights."
    )

    stats = get_product_stats()

    st.divider()

    # =====================================================
    # METRICS
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📦 Products",
            stats["total_products"]
        )

    with col2:

        st.metric(
            "⭐ Average Rating",
            f"{stats['average_rating']:.2f}"
        )

    with col3:

        st.metric(
            "📊 Total Stock",
            stats["total_stock"]
        )

    with col4:

        st.metric(
            "💰 Average Price",
            f"₹{stats['average_price']:,.0f}"
        )

    st.divider()

    # =====================================================
    # CATEGORY CHART
    # =====================================================

    st.subheader(
        "📈 Products by Category"
    )

    st.bar_chart(
        stats["category_counts"]
    )

    st.divider()

    # =====================================================
    # TOP PRODUCTS
    # =====================================================

    st.subheader(
        "🏆 Top Rated Products"
    )

    top_products = stats["top_products"]

    st.dataframe(
        top_products[
            [
                "name",
                "category",
                "brand",
                "price",
                "rating",
                "stock"
            ]
        ],
        use_container_width=True
    )

    st.divider()

    # =====================================================
    # AI GROWTH INSIGHT
    # =====================================================

    st.subheader(
        "🤖 AI Growth Insight"
    )

    if not top_products.empty:

        best_product = top_products.iloc[0]

        st.success(
            f"""
🚀 **Growth Recommendation**

**{best_product['name']}** has a rating of
⭐ {best_product['rating']}.

Promote highly-rated products through
personalized recommendations to improve
customer engagement and conversions.
"""
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🛍️ AI Smart Commerce | "
    "AI Growth & Agentic Commerce MVP"
)