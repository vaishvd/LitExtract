from utils.config import dir_fulltexts, dir_researcharticles
from utils.article_fetcher import filter_research_articles

# Filter and save research articles
filter_research_articles(dir_fulltexts,dir_researcharticles)
print("Research articles saved successfully.")
