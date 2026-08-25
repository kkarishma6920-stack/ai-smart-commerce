from utils.recommender import recommend_products


query = "laptop under 60000"

results = recommend_products(query)

print("\nTop Recommendations:\n")

for _, product in results.iterrows():

    print(
        f"{product['name']} | "
        f"₹{product['price']:,} | "
        f"Rating: ⭐ {product['rating']} | "
        f"Score: {product['recommendation_score']:.2f}"
    )