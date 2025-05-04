from dataset import get_dataset
from recommendation import recommend_agents

def main():
    print("=== Test Recommendation System ===")
    print("Example query: 'I want test for mid level position who knows English for agency manager'\n")

    dataset = get_dataset()

    user_query = input("Enter your requirements: ").strip()

    if not user_query:
        print("No input provided. Exiting.")
        return

    recommendations = recommend_agents(user_query, dataset)

    if recommendations.empty:
        print("\nNo suitable tests found.")
    else:
        print("\nTop Recommendations:\n")
        for _, row in recommendations.iterrows():
            print(f"Test Name   : {row.get('name')}")
            print(f"Category    : {row.get('category')}")
            print(f"Description : {row.get('description')}")
            print(f"Image URL   : {row.get('imagelink')}")
            print(f"Similarity  : {round(row['similarity'], 3)}")
            print("-" * 50)

if __name__ == "__main__":
    main()
