# 🚀 Guide de Démarrage pour Nouvelle Session

## Comment me mettre à jour rapidement

### ✨ Méthode Recommandée (Une seule phrase)

Dites simplement:
```
"Lis SESSION_RESUME.md et specs/001-bible-hymnal-reader/spec.md pour te mettre à jour"
```

### 📋 Méthode Détaillée (Si besoin de contexte complet)

Dites:
```
"Mets-toi à jour en lisant dans cet ordre:
1. SESSION_RESUME.md - état actuel du projet
2. specs/001-bible-hymnal-reader/spec.md - spécifications complètes
3. specs/001-bible-hymnal-reader/tasks.md - tâches et progression"
```

### ⚡ Méthode Ultra-Rapide (Pour continuer direct)

Dites:
```
"Nous travaillons sur Baiboly (Bible + Fihirana en Malagasy).
Fihirana: ✅ 892 hymnes opérationnels avec recherche par numéro/titre/paroles
Bible: ✅ API fonctionnelle, livres importés
Lis SESSION_RESUME.md pour les détails"
```

---

## 📁 Fichiers Clés pour Me Mettre à Jour

### 1️⃣ Résumé de Session (TOUJOURS lire en premier)
**Fichier:** `SESSION_RESUME.md`
**Contenu:**
- ✅ État actuel (ce qui fonctionne)
- 🐛 Bugs résolus récemment
- 🗄️ Schéma base de données
- 🚀 Commandes utiles
- 📝 Tâches potentielles à venir

**Commande pour moi:**
```
Lis SESSION_RESUME.md
```

### 2️⃣ Spécifications Complètes
**Fichier:** `specs/001-bible-hymnal-reader/spec.md`
**Contenu:**
- 📖 User stories avec priorités
- ✅ Acceptance criteria
- 🎯 Functional requirements
- 🏗️ Architecture technique
- 🗄️ Modèle de données

**Commande pour moi:**
```
Lis specs/001-bible-hymnal-reader/spec.md
```

### 3️⃣ Plan d'Implémentation
**Fichier:** `specs/001-bible-hymnal-reader/plan.md`
**Contenu:**
- 🗺️ Phases d'implémentation
- 📊 Dépendances entre tâches
- ⚙️ Décisions techniques

**Commande pour moi:**
```
Lis specs/001-bible-hymnal-reader/plan.md
```

### 4️⃣ Tâches Détaillées
**Fichier:** `specs/001-bible-hymnal-reader/tasks.md`
**Contenu:**
- ☑️ Liste complète des tâches
- ✅ Statut de chaque tâche (TODO/DOING/DONE)
- 🔗 Dépendances

**Commande pour moi:**
```
Lis specs/001-bible-hymnal-reader/tasks.md
```

### 5️⃣ Modèle de Données
**Fichier:** `specs/001-bible-hymnal-reader/data-model.md`
**Contenu:**
- 🗄️ Schéma SQL complet
- 📊 Relations entre tables
- 💡 Exemples de données
- ⚠️ Notes critiques (ex: preservation des `\n`)

**Commande pour moi:**
```
Lis specs/001-bible-hymnal-reader/data-model.md
```

---

## 🎯 Exemples de Phrases pour Nouvelle Session

### Scénario 1: Continuer où nous nous sommes arrêtés
```
"Salut ! Nous travaillons sur le projet Baiboly.
Lis SESSION_RESUME.md pour te mettre à jour sur l'état actuel."
```

### Scénario 2: Nouvelle fonctionnalité
```
"Je veux ajouter [fonctionnalité X] au projet Baiboly.
Lis d'abord SESSION_RESUME.md et specs/001-bible-hymnal-reader/spec.md
pour comprendre l'architecture existante."
```

### Scénario 3: Bug à corriger
```
"J'ai un bug avec [composant Y].
Lis SESSION_RESUME.md section 'Bugs Connus' et
specs/001-bible-hymnal-reader/data-model.md pour le contexte technique."
```

### Scénario 4: Comprendre une partie spécifique
```
"Explique-moi comment fonctionne [Bible/Fihirana].
Lis specs/001-bible-hymnal-reader/spec.md section [nom de la section]."
```

---

## 🔍 Vérification Rapide de l'État du Projet

### Pour vérifier que tout fonctionne

**Commande:**
```bash
cd C:\Dev\baiboly
docker-compose ps
```

**Résultat attendu:**
```
baiboly_frontend   Up (healthy)
baiboly_backend    Up (healthy)
baiboly_db         Up (healthy)
```

### Pour tester l'API

**Bible:**
```bash
curl http://localhost:5000/api/bible/livres
```

**Fihirana:**
```bash
curl http://localhost:5000/api/fihirana?limit=5
```

**Recherche:**
```bash
curl "http://localhost:5000/api/fihirana/search?q=36"
```

### Pour voir l'interface

**URL:** http://localhost:5173

**Navigation:**
- Onglet **Baiboly** → Section Bible
- Onglet **Fihirana** → Liste des hymnes
- Onglet **Karohy** → Recherche dédiée

---

## 📊 État Actuel du Projet (Snapshot)

### ✅ Fonctionnalités Complètes

