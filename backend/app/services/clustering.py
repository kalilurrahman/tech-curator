from sklearn.cluster import AgglomerativeClustering
from sentence_transformers import SentenceTransformer
from app.models import Article, StoryCluster
import numpy as np
from app.services.llm import generate_topic_label

# Load once
embedder = SentenceTransformer('all-MiniLM-L6-v2')

def cluster_stories(articles):
    if not articles: return []
    if len(articles) == 1:
        return [StoryCluster(
            cluster_id="single-0", 
            primary_article=articles[0], 
            related_articles=[], 
            topic_label="NEWS"
        )]

    texts = [f"{a.title} {a.summary}" for a in articles]
    embeddings = embedder.encode(texts)
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

    clustering = AgglomerativeClustering(
        n_clusters=None,
        distance_threshold=0.6,
        metric='cosine',
        linkage='average'
    )
    labels = clustering.fit_predict(embeddings)

    clusters = {}
    for idx, label in enumerate(labels):
        if label not in clusters: clusters[label] = []
        clusters[label].append(articles[idx])

    results = []
    for label, group in clusters.items():
        primary = group[0]
        related = group[1:]
        tag = generate_topic_label(primary.title)
        
        results.append(StoryCluster(
            cluster_id=f"c-{label}",
            primary_article=primary,
            related_articles=related,
            topic_label=tag
        ))
        
    return results
