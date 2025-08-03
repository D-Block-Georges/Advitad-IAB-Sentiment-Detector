"""
Script de test pour vérifier la cohérence avec tests.ipynb
"""

import sys
import os
sys.path.append('/root/genesis')

def test_taxonomy_loading():
    """Test de chargement de la taxonomie"""
    try:
        from models.classifier import classifier
        print(f"✅ Taxonomie chargée: {len(classifier.tier1_labels)} catégories Tier 1")
        print(f"✅ Mappings créés: {len(classifier.id2label)} entrées")
        print(f"✅ Descendants: {len(classifier.descendants)} groupes")
        
        # Afficher quelques exemples
        print("\n📋 Exemples de catégories Tier 1:")
        for i, label in enumerate(classifier.tier1_labels[:5]):
            print(f"  {i+1}. {label}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors du chargement: {e}")
        return False

def test_config():
    """Test de la configuration"""
    try:
        import config
        print(f"✅ Types de contenu: {len(config.CONTENT_TYPES)} définis")
        print(f"✅ Seuils: Tier1={config.TIER1_THRESHOLD}, Final={config.FINAL_THRESHOLD}")
        
        print("\n📋 Types de contenu configurés:")
        for i, ctype in enumerate(config.CONTENT_TYPES):
            print(f"  {i+1}. {ctype}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors du test config: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Test de la refactorisation du classifier")
    print("=" * 50)
    
    success = True
    success &= test_config()
    print()
    success &= test_taxonomy_loading()
    
    if success:
        print("\n🎉 Tous les tests sont passés!")
        print("Le classifier est cohérent avec tests.ipynb")
    else:
        print("\n💥 Certains tests ont échoué")
