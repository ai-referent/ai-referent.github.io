---
title: "Self-hosted sandbox : la sécurisation de l'exécution ne garantit pas la souveraineté des données"
date: 2026-06-09
author: "AI Referent"
tags: [AgentIA, Anthropic, Souveraineté, Sécurité]
reading_time: 3
description: "Anthropic propose une self-hosted sandbox pour Claude Managed Agents : les outils s'exécutent localement, mais les données métier quittent quand même l'entreprise."
excerpt: "La sécurisation de l'environnement d'exécution ne garantit pas la souveraineté des données. Analyse de l'architecture self-hosted sandbox d'Anthropic et de ses limites."
---

Anthropic propose depuis quelques mois *Claude Managed Agents*, une infrastructure complète pour exécuter des agents IA : orchestration des tâches, gestion de contexte, exécution d'outils, traçabilité, etc. Initialement, tout s'exécutait dans l'infrastructure d'Anthropic mais une nouvelle fonctionnalité a été ajoutée récemment (**self-hosted sandbox**), qui permet schématiquement aux outils et au code de s'exécuter dans une sandbox locale (l'orchestration restant hébergée chez Anthropic).

La promesse de cette **self-hosted sandbox** est de limiter l'exposition des données et ressources métier de l'entreprise. Mais cette atténuation des risques n'est que très partielle puisque, même si les outils s'exécutent localement, l'agent doit quand même transmettre au modèle les résultats des appels aux outils donc par exemple, des résultats de requêtes, etc. Des informations potentiellement sensibles doivent donc toujours quitter l'environnement de l'entreprise en direction de l'infrastructure du fournisseur du modèle.

L'environnement d'exécution est protégé mais le risque de fuite de données demeure. J'ai résumé l'architecture dans le schéma joint, sur lequel je travaille pour préparer un cours : dans ce schéma c'est la flèche « tool_result » horizontale qui correspond au problème.

Pour être complet, Anthropic a aussi introduit la notion de *MCP tunnels*, que j'ajouterai au schéma, mais ça ne change rien au fait que **La sécurisation de l'exécution ne garantit pas la souveraineté des données**.
