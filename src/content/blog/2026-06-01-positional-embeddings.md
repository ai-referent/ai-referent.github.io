---
title: "Les embeddings de position : de Vaswani à RoPE"
date: 2026-06-01
author: "AI Referent"
tags: [AIResearch, Transformers]
reading_time: 8
description: "Comment les Transformers encodent-ils la position des tokens ? De l'encodage sinusoïdal de Vaswani aux rotations de RoPE, un tour d'horizon de l'évolution des encodages positionnels."
excerpt: "De l'encodage sinusoïdal de Vaswani aux rotations de RoPE : comment la notion de distance relative a progressivement été intégrée — et formalisée — dans les mécanismes d'attention."
---

Les textes sont des séquences et l'ordre des mots contribue fortement au sens.

```
Il faut manger pour vivre
Il faut vivre pour manger

Pierre aime Julie
Julie aime Pierre
```

Il est donc important d'intégrer des informations de position dans la représentation vectorielle des mots (plus exactement, des tokens) que l'on fournit en entrée à un modèle d'IA. Cette information est notamment essentielle pour le bon fonctionnement du mécanisme d'attention qui ne peut pas travailler sur un *bag of words* sans structure.

Au début du traitement, le modèle associe à chaque token un vecteur initial (*token embedding*) extrait d'une table. Une approche naïve consiste à associer à chaque token embedding l'index de sa position dans la séquence. Dans l'exemple "Il faut manger pour vivre", on associe ainsi l'index $2$ (en numérotant à partir de $0$) au token "manger" — mais lors du traitement de "Il faut vivre pour manger" on associera ce même index $2$ au token "vivre". On voit déjà le côté arbitraire des positions absolues. Par exemple, dans un texte où "vivre pour manger" apparaît à deux endroits différents :

```
Il faut vivre pour manger oui vraiment vivre pour manger.
```

des patterns différents, par exemple $(3, 4)$ et $(8, 9)$, sont associés à un même phénomène linguistique local : l'important c'est que "manger" suit immédiatement "pour", c'est-à-dire la position *relative* des deux mots, et non leurs positions absolues individuelles. La conséquence est que le modèle risque d'associer certaines propriétés à des positions particulières alors qu'elles dépendent uniquement de la distance entre les mots.

Cette conséquence apparaît dans le calcul des similarités entre *query* $Q_q$ et *key* $K_p$ dans les modules d'attention. Avec des positions absolues, le score dépend de la position de $q$, de la position de $p$, et du contenu de $q$ et $p$ — rendant la généralisation difficile.

Pour résoudre ce problème, il faut que le score dépende non plus des positions $q$ et $p$ individuellement, mais de la distance $q-p$ entre les tokens. On va voir comment cette nécessité a été progressivement prise en compte : implicitement chez Vaswani, puis explicitement avec RoPE.

---

## Prise en compte implicite : Vaswani et al. (2017)

