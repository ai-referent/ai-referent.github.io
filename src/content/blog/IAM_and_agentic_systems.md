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

La majorité des attaques cyber ne passent pas par des failles techniques sophistiquées. Elles exploitent des identités mal gouvernées : un credential volé et jamais révoqué, un compte avec des droits au-delà de ce qu'il devrait avoir, une permission accordée pour dépanner en urgence et oubliée depuis. En résumé, des identités dont le cycle de vie (création, droits, révision, suppression) n'est pas maîtrisé. L'identité est définie ici comme une entité dotée d'un identifiant, pouvant s'authentifier et recevoir des autorisations.

Ce problème des identités mal gérées est déjà bien présent. Début 2026,  89 % des décideurs IT et sécurité considèrent les attaques liées à l’identité comme la principale menace cyber, et que les compromissions d’identités sont devenues le point d’entrée dominant des attaques  (Source : [les attaques liées à l’identité : la principale menace cyber selon Rubrik](https://decideur-it.fr/89-des-dirigeants-francais-considerent-les-attaques-liees-a-lidentite-comme-la-principale-menace-cyber-selon-rubrik/). Le phénomène risque de prendre encore plus d'ampleur avec des systèmes agentiques où des identités non-humaines (*Non-Human Identity* ou NHI) , sont créées en masse. Chaque agent est une identité. Chaque *service account* qu'il utilise est une identité. . Et ces identités prolifèrent à une vitesse et dans des volumes inédits jusqu'à maintenant.

Déployer des agents sans réponse claire à la question de la gouvernance des NHI, c'est aggraver structurellement la surface d'attaque.

---

## Les NHI dans un contexte agentique

Une NHI classique — un *service account*, un client OAuth2 — est statique : elle est créée, elle tourne, elle est (rarement) révoquée. On sait à peu près ce qu'elle fait.

Les NHI agentiques sont d'une nature différente, et c'est là que la difficulté commence.

Un agent IA n'est pas un processus déterministe qui exécute toujours la même séquence d'actions. Il raisonne, planifie, et décide quels outils appeler en fonction du contexte. Concrètement, cela produit plusieurs types de NHI imbriquées :

→ L'agent lui-même a une identité pour s'authentifier auprès des systèmes qu'il orchestre.  
→ Les outils qu'il appelle (APIs tierces, bases de données, services cloud) ont chacun leurs propres credentials, souvent injectés au moment de l'exécution.  
→ Les sous-agents qu'il peut instancier dynamiquement héritent ou délèguent des droits, parfois sans traçabilité claire de la chaîne d'origine.  
→ Les sessions et tokens générés à la volée ont des durées de vie variables, parfois longues, parfois réutilisés entre tâches.

Ces imbrications reflètent cinq propriétés fondamentales des agents : ils sont **multiples**, **éphémères**, **rapides**, **non-déterministes** et **autonomes**. C'est précisément ces propriétés qui rendent la gouvernance des NHI agentiques difficile à assurer avec les méthodes IAM traditionnelles.

---

## 🔍 Pourquoi les méthodes IAM traditionnelles ne suivent pas

Les agents ne sont pas de simples NHI en plus grand nombre. Ils ont des propriétés qui mettent structurellement en difficulté les concepts et protocoles sur lesquels repose l'IAM (*Identity Access Management*) traditionnel. Le tableau ci-dessous met en regard les caractéristiques des agents et les aspects de l'IAM impactés par ces caractéristiques.

<div style="overflow-x:auto;">
<table class="iam-table">
  <thead>
    <tr>
      <th>Propriété</th>
      <th>Conséquence</th>
      <th>Aspects IAM mis en difficulté</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="prop-cell group-multiples">Multiples</td>
      <td class="group-multiples">Volume massif de nouvelles identités à provisionner</td>
      <td class="group-multiples">Provisionnement (SCIM, workflows IGA)</td>
    </tr>
    <tr>
      <td class="prop-cell group-multiples-eph">Multiples +&nbsp;Éphémères</td>
      <td class="group-multiples-eph">Volume massif de credentials à émettre, rotation et révocation à grande échelle</td>
      <td class="group-multiples-eph">Gestion des credentials et secrets (PKI, gestionnaires de secrets)</td>
    </tr>
    <tr>
      <td class="prop-cell group-ephemeres">Éphémères</td>
      <td class="group-ephemeres">Identités disparaissant avant toute révision possible</td>
      <td class="group-ephemeres">Recertification, access reviews (IGA)</td>
    </tr>
    <tr>
      <td class="prop-cell group-rapides">Rapides</td>
      <td class="group-rapides">Centaines de sessions et appels ouverts/fermés en quelques minutes</td>
      <td class="group-rapides">Gestion des sessions, JIT access</td>
    </tr>
    <tr>
      <td class="prop-cell group-nondetermin" rowspan="2">Non-déterministes</td>
      <td class="group-nondetermin">Comportement légitime variable d'une exécution à l'autre</td>
      <td class="group-nondetermin">Détection comportementale (UEBA, ITDR) — baseline comportementale structurellement difficile à établir</td>
    </tr>
    <tr>
      <td class="group-nondetermin">Séquence d'appels et chemins d'exécution variables et opaques</td>
      <td class="group-nondetermin">Journalisation et traçabilité des accès</td>
    </tr>
    <tr>
      <td class="prop-cell group-autonomes" rowspan="4">Autonomes</td>
      <td class="group-autonomes">Aucun principal humain identifiable derrière l'agent, aucune interaction humaine dans la boucle d'authentification</td>
      <td class="group-autonomes">Authentification et fédération d'identité (SAML, OIDC) — conçus autour d'un humain qui consent et s'authentifie</td>
    </tr>
    <tr>
      <td class="group-autonomes">Accès à des ressources non anticipées a priori</td>
      <td class="group-autonomes">Contrôle d'accès aux ressources (RBAC, ABAC, least privilege)</td>
    </tr>
    <tr>
      <td class="group-autonomes">Actions non anticipées initiées par l'agent (écriture, envoi, appel externe…)</td>
      <td class="group-autonomes">Politiques d'autorisation des actions — supposent qu'on peut énumérer l'espace des actions possibles</td>
    </tr>
    <tr>
      <td class="group-autonomes">Délégation dynamique à des sous-agents avec transfert de droits</td>
      <td class="group-autonomes">Délégation d'accès (OAuth 2.0), séparation des tâches (SoD)</td>
    </tr>
  </tbody>
</table>
</div>

Ce tableau montre que les méthodes traditionnelles ne sont pas simplement sous-dimensionnées — elles reposent sur des hypothèses (un humain dans la boucle, un périmètre d'accès définissable à l'avance, un comportement suffisamment stable pour établir une baseline) que les agents invalident structurellement.

La question n'est donc pas seulement "comment adapter l'IAM aux agents ?" mais "quelles nouvelles primitives faut-il construire ?"
