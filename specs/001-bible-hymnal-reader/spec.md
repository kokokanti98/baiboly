# Feature Specification: Plateforme Baiboly sy Fihirana

**Feature Branch**: `001-bible-hymnal-reader`
**Created**: 2025-11-18
**Status**: Draft
**Input**: User description: "je veux développer un site web fonctionnant en web et mobile responsive pour lire la bible et d'avoir aussi les paroles des chanson évangéliques luthérien et fjkm. Il va se diviser en 2 partie la bible ou y aura les paroles de Dieu avec nom, verset et une autre partie pour avoir les paroles chansons recherche avec le numéro ou une recherche par contient: - Bible : recherche de la bible par nom, verset ou bien par contient via recherche nom ou phrase - Fihirana : recherche les paroles des chansons via son numero ou bien par contient via recherche nom ou phrase"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Lecture et recherche de versets bibliques (Priority: P1)

Un utilisateur ouvre l'application pour lire la Bible en Malagasy. Il peut parcourir les livres de la Bible, naviguer vers un chapitre et verset spécifique, et lire le contenu complet. Il peut également effectuer une recherche par nom de livre, numéro de verset, ou rechercher un mot ou une phrase spécifique dans tout le texte biblique pour trouver rapidement des passages pertinents.

**Why this priority**: La fonctionnalité de lecture biblique est le cœur de l'application. C'est la fonctionnalité principale que les utilisateurs attendent d'une application Baiboly. Sans cette fonctionnalité, l'application ne remplit pas son objectif principal.

**Independent Test**: Peut être testé indépendamment en vérifiant qu'un utilisateur peut accéder à n'importe quel livre de la Bible, lire des versets, et effectuer des recherches basiques. Délivre une valeur immédiate en permettant la lecture complète de la Bible.

**Acceptance Scenarios**:

1. **Given** l'utilisateur est sur la page d'accueil Bible, **When** il sélectionne un livre (ex: "Genesisy"), **Then** la liste des chapitres de ce livre s'affiche
2. **Given** l'utilisateur a sélectionné un livre et un chapitre, **When** il sélectionne le chapitre 1, **Then** tous les versets du chapitre 1 s'affichent en Malagasy
3. **Given** l'utilisateur est sur la page de recherche Bible, **When** il tape "Genesisy 1:1", **Then** le système affiche le verset Genesisy 1:1
4. **Given** l'utilisateur est sur la page de recherche Bible, **When** il tape un mot comme "fitiavana" (amour), **Then** le système affiche tous les versets contenant ce mot avec les références (livre, chapitre, verset)
5. **Given** l'utilisateur lit un passage, **When** il fait défiler la page, **Then** le système maintient le contexte (livre, chapitre actuel visible)

---

### User Story 2 - Lecture et recherche des chants évangéliques (Priority: P2)

Un utilisateur accède à la section Fihirana pour consulter les paroles des chants évangéliques luthériens et FJKM. Il peut rechercher un chant par son numéro dans l'hymnaire ou effectuer une recherche par contenu (titre du chant ou mots-clés dans les paroles). Une fois le chant trouvé, il peut lire les paroles complètes en Malagasy.

**Why this priority**: La section Fihirana est la deuxième fonctionnalité principale de l'application et complète l'expérience spirituelle des utilisateurs. Elle est indépendante de la Bible et apporte une valeur distincte.

**Independent Test**: Peut être testé indépendamment en vérifiant qu'un utilisateur peut rechercher des chants par numéro ou contenu, et afficher les paroles complètes. Délivre une valeur immédiate en donnant accès à l'hymnaire complet.

**Acceptance Scenarios**:

1. **Given** l'utilisateur est sur la page Fihirana, **When** il entre un numéro de chant (ex: "125"), **Then** le système affiche le chant numéro 125 avec son titre et ses paroles complètes
2. **Given** l'utilisateur est sur la page de recherche Fihirana, **When** il tape un titre ou un mot des paroles (ex: "Jesosy"), **Then** le système affiche la liste des chants contenant ce mot avec leur numéro et titre
3. **Given** l'utilisateur consulte les résultats de recherche, **When** il clique sur un chant dans la liste, **Then** le système affiche les paroles complètes du chant
4. **Given** l'utilisateur lit les paroles d'un chant, **When** il visualise la page sur mobile, **Then** les paroles s'affichent de manière lisible et responsive
5. **Given** l'utilisateur lit un chant, **When** il veut revenir à la liste, **Then** le système permet une navigation facile retour

