import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors

# 1. LOADING MY CSV
df = pd.read_csv("music_data.csv")

# Create a combined text column for embedding
df["combined"] = df["genre"] + " " + df["name"] + " " + df["artist"]

# 2. LOAD EMBEDDING MODEL
model = SentenceTransformer("all-MiniLM-L6-v2")

# Encode all database entries
vectors = model.encode(df["combined"].tolist(), convert_to_numpy=True)

# 3. BUILD NEAREST-NEIGHBORS INDEX
# n_neighbors = how many recommendations to store in index
nn = NearestNeighbors(n_neighbors=5, metric="cosine")
nn.fit(vectors)

# 4. GET USER INPUT
query = input("Describe your music vibe: ")

# Encode the query
query_vec = model.encode([query], convert_to_numpy=True)

# 5. SEARCH TOP MATCHES
distances, indices = nn.kneighbors(query_vec)

print("\n🎧 TOP MATCHES:\n")

for idx in indices[0]:
    row = df.iloc[idx]
    print(f"- {row['name']} by {row['artist']}  ({row['genre']})")