Dans le [modèle Transformer original](https://arxiv.org/abs/1706.03762), pour un token en position $p$, le vecteur d'entrée est $x_p = c_p + \mathrm{PE}(p)$ où $c_p$ est l'embedding de contenu et $\mathrm{PE}(p)$ un encodage de position trigonométrique. À titre d'exemple, voici une matrice pour trois tokens et quatre dimensions :

$$\omega_i = 10000^{-2i/d_{\mathrm{model}}}$$

$$
PE=
\begin{bmatrix}
\sin(\omega_0 p_0) & \cos(\omega_0 p_0) & \sin(\omega_1 p_0) & \cos(\omega_1 p_0) \\
\sin(\omega_0 p_1) & \cos(\omega_0 p_1) & \sin(\omega_1 p_1) & \cos(\omega_1 p_1) \\
\sin(\omega_0 p_2) & \cos(\omega_0 p_2) & \sin(\omega_1 p_2) & \cos(\omega_1 p_2)
\end{bmatrix}
$$

Les dimensions sont organisées en paires sinus/cosinus, chaque fréquence occupant 2 dimensions (dimensions $0$–$1$ pour $\omega_0$, dimensions $2$–$3$ pour $\omega_1$, etc.). Le vecteur de position d'un token $p$ est donc :

$$\mathrm{PE}(p) = \big[\sin(\omega_0 p),\, \cos(\omega_0 p),\, \sin(\omega_1 p),\, \cos(\omega_1 p),\, \ldots\big]$$

Si on compare deux positions $p$ et $q$ sur une seule fréquence $\omega_k$, le produit scalaire vaut :

$$\mathbf{v}_k(p)\cdot \mathbf{v}_k(q) = \cos(\omega_k p)\cos(\omega_k q) + \sin(\omega_k p)\sin(\omega_k q) = \cos(\omega_k(q-p))$$

Le produit scalaire global entre deux encodages est alors $\sum_{k} \cos(\omega_k(q-p))$ : **il dépend uniquement de la différence $q-p$**, formant une signature multi-échelle de la distance relative.

Malheureusement, cette belle propriété ne va pas être exploitée pleinement. Dans ces modèles, les embeddings positionnels sont ajoutés aux embeddings de contenu puis projetés, et le score d'attention entre une *query* $q$ et une *key* $p$ se décompose en quatre termes :

$$
\begin{aligned}
Q_q \cdot K_p
&= \big(e_q + \mathrm{PE}(q)\big) W_Q \cdot \big(e_p + \mathrm{PE}(p)\big) W_K \\
&= \underbrace{e_q^\top W_Q W_K^\top e_p}_{\text{contenu–contenu}}
+ \underbrace{e_q^\top W_Q W_K^\top \mathrm{PE}(p)}_{\text{contenu–position}}
+ \underbrace{\mathrm{PE}(q)^\top W_Q W_K^\top e_p}_{\text{position–contenu}}
+ \underbrace{\mathrm{PE}(q)^\top W_Q W_K^\top \mathrm{PE}(p)}_{\text{position–position}}
\end{aligned}
$$

Le dernier terme encode bien les interactions position-position, mais les deux termes du milieu mélangent contenu et position. **La dépendance à la distance relative est partiellement masquée par ces termes croisés.**

---

## Prise en compte explicite : RoPE (2021)

Pour remédier à cela, les auteurs de [RoPE](https://arxiv.org/abs/2104.09864) ont adopté une démarche différente : au lieu d'imposer une représentation et d'observer ses propriétés, ils ont d'abord défini la propriété désirée, puis construit la représentation en conséquence.

Cette propriété est exprimée par une contrainte fonctionnelle sur le score d'attention :

$$\langle f_q(x_q, q),\, f_k(x_p, p) \rangle = G(x_q, x_p, q - p)$$

La signature de $G$ garantit que le score dépend du contenu sémantique des tokens **et** de leur distance relative $q-p$ — rien d'autre.

Les auteurs ont déterminé une représentation satisfaisant cette contrainte :

$$f_q(x_q,q) = \Big(h^{(0)} e^{i q \theta_0},\; h^{(1)} e^{i q \theta_1},\; \ldots,\; h^{(K-1)} e^{i q \theta_{K-1}}\Big)$$

$$f_k(x_p,p) = \Big(g^{(0)} e^{i p \theta_0},\; g^{(1)} e^{i p \theta_1},\; \ldots,\; g^{(K-1)} e^{i p \theta_{K-1}}\Big)$$

où $h^{(k)}$ (resp. $g^{(k)}$) est une paire de dimensions du vecteur de contenu projeté de la *query* (resp. de la *key*). Comme chez Vaswani, on regroupe les dimensions par paires — mais ici ce sont les dimensions du vecteur de **contenu** (et non du vecteur de position). Chaque facteur $e^{ip\theta_k}$ représente une rotation appliquée à la paire correspondante, via une matrice bloc-diagonale :

$$
\mathrm{RoPE}(x,p)
=
\begin{bmatrix}
R_0(p) & & \\
& \ddots & \\
& & R_{K-1}(p)
\end{bmatrix}
W x
\qquad \text{où} \quad
R_k(p) =
\begin{pmatrix}
\cos(\theta_k p) & -\sin(\theta_k p) \\
\sin(\theta_k p) & \cos(\theta_k p)
\end{pmatrix}
$$

Le produit scalaire de ces représentations vaut :

$$
\langle f_q, f_k \rangle
= \sum_{k=0}^{K-1} h^{(k)} e^{i q \theta_k} \cdot \overline{g^{(k)} e^{i p \theta_k}}
= \sum_{k} h^{(k)} \overline{g^{(k)}} \cdot e^{i(q-p)\theta_k}
$$

**Le produit scalaire se factorise naturellement en un terme de contenu $h^{(k)}\overline{g^{(k)}}$ et un terme de position $e^{i(q-p)\theta_k}$.** La contrainte est satisfaite par construction, et non par espoir.

---

## Conclusion

| | **Vaswani (2017)** | **RoPE (2021)** |
|---|---|---|
| **Démarche** | Représentation imposée a priori ; propriétés observées a posteriori | Propriété cible définie a priori ; représentation construite en conséquence |
| **Injection de la position** | Addition au vecteur de contenu : $x_p = e_p + \mathrm{PE}(p)$ | Rotation du vecteur de contenu : $\mathrm{RoPE}(x,p) = R(p)\,Wx$ |
| **Dépendance à $q-p$** | Implicite, masquée par les termes croisés contenu-position | Algébrique, garantie par construction |

RoPE n'a pas découvert la notion de distance relative — elle était déjà présente implicitement dans les encodages sinusoïdaux de Vaswani. Mais il l'utilise **explicitement et formellement** dans le produit scalaire d'attention, là où Vaswani la laissait apparaître sans garantie.

La représentation RoPE a d'autres avantages importants (*long term decay*, gestion de contextes longs…) — ce sera pour une prochaine fois !
