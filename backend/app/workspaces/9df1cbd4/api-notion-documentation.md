# Documentation de l'API Notion

## Table des matières
- [Introduction](#introduction)
- [Authentification](#authentification)
- [Endpoints principaux](#endpoints-principaux)
- [Types de données](#types-de-données)
- [Bases de données](#bases-de-données)
- [Pages](#pages)
- [Blocs](#blocs)
- [Utilisateurs](#utilisateurs)
- [Recherche](#recherche)
- [Webhooks](#webhooks)
- [Exemples de code](#exemples-de-code)
- [Limitations et quotas](#limitations-et-quotas)
- [Bonnes pratiques](#bonnes-pratiques)
- [Codes d'erreur](#codes-derreur)
- [Ressources utiles](#ressources-utiles)

---

## Introduction

L'API Notion permet d'interagir avec les données de Notion de manière programmatique. Elle offre un accès RESTful à vos bases de données, pages et blocs de contenu.

### Caractéristiques principales
- **API REST** : Endpoints HTTP standards (GET, POST, PATCH, DELETE)
- **Format JSON** : Pour les requêtes et réponses
- **Version actuelle** : v1
- **URL de base** : `https://api.notion.com/v1/`
- **Format des dates** : ISO 8601 (YYYY-MM-DD)

---

## Authentification

### Clé API
Pour utiliser l'API Notion, vous devez obtenir une clé d'intégration :

```http
Authorization: Bearer VOTRE_CLÉ_SECRÈTE_NOTION
Notion-Version: 2022-06-28
Content-Type: application/json
```

### Créer une intégration
1. Accédez à [Notion Developers](https://www.notion.so/my-integrations)
2. Créez une nouvelle intégration
3. Obtenez votre clé secrète interne (Internal Integration Token)
4. Partagez vos pages/bases avec l'intégration

### Configuration des en-têtes HTTP
```bash
# En-têtes requis pour toutes les requêtes
curl -X GET "https://api.notion.com/v1/users/me" \
  -H "Authorization: Bearer secret_yourTokenHere" \
  -H "Notion-Version: 2022-06-28"
```

---

## Endpoints principaux

### Bases de données
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/databases/{database_id}` | Récupérer une base de données |
| `POST` | `/databases/{database_id}/query` | Interroger une base de données |
| `POST` | `/databases` | Créer une base de données |
| `PATCH` | `/databases/{database_id}` | Mettre à jour une base de données |

### Pages
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/pages/{page_id}` | Récupérer une page |
| `POST` | `/pages` | Créer une page |
| `PATCH` | `/pages/{page_id}` | Mettre à jour une page |

### Blocs
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/blocks/{block_id}` | Récupérer un bloc |
| `GET` | `/blocks/{block_id}/children` | Récupérer les enfants d'un bloc |
| `PATCH` | `/blocks/{block_id}` | Mettre à jour un bloc |
| `POST` | `/blocks/{block_id}/children` | Ajouter des blocs enfants |
| `DELETE` | `/blocks/{block_id}` | Supprimer un bloc |

### Autres endpoints
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/users` | Lister tous les utilisateurs |
| `GET` | `/users/{user_id}` | Récupérer un utilisateur |
| `POST` | `/search` | Rechercher du contenu |

---

## Types de données

### Propriétés de page principales
```json
{
  "Nom": {
    "title": [
      {
        "text": {
          "content": "Titre de la page"
        }
      }
    ]
  },
  "Description": {
    "rich_text": [
      {
        "text": {
          "content": "Description détaillée"
        }
      }
    ]
  },
  "Statut": {
    "select": {
      "name": "En cours"
    }
  },
  "Priorité": {
    "select": {
      "name": "Haute",
      "color": "red"
    }
  },
  "Date échéance": {
    "date": {
      "start": "2024-01-15",
      "end": "2024-01-20"
    }
  },
  "URL": {
    "url": "https://exemple.com"
  },
  "Tags": {
    "multi_select": [
      {"name": "Urgent", "color": "red"},
      {"name": "Important", "color": "orange"}
    ]
  },
  "Personne assignée": {
    "people": [
      {"id": "user_id"}
    ]
  },
  "Vérifié": {
    "checkbox": true
  },
  "Nombre": {
    "number": 42
  }
}
```

### Types de propriétés disponibles
- **title** : Titre de page
- **rich_text** : Texte enrichi
- **number** : Nombre
- **select** : Sélection unique
- **multi_select** : Sélection multiple
- **date** : Date
- **people** : Personnes
- **files** : Fichiers
- **checkbox** : Case à cocher
- **url** : URL
- **email** : Email
- **phone_number** : Numéro de téléphone
- **formula** : Formule
- **relation** : Relation
- **rollup** : Agrégation

---

## Bases de données

### Créer une base de données
```json
{
  "parent": {
    "type": "page_id",
    "page_id": "page_id_parent"
  },
  "title": [
    {
      "type": "text",
      "text": {
        "content": "Ma base de données"
      }
    }
  ],
  "properties": {
    "Nom": {
      "title": {}
    },
    "Description": {
      "rich_text": {}
    },
    "Statut": {
      "select": {
        "options": [
          {"name": "À faire", "color": "red"},
          {"name": "En cours", "color": "yellow"},
          {"name": "Terminé", "color": "green"}
        ]
      }
    },
    "Date création": {
      "created_time": {}
    },
    "Dernière modification": {
      "last_edited_time": {}
    }
  }
}
```

### Interroger une base de données
```json
{
  "filter": {
    "and": [
      {
        "property": "Statut",
        "select": {
          "equals": "En cours"
        }
      },
      {
        "property": "Priorité",
        "select": {
          "equals": "Haute"
        }
      }
    ]
  },
  "sorts": [
    {
      "property": "Date",
      "direction": "descending"
    },
    {
      "timestamp": "created_time",
      "direction": "ascending"
    }
  ],
  "page_size": 50
}
```

### Filtres disponibles
- **equals** : Égal à
- **does_not_equal** : Différent de
- **contains** : Contient
- **does_not_contain** : Ne contient pas
- **starts_with** : Commence par
- **ends_with** : Termine par
- **greater_than** : Supérieur à
- **less_than** : Inférieur à
- **is_empty** : Est vide
- **is_not_empty** : N'est pas vide

---

## Pages

### Créer une page dans une base de données
```json
{
  "parent": {
    "type": "database_id",
    "database_id": "database_id"
  },
  "properties": {
    "Nom": {
      "title": [
        {
          "text": {
            "content": "Nouvelle tâche"
          }
        }
      ]
    },
    "Description": {
      "rich_text": [
        {
          "text": {
            "content": "Description de la tâche..."
          }
        }
      ]
    },
    "Statut": {
      "select": {
        "name": "À faire"
      }
    }
  }
}
```

### Créer une page sous une autre page
```json
{
  "parent": {
    "type": "page_id",
    "page_id": "parent_page_id"
  },
  "properties": {
    "title": [
      {
        "text": {
          "content": "Page enfant"
        }
      }
    ]
  }
}
```

### Mettre à jour une page
```json
{
  "properties": {
    "Statut": {
      "select": {
        "name": "Terminé"
      }
    },
    "Date fin": {
      "date": {
        "start": "2024-01-15",
        "end": null
      }
    }
  }
}
```

### Archiver une page
```json
{
  "archived": true
}
```

---

## Blocs

### Types de blocs supportés
| Type | Description |
|------|-------------|
| **paragraph** | Paragraphe de texte |
| **heading_1**, **heading_2**, **heading_3** | Titres de différents niveaux |
| **bulleted_list_item** | Élément de liste à puces |
| **numbered_list_item** | Élément de liste numérotée |
| **to_do** | Case à cocher |
| **toggle** | Bloc dépliable |
| **code** | Code source avec coloration syntaxique |
| **quote** | Citation |
| **callout** | Encadré spécial avec emoji |
| **divider** | Séparateur horizontal |
| **image** | Image |
| **file** | Fichier |
| **embed** | Contenu embarqué (YouTube, etc.) |
| **bookmark** | Signet |
| **equation** | Équation mathématique |
| **table** | Tableau |
| **table_row** | Ligne de tableau |

### Structure d'un bloc
```json
{
  "object": "block",
  "id": "block_id",
  "type": "paragraph",
  "paragraph": {
    "rich_text": [
      {
        "type": "text",
        "text": {
          "content": "Contenu du bloc",
          "link": null
        },
        "annotations": {
          "bold": false,
          "italic": false,
          "strikethrough": false,
          "underline": false,
          "code": false,
          "color": "default"
        }
      }
    ]
  }
}
```

### Ajouter des blocs enfants à une page
```json
{
  "children": [
    {
      "object": "block",
      "type": "heading_1",
      "heading_1": {
        "rich_text": [
          {
            "type": "text",
            "text": {
              "content": "Titre principal"
            }
          }
        ],
        "color": "blue"
      }
    },
    {
      "object": "block",
      "type": "paragraph",
      "paragraph": {
        "rich_text": [
          {
            "type": "text",
            "text": {
              "content": "Ceci est un "
            }
          },
          {
            "type": "text",
            "text": {
              "content": "texte en gras",
              "link": null
            },
            "annotations": {
              "bold": true,
              "italic": false
            }
          },
          {
            "type": "text",
            "text": {
              "content": " et ceci est du "
            }
          },
          {
            "type": "text",
            "text": {
              "content": "code",
              "link": null
            },
            "annotations": {
              "code": true
            }
          }
        ]
      }
    }
  ]
}
```

### Exemple de bloc code avec langage
```json
{
  "object": "block",
  "type": "code",
  "code": {
    "rich_text": [
      {
        "type": "text",
        "text": {
          "content": "function hello() {\n  console.log('Hello World!');\n}"
        }
      }
    ],
    "language": "javascript",
    "caption": [
      {
        "type": "text",
        "text": {
          "content": "Exemple de fonction JavaScript"
        }
      }
    ]
  }
}
```

---

## Utilisateurs

### Récupérer tous les utilisateurs
```bash
curl -X GET "https://api.notion.com/v1/users" \
  -H "Authorization: Bearer secret_yourToken" \
  -H "Notion-Version: 2022-06-28"
```

### Structure d'un utilisateur
```json
{
  "object": "user",
  "id": "user_id",
  "type": "person",
  "person": {
    "email": "user@example.com"
  },
  "name": "John Doe",
  "avatar_url": "https://example.com/avatar.jpg"
}
```

### Types d'utilisateurs
- **person** : Utilisateur humain
- **bot** : Intégration/bot
- **guest** : Invité

---

## Recherche

### Rechercher du contenu
```json
{
  "query": "mot clé",
  "filter": {
    "value": "page",
    "property": "object"
  },
  "sort": {
    "direction": "descending",
    "timestamp": "last_edited_time"
  },
  "page_size": 50
}
```

### Filtres de recherche
```json
{
  "filter": {
    "value": "database",
    "property": "object"
  }
}
```

```json
{
  "filter": {
    "or": [
      {
        "property": "object",
        "value": "page"
      },
      {
        "property": "object",
        "value": "database"
      }
    ]
  }
}
```

---

## Webhooks

### Configuration des webhooks
1. Créez un endpoint webhook dans votre application
2. Enregistrez l'URL dans [l'interface développeur Notion](https://www.notion.so/my-integrations)
3. Implémentez la vérification du webhook
4. Gérez les événements reçus

### Structure d'un événement webhook
```json
{
  "object": "page",
  "id": "page_id",
  "created_time": "2024-01-01T00:00:00.000Z",
  "last_edited_time": "2024-01-01T01:00:00.000Z",
  "archived": false,
  "url": "https://www.notion.so/Page-Title-page_id",
  "properties": {
    // Propriétés de la page
  }
}
```

### Types d'événements
| Événement | Description |
|-----------|-------------|
| **page.created** | Page créée |
| **page.updated** | Page mise à jour |
| **page.deleted** | Page supprimée |
| **database.updated** | Base de données mise à jour |
| **block.children.updated** | Blocs enfants modifiés |

### Vérification du webhook
```python
import hashlib
import hmac

def verify_webhook_signature(body, signature_header, secret):
    signature = hmac.new(
        secret.encode('utf-8'),
        body.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, signature_header)
```

---

## Exemples de code

### Python avec requests
```python
import requests
import json
import os
from typing import Dict, Any

class NotionAPI:
    def __init__(self, token: str):
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
    
    def get_database(self, database_id: str) -> Dict[str, Any]:
        """Récupérer une base de données"""
        response = requests.get(
            f"{self.base_url}/databases/{database_id}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def query_database(self, database_id: str, filter_data: Dict = None, sorts: list = None) -> Dict[str, Any]:
        """Interroger une base de données"""
        data = {}
        if filter_data:
            data["filter"] = filter_data
        if sorts:
            data["sorts"] = sorts
        
        response = requests.post(
            f"{self.base_url}/databases/{database_id}/query",
            headers=self.headers,
            json=data
        )
        response.raise_for_status()
        return response.json()
    
    def create_page(self, parent_type: str, parent_id: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        """Créer une page"""
        data = {
            "parent": {
                parent_type: parent_id
            },
            "properties": properties
        }
        
        response = requests.post(
            f"{self.base_url}/pages",
            headers=self.headers,
            json=data
        )
        response.raise_for_status()
        return response.json()

# Utilisation
notion = NotionAPI(os.getenv("NOTION_TOKEN"))

# Créer une tâche
new_task = notion.create_page(
    parent_type="database_id",
    parent_id=os.getenv("TASKS_DATABASE_ID"),
    properties={
        "Nom": {
            "title": [
                {"text": {"content": "Nouvelle tâche API"}}
            ]
        },
        "Description": {
            "rich_text": [
                {"text": {"content": "Créée via l'API Python"}}
            ]
        }
    }
)
```

### JavaScript/Node.js avec le SDK officiel
```javascript
const { Client } = require('@notionhq/client');

// Initialiser le client
const notion = new Client({
  auth: process.env.NOTION_TOKEN,
});

// Fonction pour créer une page
async function createPage(databaseId, title, description) {
  try {
    const response = await notion.pages.create({
      parent: {
        database_id: databaseId,
      },
      properties: {
        Name: {
          title: [
            {
              text: {
                content: title,
              },
            },
          ],
        },
        Description: {
          rich_text: [
            {
              text: {
                content: description,
              },
            },
          ],
        },
        Status: {
          select: {
            name: 'To Do',
          },
        },
      },
    });
    
    console.log('Page créée:', response.id);
    return response;
  } catch (error) {
    console.error('Erreur:', error);
    throw error;
  }
}

// Fonction pour récupérer une base de données
async function queryDatabase(databaseId, filter = {}) {
  const response = await notion.databases.query({
    database_id: databaseId,
    filter: filter,
    sorts: [
      {
        property: 'Date',
        direction: 'descending',
      },
    ],
  });
  
  return response.results;
}

// Utilisation
async function main() {
  const databaseId = process.env.DATABASE_ID;
  
  // Créer une page
  await createPage(databaseId, 'Tâche API', 'Créée avec Node.js');
  
  // Interroger la base
  const tasks = await queryDatabase(databaseId, {
    property: 'Status',
    select: {
      equals: 'To Do',
    },
  });
  
  console.log(`Tâches à faire: ${tasks.length}`);
}

main();
```

---

## Limitations et quotas

### Limites de taux
| Limite | Valeur | Description |
|--------|--------|-------------|
| **Requêtes par seconde** | ~3 req/s | Limite variable selon le plan |
| **Requêtes par minute** | ~100 req/min | Pour éviter le throttling |
| **Taille de payload** | 5 MB | Maximum par requête |
| **Pages par réponse** | 100 | Maximum pour les requêtes paginées |

### Bonnes pratiques pour éviter les limites
1. **Mise en cache** : Cachez les données statiques
2. **Retry avec backoff** : Implémentez une stratégie de retry exponentiel
3. **Pagination** : Traitez toutes les pages de résultats
4. **Batching** : Regroupez les opérations lorsque possible

### Exemple de retry avec backoff
```python
import time
import requests
from requests.exceptions import HTTPError

def make_request_with_retry(url, headers, data=None, max_retries=3):
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except HTTPError as err:
            if err.response.status_code == 429:  # Too Many Requests
                wait_time = (2 ** retry_count) + random.random()
                time.sleep(wait_time)
                retry_count += 1
            else:
                raise
    
    raise Exception(f"Échec après {max_retries} tentatives")
```

---

## Bonnes pratiques

### 1. Validation des données
```python
def validate_page_properties(properties):
    """Valider les propriétés d'une page avant envoi"""
    required_fields = ['Nom']
    
    for field in required_fields:
        if field not in properties:
            raise ValueError(f"Champ requis manquant: {field}")
    
    # Valider les types de propriétés
    for prop_name, prop_value in properties.items():
        if not isinstance(prop_value, dict):
            raise ValueError(f"Propriété {prop_name} doit être un objet")
    
    return True
```

### 2. Gestion des erreurs robuste
```python
class NotionError(Exception):
    """Exception personnalisée pour les erreurs Notion"""
    pass

def handle_notion_error(response):
    """Gérer les erreurs de l'API Notion"""
    if response.status_code == 400:
        raise NotionError(f"Requête invalide: {response.text}")
    elif response.status_code == 401:
        raise NotionError("Authentification invalide")
    elif response.status_code == 403:
        raise NotionError("Permission refusée")
    elif response.status_code == 404:
        raise NotionError("Ressource non trouvée")
    elif response.status_code == 429:
        raise NotionError("Limite de taux dépassée")
    elif response.status_code >= 500:
        raise NotionError("Erreur serveur Notion")
    
    return response.json()
```

### 3. Performance et optimisation
- **Récupération sélective** : Ne récupérez que les propriétés nécessaires
- **Pagination** : Traitez les résultats paginés efficacement
- **Cache** : Mettez en cache les données rarement modifiées
- **Requêtes parallèles** : Utilisez le threading pour les opérations indépendantes

### 4. Sécurité
- **Variables d'environnement** : Stockez les tokens dans des variables d'env
- **Permissions minimales** : Accordez seulement les permissions nécessaires
- **Validation d'entrée** : Validez toujours les données avant envoi
- **Logging sécurisé** : Ne logguez jamais les tokens ou données sensibles

---

## Codes d'erreur

### Codes HTTP courants
| Code | Signification | Solution recommandée |
|------|--------------|----------------------|
| **200** | Succès | - |
| **201** | Créé | - |
| **400** | Mauvaise requête | Vérifier le format JSON, les champs requis |
| **401** | Non autorisé | Vérifier le token d'authentification |
| **403** | Interdit | Vérifier les permissions de l'intégration |
| **404** | Non trouvé | Vérifier l'ID de la ressource |
| **409** | Conflit | La ressource existe déjà |
| **429** | Trop de requêtes | Attendre et réessayer avec backoff |
| **500** | Erreur interne serveur | Réessayer plus tard |
| **502** | Bad Gateway | Réessayer plus tard |
| **503** | Service indisponible | Réessayer plus tard |

### Messages d'erreur spécifiques
```json
{
  "object": "error",
  "status": 400,
  "code": "validation_error",
  "message": "body failed validation. Fix one: body.properties should be defined, instead was undefined."
}
```

```json
{
  "object": "error",
  "status": 403,
  "code": "object_not_found_within_parent",
  "message": "Could not find page with ID: page_id. Make sure the relevant pages and databases are shared with your integration."
}
```

---

## Ressources utiles

### Documentation officielle
- 📚 [Documentation API Notion](https://developers.notion.com/)
- 🔧 [Bibliothèques client officielles](https://developers.notion.com/docs/client-libraries)
- 🚀 [Guide de démarrage rapide](https://developers.notion.com/docs/getting-started)
- 📖 [Référence API complète](https://developers.notion.com/reference/intro)

### Communauté et support
- 💬 [Forum des développeurs Notion](https://developers.notion.com/)
- 🐦 [Twitter @NotionDevs](https://twitter.com/NotionDevs)
- 💻 [GitHub - Exemples et SDKs](https://github.com/topics/notion-api)
- 📊 [Statut de l'API Notion](https://status.notion.so/)

### Outils et bibliothèques
- **Python** : `notion-client`, `notion-sdk-py`
- **JavaScript/Node.js** : `@notionhq/client`
- **Go** : `go-notion`
- **Ruby** : `notion-ruby-client`
- **PHP** : `notion-php-sdk`

### Exemples de projets
1. **Synchronisation de données** : Sync Notion ↔️ Google Sheets
2. **Automation** : Création automatique de pages
3. **Intégration CMS** : Blog avec Notion comme backend
4. **Dashboard** : Visualisation de données Notion
5. **Bot Discord/Slack** : Notifications depuis Notion

---

## Guide de migration

### Migration de v1 à v2 (si applicable)
1. Vérifier les changements d'endpoints
2. Mettre à jour les en-têtes d'authentification
3. Adapter les structures de données
4. Tester en environnement de développement
5. Déployer progressivement

### Tests avant déploiement
```python
# Script de test pour vérifier la connexion
def test_connection():
    try:
        # Test de récupération de l'utilisateur
        response = notion.users.me()
        print(f"✅ Connecté en tant que: {response['name']}")
        
        # Test de création de page
        test_page = create_test_page()
        print(f"✅ Page de test créée: {test_page['id']}")
        
        # Test de suppression
        notion.pages.update(page_id=test_page['id'], archived=True)
        print("✅ Page de test archivée")
        
        return True
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False
```

---

**Dernière mise à jour : Janvier 2026**

*Pour les mises à jour et changements, consultez toujours la [documentation officielle](https://developers.notion.com/).*
