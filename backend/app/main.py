from fastapi import FastAPI, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from app.services.ingestion import fetch_news
from app.services.dedupe import Deduplicator
from app.services.clustering import cluster_stories
from app.models import StoryCluster, Article
from typing import List, Optional

app = FastAPI(title="TechCurator Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

deduper = Deduplicator()
current_clusters: List[StoryCluster] = []

@app.on_event("startup")
async def startup():
    # Trigger initial fetch (blocking for demo simplicity)
    run_pipeline()

@app.get("/feed", response_model=List[StoryCluster])
async def get_feed(q: Optional[str] = Query(None, description="Search query to filter stories")):
    if q:
        query = q.lower()
        filtered_clusters = []
        for cluster in current_clusters:
            # Check topic label
            if query in cluster.topic_label.lower():
                filtered_clusters.append(cluster)
                continue

            # Check primary article
            if query in cluster.primary_article.title.lower() or \
               (cluster.primary_article.summary and query in cluster.primary_article.summary.lower()):
                filtered_clusters.append(cluster)
                continue

            # Check related articles
            for article in cluster.related_articles:
                if query in article.title.lower() or \
                   (article.summary and query in article.summary.lower()):
                    filtered_clusters.append(cluster)
                    break

        return filtered_clusters

    return current_clusters

@app.post("/refresh")
async def refresh_feed(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_pipeline)
    return {"status": "Ingestion triggered"}

def run_pipeline():
    global current_clusters
    print("--- Starting Ingestion Pipeline ---")
    
    raw_data = fetch_news()
    unique_articles = []
    
    for data in raw_data:
        # Create a signature from title + summary
        sig = f"{data['title']} {data['summary']}"
        if not deduper.is_duplicate(data['url'], sig):
            unique_articles.append(Article(**data))
            
    print(f"Deduplication: {len(raw_data)} -> {len(unique_articles)} items")
    
    current_clusters = cluster_stories(unique_articles)
    print(f"Clustering: Generated {len(current_clusters)} clusters")
