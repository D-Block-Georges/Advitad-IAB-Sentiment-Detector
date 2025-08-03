"""
Content Analyzer - Application principale Flask
"""

import os
import logging
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
app.config['HOST'] = os.getenv('HOST', '0.0.0.0')
app.config['PORT'] = int(os.getenv('PORT', 5000))

@app.route('/')
def index():
    """Page d'accueil avec formulaire d'analyse"""
    return render_template('index.html')

@app.route('/health')
def health():
    """Endpoint de santé pour vérifier que l'API fonctionne"""
    return jsonify({
        'status': 'healthy',
        'service': 'content-analyzer',
        'version': '1.0.0'
    })

@app.route('/models/status')
def models_status():
    """Vérifie si les modèles ML sont chargés et prêts"""
    try:
        from models.classifier import classifier
        
        if classifier is None:
            return jsonify({
                'status': 'unavailable',
                'message': 'Dépendances ML non installées',
                'classification_ready': False,
                'sentiment_ready': False
            })
        
        # Vérifier si les modèles sont chargés
        classification_ready = classifier._classification_pipeline is not None
        sentiment_ready = classifier._sentiment_pipeline is not None
        
        return jsonify({
            'status': 'ready' if (classification_ready and sentiment_ready) else 'loading',
            'classification_ready': classification_ready,
            'sentiment_ready': sentiment_ready,
            'taxonomy_loaded': len(classifier.tier1_labels) > 0
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'classification_ready': False,
            'sentiment_ready': False
        }), 500

@app.route('/models/preload', methods=['POST'])
def preload_models():
    """Force le préchargement des modèles ML"""
    try:
        from models.classifier import classifier
        
        if classifier is None:
            return jsonify({'error': 'Dépendances ML non disponibles'}), 500
        
        # Forcer le chargement des modèles
        classifier._get_classification_pipeline()
        classifier._get_sentiment_pipeline()
        
        return jsonify({
            'status': 'success',
            'message': 'Modèles préchargés avec succès'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Endpoint principal pour analyser du contenu
    Accepte soit un contenu textuel, soit une URL
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        content = data.get('content')
        url = data.get('url')
        
        if not content and not url:
            return jsonify({'error': 'Either content or url must be provided'}), 400
        
        # Vérifier que les modèles sont disponibles
        from models.classifier import classifier
        if classifier is None:
            return jsonify({'error': 'Modèles ML non disponibles'}), 503
        
        # Extraction de contenu depuis URL ou texte direct
        if url:
            try:
                from models.content_extractor import extractor
                logger.info(f"🌐 Extraction de contenu depuis: {url}")
                
                extraction_result = extractor.extract_from_url(url)
                extracted_text = extraction_result['text']
                metadata = {
                    'title': extraction_result['title'],
                    'description': extraction_result['description'],
                    'url': extraction_result['url'],
                    'author': extraction_result.get('author', ''),
                    'published_date': extraction_result.get('published_date', '')
                }
                
                # Valider le contenu extrait
                is_valid, validation_message = extractor.validate_content(extraction_result)
                if not is_valid:
                    logger.warning(f"⚠️ Contenu extrait invalide: {validation_message}")
                    return jsonify({'error': f'Contenu extrait invalide: {validation_message}'}), 400
                
                logger.info(f"✅ Extraction réussie: {validation_message}")
                
            except Exception as e:
                logger.error(f"❌ Erreur lors de l'extraction: {str(e)}")
                return jsonify({'error': f'Impossible d\'extraire le contenu de l\'URL: {str(e)}'}), 400
        else:
            extracted_text = content
            metadata = {
                'title': 'Contenu saisi directement',
                'description': content[:200] + '...' if len(content) > 200 else content,
                'url': 'direct_input'
            }
        
        # Analyse avec les vrais modèles
        try:
            # Debug: logger le texte analysé
            logger.info(f"🔍 Analyse du texte (longueur: {len(extracted_text)})")
            logger.info(f"📝 Début du texte: {extracted_text[:300]}...")
            
            analysis_results = classifier.analyze_full_content(extracted_text)
            
            # Debug: logger les résultats
            logger.info(f"📊 Résultats d'analyse: {analysis_results}")
            
            result = {
                'iab_categories': analysis_results['iab_categories'],
                'sentiment': analysis_results['sentiment'],
                'content_type': analysis_results['content_type'],
                'extracted_text': extracted_text[:500] + '...' if len(extracted_text) > 500 else extracted_text,
                'metadata': metadata
            }
            
            return jsonify(result)
            
        except Exception as e:
            # Erreur lors de l'analyse - retourner l'erreur réelle
            logger.error(f"❌ Erreur lors de l'analyse ML: {str(e)}")
            return jsonify({
                'error': f'Erreur lors de l\'analyse: {str(e)}',
                'details': 'Vérifiez que les modèles ML sont correctement chargés'
            }), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
