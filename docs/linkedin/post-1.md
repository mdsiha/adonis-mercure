# LinkedIn post #1 — adonis-mercure

Attach: `carrousel-linkedin-fr.pdf` (FR) or `carousel-linkedin-en.pdf` (EN) as a **document** (carousel).

---

## Version française

Votre application survit-elle à un service tiers lent ?

En construisant @mdsiha369/adonis-mercure (un package AdonisJS pour pousser du temps réel via Mercure / SSE), j'ai dû trancher 3 questions qui valent pour n'importe quel appel sortant :

1️⃣ Un timeout explicite (5 s par défaut). Sans lui, un service lent accumule des requêtes en attente et fait exploser la latence p99.

2️⃣ Des erreurs typées (Timeout, Connection, Publish). L'appelant décide quoi faire sans parser de texte, et brancher un retry devient simple.

3️⃣ Fail-fast au démarrage… mais sans ping du hub. Une config invalide est un bug à détecter au déploiement. Un hub en panne est un incident d'exploitation qui ne doit pas bloquer mes déploiements.

Limites assumées : pas de retry ni de métriques pour l'instant. Prochaine étape : backoff + jitter sur les erreurs transitoires uniquement, puis un circuit breaker.

Et vous : un timeout par défaut dans vos clients HTTP, oui ou non ? 👇

Carrousel en pièce jointe (5 slides).

#NodeJS #TypeScript #AdonisJS #BackendEngineering #SystemDesign

**Premier commentaire (liens) :**
npm : https://www.npmjs.com/package/@mdsiha369/adonis-mercure
GitHub : https://github.com/mdsiha/adonis-mercure

---

## English version

Would your app survive a slow third-party service?

While building @mdsiha369/adonis-mercure (an AdonisJS package that pushes real-time updates through Mercure / SSE), I had to settle 3 questions that apply to any outbound call:

1️⃣ An explicit timeout (5 s by default). Without it, a slow service piles up pending requests and blows up p99 latency.

2️⃣ Typed errors (Timeout, Connection, Publish). The caller decides what to do without parsing text, and plugging in a retry becomes easy.

3️⃣ Fail-fast at startup… but no hub ping. An invalid config is a bug to catch at deploy time. A hub outage is an operational incident that must not block my deployments.

Known limits: no retry and no metrics yet. Next step: backoff + jitter on transient errors only, then a circuit breaker.

What about you: a default timeout in your HTTP clients, yes or no? 👇

Carousel attached (5 slides).

#NodeJS #TypeScript #AdonisJS #BackendEngineering #SystemDesign

**First comment (links):**
npm: https://www.npmjs.com/package/@mdsiha369/adonis-mercure
GitHub: https://github.com/mdsiha/adonis-mercure
