---
title: "Apprentissage à la volée sur les longues séquences : le Test-Time Training en pratique"
date: 2026-03-10
author: "AI Referent"
tags: [EmergentAI, AIResearch]
reading_time: 3
description: "Et si le modèle s'adaptait à la volée au contenu de sa fenêtre de contexte ? C'est la promesse du Test-Time Training appliqué aux longues séquences — une idée dont l'originalité tient moins à la technique qu'au contexte d'application."
excerpt: "Adapter le modèle token par token à ce qu'il lit : l'idée est audacieuse. La réalité technique est plus nuancée"
---

Parmi les tendances récentes pour mieux prendre en compte les fenêtres de contexte : ne pas seulement prendre connaissance des tokens de la fenêtre mais les utiliser pour adapter le modèle à la volée.

C'est ce que propose [End-to-End Test-Time Training for Long Context](
https://arxiv.org/pdf/2512.23675).

Ce qui paraît séduisant de prime abord dans ce papier c'est qu'ils font de l'apprentissage en ligne (*online training*) au niveau de chaque token d'une séquence, donc pas d'une séquence individuelle à une autre. Ca revient à traiter chaque token comme un data point, avec donc une mise à jour des poids pour chaque token traité.

Mais une estimation de gradient sur un seul token c'est fragile et coûteux ! Les auteurs proposent donc finalement de faire du batching. La séquence est divisée en sous-séquences. Pour chaque sous-séquence, la fonction de perte est calculée comme une moyenne sur les tokens et c'est ce coût qui est utilisé pour mettre à jour le modèle. Mais on arrive là à de l'apprentissage standard avec un batch de taille $1$, où la perte est également moyennée sur les tokens avant une mise à jour !

L'originalité du papier tient donc moins à la technique qu'au contexte (sans jeu de mots !) d'utilisation : adapter le modèle à des séquences reçues via sa fenêtre de contexte.
