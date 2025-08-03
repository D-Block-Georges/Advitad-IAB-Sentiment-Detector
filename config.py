"""
Configuration et constantes pour le Content Analyzer
Centralise les listes et paramètres utilisés dans l'analyse
"""

# Types de contenu pour la classification
CONTENT_TYPES = [
    "product recommendation", 
    "news article", 
    "travel guide", 
    "opinion", 
    "review",
    "tutorial",
    "blog post",
    "research article"
]

# Mapping des sentiments (si nécessaire selon le modèle)
SENTIMENT_MAPPING = {
    'label_0': 'negative',
    'label_1': 'neutral', 
    'label_2': 'positive'
}

# Configuration des modèles
DEFAULT_CLASSIFICATION_MODEL = "knowledgator/gliclass-modern-base-v3.0"
DEFAULT_SENTIMENT_MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"

# Seuils pour la classification
TIER1_THRESHOLD = 0.1
FINAL_THRESHOLD = 0.3
CONTENT_TYPE_THRESHOLD = 0.3

# Limites
MAX_IAB_CATEGORIES = 4
MAX_TOP_RESULTS = 5

# Chemins des fichiers
TAXONOMY_PATHS = [
    'data/Content Taxonomy 3.1.tsv',
    'Content Taxonomy 3.1.tsv', 
    '../data/Content Taxonomy 3.1.tsv'
]
