"""
Liste des modèles LLM disponibles
"""

MODELS = {
    "mistral:latest": {
        "size": "4 GB",
        "description": "Rapide, léger",
        "category": "general"
    },
    "mistral-small3.2:latest": {
        "size": "15 GB",
        "description": "Plus puissant",
        "category": "general"
    },
    "devstral-small-2:24b": {
        "size": "15 GB",
        "description": "Code (Mistral)",
        "category": "code"
    },
    "qwen3:32b": {
        "size": "20 GB",
        "description": "Chat général",
        "category": "general"
    },
    "qwen3-vl:32b": {
        "size": "21 GB",
        "description": "Vision (images)",
        "category": "vision"
    },
    "qwen3-coder:30b": {
        "size": "18 GB",
        "description": "Code",
        "category": "code"
    },
    "llama3.3:latest": {
        "size": "42 GB",
        "description": "Meta LLaMA",
        "category": "general"
    },
    "gpt-oss:20b": {
        "size": "14 GB",
        "description": "GPT open-source",
        "category": "general"
    },
    "gpt-oss:120b": {
        "size": "65 GB",
        "description": "GPT (très gros)",
        "category": "general"
    },
    "pxlksr/llama-3-refueled:f16": {
        "size": "16 GB",
        "description": "LLaMA fine-tuné",
        "category": "general"
    },
    "michaelborck/refuled:latest": {
        "size": "5 GB",
        "description": "LLaMA fine-tuné",
        "category": "general"
    }
}

# Modèles recommandés par catégorie
RECOMMENDED_MODELS = {
    "general": "gpt-oss:20b",
    "code": "qwen3-coder:30b",
    "vision": "qwen3-vl:32b",
    "lightweight": "mistral:latest"
}

def get_all_models():
    """Retourne tous les modèles disponibles"""
    return MODELS

def get_model_info(model_name):
    """Retourne les informations d'un modèle spécifique"""
    return MODELS.get(model_name)

def get_models_by_category(category):
    """Retourne les modèles par catégorie"""
    return {name: info for name, info in MODELS.items() if info["category"] == category}

def get_recommended_model(category):
    """Retourne le modèle recommandé pour une catégorie"""
    return RECOMMENDED_MODELS.get(category)