#### Fihirana (Hymnes)
- ✅ 892 hymnes importés (FFPM: 814, FANAMPINY: 54, ANTEMA: 24)
- ✅ Affichage avec versets numérotés et refrains colorés
- ✅ Recherche par numéro exact (ex: "36")
- ✅ Recherche par titre (ex: "Andriananahary")
- ✅ Recherche par contenu des paroles (ex: "Jeso")
- ✅ Navigation par collection
- ✅ Interface responsive (mobile, tablette, desktop)

#### Bible
- ✅ API fonctionnelle
- ✅ Livres importés en base de données
- ✅ Modèle de données créé (Livre, Chapitre, Verset)
- ✅ Endpoints disponibles:
  - `GET /api/bible/livres` - Liste des livres
  - `GET /api/bible/livres/{id}` - Détails d'un livre
  - `GET /api/bible/chapitres/{livre_id}/{chapitre_num}` - Versets d'un chapitre
  - `GET /api/bible/search` - Recherche dans la Bible

### 🚧 À Vérifier/Compléter

#### Bible (Frontend)
- ⚠️ Interface de lecture à vérifier
- ⚠️ Recherche Bible frontend à vérifier
- ⚠️ Navigation livre/chapitre/verset à vérifier

**Comment vérifier:**
```
"Teste la section Bible et montre-moi ce qui fonctionne et ce qui manque"
```

---

## 🗂️ Structure du Projet

```
baiboly/
├── SESSION_RESUME.md                    ← ⭐ Lire en PREMIER
├── QUICK_START_NOUVELLE_SESSION.md     ← Ce fichier
│
├── specs/001-bible-hymnal-reader/
│   ├── spec.md                          ← Spécifications complètes
│   ├── plan.md                          ← Plan d'implémentation
│   ├── tasks.md                         ← Tâches détaillées
│   └── data-model.md                    ← Schéma base de données
│
├── backend/
│   ├── src/
│   │   ├── models/
│   │   │   ├── fihirana.py              ← Modèles Hira, Tononkira, Sokajy
│   │   │   └── bible.py                 ← Modèles Livre, Chapitre, Verset
│   │   ├── services/
│   │   │   ├── fihirana_service.py      ← Logique métier Fihirana
│   │   │   └── bible_service.py         ← Logique métier Bible
│   │   ├── routes/
│   │   │   ├── fihirana.py              ← Endpoints API Fihirana
│   │   │   └── bible.py                 ← Endpoints API Bible
│   │   └── scripts/
│   │       ├── import_fihirana_json.py  ← Import hymnes depuis GitHub
│   │       └── import_bible.py          ← Import Bible (si existe)
│
└── frontend/
    └── src/
        ├── components/
        │   ├── fihirana/
        │   │   ├── FihiranaReader.tsx   ← Liste + lecture
        │   │   ├── FihiranaSearch.tsx   ← Recherche dédiée
        │   │   ├── FihiranaDetail.tsx   ← Affichage détaillé
        │   │   └── FihiranaList.tsx     ← Liste avec filtres
        │   └── bible/                   ← Composants Bible (à vérifier)
        └── pages/
            ├── FihiranaPage.tsx         ← Page principale Fihirana
            └── BiblePage.tsx            ← Page principale Bible (à vérifier)
```

---

## 💡 Conseils pour une Session Productive

### ✅ Bonnes Pratiques

1. **Toujours commencer par lire `SESSION_RESUME.md`**
   - Évite de refaire du travail déjà fait
   - Comprend les bugs déjà résolus
   - Sait exactement où en est le projet

2. **Référencer les specs quand nécessaire**
   - Pour les requirements: `spec.md`
   - Pour l'architecture: `plan.md`
   - Pour le schéma DB: `data-model.md`

3. **Mettre à jour `SESSION_RESUME.md` après chaque session**
   - Ajouter les nouveaux bugs résolus
   - Mettre à jour l'état des fonctionnalités
   - Noter les décisions techniques importantes

### ❌ À Éviter

1. ❌ Me demander "où en sommes-nous ?" sans me donner les fichiers à lire
2. ❌ Supposer qu'une fonctionnalité n'existe pas sans vérifier d'abord
3. ❌ Ignorer les notes critiques dans `data-model.md` (ex: `\n` line breaks)
4. ❌ Oublier de commit et push après des changements importants

---

## 🎬 Template de Message pour Nouvelle Session

```
Bonjour ! Nous travaillons sur le projet Baiboly - une application
de lecture de Bible et Fihirana (hymnes) en Malagasy.

Pour te mettre à jour:
1. Lis SESSION_RESUME.md (état actuel du projet)
2. Lis specs/001-bible-hymnal-reader/spec.md (spécifications)

Ensuite [décris ce que tu veux faire dans cette session].
```

---

## 📞 Commandes Rapides

### Redémarrer l'application
```bash
cd C:\Dev\baiboly
docker-compose restart
```

### Voir les logs
```bash
docker-compose logs -f frontend
docker-compose logs -f backend
```

### Accéder à la base de données
```bash
docker-compose exec backend python
>>> from src.app import create_app, db
>>> app = create_app()
>>> with app.app_context():
...     # vos commandes SQL ici
```

### Ré-importer les données
```bash
# Fihirana
docker-compose exec backend python src/scripts/import_fihirana_json.py

# Bible (si script existe)
docker-compose exec backend python src/scripts/import_bible.py
```

---

**Dernière mise à jour:** 2025-11-19
**Prochaine action suggérée:** Vérifier l'état complet de la section Bible (frontend + backend)