---

### User Story 3 - Navigation principale et expérience responsive (Priority: P3)

Un utilisateur accède à l'application depuis n'importe quel appareil (téléphone mobile, tablette, ou ordinateur de bureau) et navigue facilement entre les deux sections principales : Bible et Fihirana. L'interface s'adapte automatiquement à la taille de l'écran et offre une expérience utilisateur cohérente et intuitive en Malagasy.

**Why this priority**: L'expérience utilisateur et l'accessibilité multi-plateforme sont essentielles pour l'adoption de l'application, mais cette fonctionnalité est dépendante des deux premières histoires pour avoir de la valeur.

**Independent Test**: Peut être testé indépendamment en vérifiant que l'interface principale fonctionne correctement sur différents appareils (mobile 375px, tablette 768px, desktop 1024px+) et que la navigation entre sections est fluide.

**Acceptance Scenarios**:

1. **Given** l'utilisateur ouvre l'application sur un smartphone, **When** la page se charge, **Then** l'interface s'affiche correctement avec menu de navigation accessible
2. **Given** l'utilisateur est sur la page d'accueil, **When** il clique sur "Baiboly", **Then** il accède à la section Bible
3. **Given** l'utilisateur est sur la page d'accueil, **When** il clique sur "Fihirana", **Then** il accède à la section Fihirana
4. **Given** l'utilisateur est sur mobile (≤768px), **When** il navigue dans l'application, **Then** tous les boutons de navigation respectent la taille minimale de 44x44 pixels
5. **Given** l'utilisateur est sur tablette ou desktop, **When** il utilise l'application, **Then** l'interface utilise l'espace disponible de manière optimale

---

### Edge Cases

- Que se passe-t-il lorsque l'utilisateur recherche un verset avec une référence invalide (ex: "Genesisy 1:999" qui n'existe pas)?
- Comment le système gère-t-il une recherche par contenu qui ne retourne aucun résultat?
- Que se passe-t-il lorsque l'utilisateur entre un numéro de chant qui n'existe pas dans l'hymnaire?
- Comment le système affiche-t-il les résultats de recherche lorsqu'il y a plus de 100 résultats correspondants?
- Que se passe-t-il lorsque l'utilisateur fait une recherche avec des caractères spéciaux ou des accents?
- Comment le système se comporte-t-il lorsque la connexion internet est lente ou interrompue?

## Requirements *(mandatory)*

### Functional Requirements

**Section Bible**:

- **FR-001**: Le système DOIT afficher la liste complète des 66 livres de la Bible (39 Ancien Testament, 27 Nouveau Testament) en Malagasy
- **FR-002**: Le système DOIT permettre la navigation par livre, chapitre et verset avec une hiérarchie claire
- **FR-003**: Le système DOIT afficher les versets bibliques en texte Malagasy avec les références (livre, chapitre, numéro de verset)
- **FR-004**: Les utilisateurs DOIVENT pouvoir rechercher par référence exacte (ex: "Jaona 3:16" ou "Jean 3:16")
- **FR-005**: Les utilisateurs DOIVENT pouvoir rechercher par contenu (mot ou phrase) dans tout le texte biblique
- **FR-006**: Le système DOIT afficher les résultats de recherche avec le contexte (verset complet + référence)
- **FR-007**: Le système DOIT supporter les variations de noms de livres en français et en Malagasy (ex: "Jean" et "Jaona")

**Section Fihirana**:

- **FR-008**: Le système DOIT stocker et afficher les chants évangéliques luthériens et FJKM avec numéro, titre et paroles complètes
- **FR-009**: Les utilisateurs DOIVENT pouvoir rechercher un chant par son numéro
- **FR-010**: Les utilisateurs DOIVENT pouvoir rechercher un chant par contenu (titre ou paroles)
- **FR-011**: Le système DOIT afficher les résultats de recherche Fihirana avec numéro, titre et extrait
- **FR-012**: Le système DOIT afficher les paroles complètes d'un chant avec formatage approprié (strophes, refrains)

**Navigation et Interface**:

