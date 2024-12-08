from sentence_transformers import SentenceTransformer
import faiss

# Załaduj model do tworzenia wektorów
model = SentenceTransformer('all-MiniLM-6-v2')

# Poodziel tekst na fragmenty
documents = pdf_text.split("\n\n")  # Dziel na akapity
embeddings = model.encode(documents)

# Stwórz bazę danych FAISS
dimension = embeddings.shape[1]
index = faiss.IndexFlat2(dimension)
index.add(embeddings)

# Test: wyszukaj podpbnfragment

query = "Jak stworzyc ekran gry?"
query_embedding = model.encode([query])
distances, indices = index.search(query_embedding, k=3)
print([documents[i] for i in indices[0]])
