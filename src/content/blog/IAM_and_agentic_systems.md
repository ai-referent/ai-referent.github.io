---
title: "Les agents IA et la gouvernance des identités : les méthodes IAM traditionnelles sont-elles à la hauteur ?"
date: 2026-03-29
author: "AI Referent"
tags: [IAM, Agentic systems]
reading_time: 4
description: "L'IAM a été conçu pour des humains. Les agents ne le sont pas. Et donc..."
excerpt: "L'IAM a été conçu pour des humains. Les agents ne le sont pas. Et donc..."
---


## L'identité mal gouvernée, premier vecteur d'attaque

La majorité des attaques cyber ne passent pas par des failles techniques sophistiquées. Elles exploitent des identités mal gouvernées : un credential volé et jamais révoqué, un compte avec des droits au-delà de ce qu'il devrait avoir, une permission accordée pour dépanner en urgence et oubliée depuis. En résumé, des identités dont le cycle de vie (création, droits, révision, suppression) n'est pas maîtrisé.

Ce problème risque de prendre encore de l'ampleur avec des systèmes agentiques où des identités non-humaines (NHI) sont créées en masse. Chaque agent est une identité. Chaque service account qu'il utilise est une identité. Chaque clé API qu'il consomme est une identité. Et ces identités prolifèrent à une vitesse et dans des volumes inédits jusqu'à maintenant.

Déployer des agents sans réponse claire à la question de la gouvernance des NHI, c'est aggraver structurellement la surface d'attaque.

---

## Les NHI dans un contexte agentique

Une NHI classique — un service account applicatif, une clé API d'intégration — est statique : elle est créée, elle tourne, elle est (rarement) révoquée. On sait à peu près ce qu'elle fait.

Les NHI agentiques sont d'une nature différente, et c'est là que la difficulté commence.

Un agent IA n'est pas un processus déterministe qui exécute toujours la même séquence d'actions. Il raisonne, planifie, et décide quels outils appeler en fonction du contexte. Concrètement, cela produit plusieurs types de NHI imbriquées :

→ L'agent lui-même a une identité pour s'authentifier auprès des systèmes qu'il orchestre.  
→ Les outils qu'il appelle (APIs tierces, bases de données, services cloud) ont chacun leurs propres credentials, souvent injectés au moment de l'exécution.  
→ Les sous-agents qu'il peut instancier dynamiquement héritent ou délèguent des droits, parfois sans traçabilité claire de la chaîne d'origine.  
→ Les sessions et tokens générés à la volée ont des durées de vie variables, parfois longues, parfois réutilisés entre tâches.

Ces imbrications reflètent cinq propriétés fondamentales des agents : ils sont **multiples**, **éphémères**, **rapides**, **non-déterministes** et **autonomes**. C'est précisément ces propriétés qui rendent la gouvernance des NHI agentiques difficile à assurer avec les méthodes IAM traditionnelles.

---

## 🔍 Pourquoi les méthodes IAM traditionnelles ne suivent pas

Les agents ne sont pas de simples NHI en plus grand nombre. Ils ont des propriétés qui mettent structurellement en difficulté les concepts et protocoles sur lesquels repose l'IAM traditionnel.

| Propriété | Conséquence | Aspects IAM mis en difficulté |
|---|---|---|
| Multiples | Volume massif de nouvelles identités à provisionner | Provisionnement (SCIM, workflows IGA) |
| Multiples + Éphémères | Volume massif de credentials à émettre, rotation et révocation à grande échelle | Gestion des credentials et secrets (PKI, gestionnaires de secrets) |
| Éphémères | Identités disparaissant avant toute révision possible | Recertification, access reviews (IGA) |
| Rapides | Centaines de sessions et appels ouverts/fermés en quelques minutes | Gestion des sessions, JIT access |
| Non-déterministes | Comportement légitime variable d'une exécution à l'autre | Détection comportementale (UEBA, ITDR) — baseline comportementale structurellement difficile à établir |
| Non-déterministes | Séquence d'appels et chemins d'exécution variables et opaques | Journalisation et traçabilité des accès |
| Autonomes | Aucun principal humain identifiable derrière l'agent, aucune interaction humaine dans la boucle d'authentification | Authentification et fédération d'identité (SAML, OIDC) — conçus autour d'un humain qui consent et s'authentifie |
| Autonomes | Accès à des ressources non anticipées a priori | Contrôle d'accès aux ressources (RBAC, ABAC, least privilege) |
| Autonomes | Actions non anticipées initiées par l'agent (écriture, envoi, appel externe…) | Politiques d'autorisation des actions — supposent qu'on peut énumérer l'espace des actions possibles |
| Autonomes | Délégation dynamique à des sous-agents avec transfert de droits | Délégation d'accès (OAuth 2.0), séparation des tâches (SoD) |

Ce tableau montre que les méthodes traditionnelles ne sont pas simplement sous-dimensionnées — elles reposent sur des hypothèses (un humain dans la boucle, un périmètre d'accès définissable à l'avance, un comportement suffisamment stable pour établir une baseline) que les agents invalident structurellement.

La question n'est donc pas seulement "comment adapter l'IAM aux agents ?" mais "quelles nouvelles primitives faut-il construire ?"
