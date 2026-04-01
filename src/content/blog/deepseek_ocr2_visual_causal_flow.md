---
title: "DeepSeek-OCR 2 et la notion de Visual Causal Flow"
date: 2026-03-15
author: "AI Referent"
tags: [EmergentAI, AIResearch]
reading_time: 3
description: "DeepSeek-OCR 2 introduit une architecture encodeur–décodeur originale où des tokens supplémentaires construisent progressivement des abstractions sémantiques visuelles grâce à un mécanisme de causal flow."
excerpt: "DeepSeek-OCR 2 n'est pas qu'un nouveau modèle vision–langage. Son encodeur produit une représentation sémantique ordonnée de l'image — et comprendre pourquoi éclaire toute l'architecture."
---

## Une architecture encodeur–décodeur, mais pas comme les autres

[DeepSeek-OCR 2](
https://arxiv.org/abs/2601.20552) est un nouveau modèle encodeur–décodeur génératif, proche à première vue de modèles du type Flamingo ou BLIP-2 : un encodeur traduit une image en une séquence de tokens visuels et un décodeur génère de manière autorégressive, en étant conditionné par les tokens visuels à travers un mécanisme d'attention croisée.

Mais l'originalité tient à la qualité de la représentation du contenu visuel produite par l'encodeur.

---

## Le mécanisme clé : des tokens supplémentaires à flux causal

Lors de l'encodage, des tokens supplémentaires $q_i$ sont concaténés à la séquence de tokens visuels $v_i$. Ces tokens ont deux propriétés remarquables :

- **Ils ne sont pas dérivés de l'image** : leurs embeddings sont initialisés de manière aléatoire.
- **Ils forment leur représentation en respectant un masque causal** : chaque $q_i$ peut considérer tous les tokens visuels, mais seulement les tokens supplémentaires qui le précèdent $q_1 \to q_2 \to \cdots \to q_{i-1}$.

---

## Ce que ce causal flow induit

Ce mécanisme — d'où le titre de l'article — induit un **graphe de dépendances** entre les $q_i$ et les abstractions sémantiques qu'ils construisent :

→ Les premiers $q_i$ construisent des représentations de **bas niveau**, faciles à extraire directement de l'information visuelle brute.

→ Les $q_i$ situés plus loin dans la séquence construisent des informations de **haut niveau**, en s'appuyant sur les abstractions déjà formées.

L'encodeur peut ainsi offrir au décodeur une **information sémantique et ordonnée** — en s'abstrayant de l'ordre rigide des tokens physiques.

---

## Pourquoi ce nom ?

Le titre complet est **DeepSeek-OCR 2 : Visual Causal Flow**. Vous savez maintenant pourquoi : le flux causal entre les tokens supplémentaires est le cœur de l'architecture, et c'est ce qui distingue cet encodeur d'un encodeur visuel classique.