- **FR-013**: Le système DOIT fournir un menu de navigation permettant de basculer entre "Baiboly" et "Fihirana"
- **FR-014**: L'interface DOIT être responsive et fonctionnelle sur mobile (≥375px), tablette (≥768px) et desktop (≥1024px)
- **FR-015**: Toute l'interface utilisateur DOIT être en Malagasy (labels, boutons, messages)
- **FR-016**: Le système DOIT afficher des messages d'erreur clairs en Malagasy lorsqu'une recherche ne retourne aucun résultat
- **FR-017**: Le système DOIT maintenir l'état de navigation de l'utilisateur (position actuelle dans la Bible ou Fihirana)

**Performance et Expérience**:

- **FR-018**: Les recherches DOIVENT retourner des résultats en moins de 2 secondes pour une requête standard
- **FR-019**: Le système DOIT afficher un indicateur de chargement pour les opérations dépassant 500ms
- **FR-020**: Le système DOIT gérer les erreurs réseau de manière gracieuse avec messages en Malagasy

### Key Entities

- **Livre (Boky)**: Représente un livre de la Bible avec nom en Malagasy, nom en français, testament (Ancien/Nouveau), ordre, nombre de chapitres
- **Chapitre (Toko)**: Représente un chapitre d'un livre avec numéro, référence au livre parent, nombre de versets
- **Verset (Andininy)**: Représente un verset individuel avec numéro, texte en Malagasy, référence au chapitre parent, texte indexé pour recherche
- **Chant (Fihirana)**: Représente un chant évangélique avec numéro dans l'hymnaire, titre en Malagasy, paroles complètes, source (luthérien/FJKM), texte indexé pour recherche

### Data Sources

**Bible (Baiboly)**:
- Source: Repository GitHub `RaveloMevaSoavina/baiboly-json`
- Format: 66 fichiers JSON individuels (un par livre biblique)
- Structure:
  - Testameta taloha (Ancien Testament): 39 livres (genesisy.json, eksodosy.json, salamo.json, etc.)
  - Testameta vaovao (Nouveau Testament): 27 livres (matio.json, marka.json, lioka.json, jaona.json, etc.)
- Contenu: Texte complet de la Bible en langue Malagasy organisé par livre, chapitre et verset
- Licence: Open source, disponible publiquement

**Fihirana (Chants Évangéliques)**:
- Source: Repository GitHub `Rohan29-AN/Fihirana-FFPM`
- Format: 3 fichiers JSON avec script de génération SQL disponible
  - 01_fihirana_ffpm.json: Collection principale des chants FFPM (Fihirana Fjkm, Protestanta, Malagasy)
  - 02_fihirana_fanampiny.json: Supplément de chants additionnels
  - 03_antema.json: Section antiennes et répons
- Contenu: Numéros de chants, titres et paroles des chants luthériens et FJKM en Malagasy
- Note: Métadonnées partielles (compositeurs et titres complets en cours d'ajout par la communauté)
- Licence: Open source, disponible publiquement

### Assumptions

- Les données des repositories GitHub sont à jour, complètes et exactes
- Les deux repositories sont maintenus et disponibles pour usage dans ce projet
- Les utilisateurs auront une connexion internet pour la version web initiale
- Une version offline pourra être envisagée ultérieurement en stockant les données localement
- La structure JSON des fichiers sources est cohérente et peut être importée dans une base de données
- L'application cible principalement les locuteurs Malagasy à Madagascar et dans la diaspora

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Les utilisateurs peuvent trouver et lire n'importe quel verset de la Bible en moins de 30 secondes
- **SC-002**: Les recherches de contenu biblique retournent des résultats pertinents en moins de 2 secondes
- **SC-003**: Les utilisateurs peuvent trouver un chant par son numéro en moins de 10 secondes
- **SC-004**: 90% des utilisateurs complètent avec succès une recherche (Bible ou Fihirana) du premier coup
- **SC-005**: L'application fonctionne correctement sur au moins 95% des appareils mobiles modernes (Android 8+, iOS 13+)
- **SC-006**: L'interface est entièrement lisible et utilisable sur des écrans de 375px de largeur minimum
- **SC-007**: Le temps de chargement initial de l'application est inférieur à 3 secondes sur une connexion 3G
- **SC-008**: Les utilisateurs peuvent naviguer entre Bible et Fihirana avec une transition fluide (<1 seconde)