---
title: "Les embeddings de position : de Vaswani à RoPE"
date: 2026-06-01
author: "AI Referent"
tags: [AIResearch, Transformers]
reading_time: 8
description: "Comment les Transformers encodent-ils la position des tokens ? De l'encodage sinusoïdal de Vaswani aux rotations de RoPE, un tour d'horizon de l'évolution des encodages positionnels."
excerpt: "De l'encodage sinusoïdal de Vaswani aux rotations de RoPE : comment la notion de distance relative a progressivement été intégrée — et formalisée — dans les mécanismes d'attention."
---

## Introduction

Les textes sont des séquences et l'ordre des mots contribue fortement au sens.

```
Il faut manger pour vivre
Il faut vivre pour manger

Pierre aime Julie
Julie aime Pierre
```

Il est donc important d'intégrer  des informations de position dans la représentation vectorielle  des mots (plus exactement, des tokens) que l'on fournit en entrée à un modèle d'IA. Cette information est notamment essentielle pour le bon fonctionnement du mécanisme d'attention qui ne peut pas travailler sur un "sac de mots" (*ag of words*) sans structure.

Au début du traitement, le modèle d'IA va associer à chaque token un vecteur initial (ce vecteur est un un token embedding) extrait d'une table associant un embedding à chaque token. Une approche naïve peut consister à associer à chaque token embedding l'index de la position dans la séquence. Ca semble raisonnable puisqu'on a ainsi noté où se trouve chaque token dans la séquence. Dans l'exemple "Il faut manger pour vivre", on peut ainsi associer l'index $2$ (en numérotant à partir de $0$) au token "manger", mais on remarque aussi que lors du traitement de "Il faut vivre pour manger" on associera l'index $2$ au token "vivre". On voit déjà le côté arbitraire des positions "absolues". Par exemple, dans un texte ou "vivre pour manger" serait répété à deux endroits différents  :

```
Il faut vivre pour manger oui  vraiment vivre pour manger.
```

des patterns différents, par exemple  (3, 4) et (8, 9) sont associés à un même phénomène, un groupe prépositionnel à l'infinitif liant la même préposition au même verbe. On va aisni créer une distinction artifiicelle entre les représentations des deux occurrences de "pour" et"manger"   alors que ces occurrences participent à un même phénomène linguistique local : l'important c'est le fait que "manger" suit immédiatement "pour", c'est-à-dire la position "relative" des deux mots et non leurs positions absolues individuelles. A l'extrême, on voit que si on décale toute la phrase de quelques positions, même si le contenu linguistique reste à peu près  inchangé, la représentation interne deviendra très différente. La conséquence est que le modèle risque d'associer certaines propriétés à des positions particulières alors qu'elles dépendent en réalité uniquement de la distance entre les mots.

Cette conséquence apparaît quand on calcule les similarités entre *query* $Q_p$ et une *key* $K_q$ dans les modules d'attention. Si on inclut l'information de position sous forme d'indices absolus, le score devient alors dépendant de :

- position of $p$
- position of $q$
- le contenu de $p$ et $q$

Des structures locales similaires étant représentées de façon différentes en fonction de leur indexation absolue, le modèle aura beaucoup de mal à généraliser de manière efficace.

Pour résoudre ce problème, il faut que le score ne soit plus dépendant des positions $p$ et $q$ pris individuellement mais de la distance $q-p$ entre les tokens. Dans la suite on va voir comment cette nécessité a été progressivement prise en compte au fur et à mesure de l'évolution des modèles Transformer. En effet, on va voir que dans les premiers modèles Transformer on utilise certes une approximation implicite de la structure relative, mais pas un mécanisme intrinsèquement relatif. Cette limite a été corrigée dans des modèles plus récents (RoPE, ALiBi, etc.) où la dépendance relative  a été prise plus directement en compte dans le score d'attention lui-même.

---

## Prise en compte implicite des distances relatives dans l'architecture de Vaswani et al. (2017)

Dans le modèle Transformer original de [Vaswani et al.](https://arxiv.org/abs/1706.03762), pour un token en position $p$, le vecteur d'entrée est : $x_p = c_p + \mathrm{pos}(p)$ où $c_p$ est l'embedding de contenu (extrait de la matrice d'embedding du modèle) et $\mathrm{pos}(p)$ est un embedding de position déterminé par une formule trigonométrique. A titre d'exemple, voici une matrcie pour trois tokens et quatre dimensions :

$$\omega_i = 10000^{-2i/d_{\mathrm{model}}}$$

$$
PE=
\begin{bmatrix}
\sin(\omega_0 p_0) & \cos(\omega_0 p_0) &
\sin(\omega_1 p_0) & \cos(\omega_1 p_0) \\
\\
\sin(\omega_0 p_1) & \cos(\omega_0 p_1) &
\sin(\omega_1 p_1) & \cos(\omega_1 p_1) \\
\\
\sin(\omega_0 p_2) & \cos(\omega_0 p_2) &
\sin(\omega_1 p_2) & \cos(\omega_1 p_2)
\end{bmatrix}
$$

$$\underbrace{\hspace{3cm}}_{\text{paire associée à }\omega_0} \qquad \underbrace{\hspace{3cm}}_{\text{paire associée à }\omega_1}$$

On peut faire deux remarques. la première, moins importante pour notre exposé, mais intéressant quand même à noter est que les arguments des sinus et cosinus peuvent être vus comme des phases instantanées $\omega_i t$, où $t = \mathrm{pos}$ et $\omega_i = 10000^{-2i/d_{\mathrm{model}}}$ est une pulsation associée à chaque dimension.

**Mais le plus important à noter** est que, comme suggéré par les accolades horizontales, les 4 dimensions sont organisées comme 2 paires sinus/cosinus, avec chaque fréquence chaque fréquence occupant 2 dimensions :

- dimensions $0$-$1 \Rightarrow \omega_0$
- dimensions $2$-$3 \Rightarrow \omega_1$

Donc le vecteur de position d'un token $p$ est :

$$\mathrm{PE}(p) = \big[\sin(\omega_0 p), \cos(\omega_0 p), \sin(\omega_1 p), \cos(\omega_1 p), \ldots\big]$$

Le vecteur de position est structuré en sous-vecteurs 2D, un par fréquence. Si on compare deux positions $p$ et $q$, sur une seule fréquence $\omega_k$, le produit scalaire vaut :

$$
\begin{aligned}
\mathbf{v}_k(p)\cdot \mathbf{v}_k(q)
&= \cos(\omega_k p)\cos(\omega_k q) + \sin(\omega_k p)\sin(\omega_k q) \\
&= \cos(\omega_k(q-p))
\end{aligned}
$$

Le produit scalaire global entre deux encodings est alors :

$$\mathrm{PE}(p)\cdot \mathrm{PE}(q) = \sum_{k=0}^{K-1} \mathbf{v}_k(p)\cdot \mathbf{v}_k(q)$$

Au final, avec la représentation sinusoidale proposée par Vaswani, **le produit scalaire entre deux encodages positionnels dépend uniquement de la différence $q-p$ et s'exprime comme une somme de cosinus à différentes fréquences, formant une signature multi-échelle de la distance relative**.

Malheureusement, cette dépendance claire à $q-p$ ne va pas être exploitée pleinement par les mécanismes d'attention des premiers modèles Transformer. En effet, dans ces modèles, les embeddings positionnels sont ajoutés aux embeddings de contenu :

$$x_p = e_p + \mathrm{PE}(p)$$

puis projetés :

$$Q = xW_Q,\quad K = xW_K,\quad V = xW_V$$

et le score d'attention entre une *query* $q$ et une *key* $p$ devient :

$$
\begin{aligned}
Q_q \cdot K_p
&=
\big(e_q + \mathrm{PE}(q)\big) W_Q
\;\cdot\;
\big(e_p + \mathrm{PE}(p)\big) W_K \\
&=
e_q^\top W_Q W_K^\top e_p \\
&\quad + e_q^\top W_Q W_K^\top \mathrm{PE}(p) \\
&\quad + \mathrm{PE}(q)^\top W_Q W_K^\top e_p \\
&\quad + \mathrm{PE}(q)^\top W_Q W_K^\top \mathrm{PE}(p)
\end{aligned}
$$

Le dernier terme de la somme représente bien des interactions position-position mais les deux termes du milieu représentent des interactions contenu-position et position-contenu. La dépendance explicite à la distance relative est partiellement masquée par ces termes croisés.

---

## Prise en compte explicite des distances relatives : les *Rotary Position Embedding* (RoPE)

Pour remédier aux problèmes qui viennent d'être évoqués, certains chercheurs [(Su et al., 2021)](https://arxiv.org/abs/2104.09864) ont essayé de définir explicitement quelle représentation devaient avoir les vecteurs participant aux produits scalaires entre $query$ et $key$ de manière à intégrer proprement l'information de distance relative.

Dans l'approche de Vaswani on se souvient qu'il n'y avait pas cette démarche conceptuelle. Les représentations utilisées dans les produits scalaires de l'attention entre tokens, (supposées obtenues par les fonctions $f_q(x_q, q)$ et $f_k(x_p, p)$) étaient en quelque sorte imposées : addition des embeddings de contenu et de position, puis multiplication par une matrice de projection :

$$f_q(x_q, q) = (x_q + \mathrm{PE}(q)) W_Q$$

$$f_k(x_p, p) = (x_p + \mathrm{PE}(p)) W_K$$

le score étant donc :

$$\langle f_q(x_q, q), f_k(x_p, p) \rangle$$

Avec RoPE, on n'impose rien a-priori, et on cherche juste une représentation respectant une contrainte fonctionnelle sur le résultat final, comme exprimé par l'équation (11) de l'article sur RoPE [(Su et al., 2021)](https://arxiv.org/abs/2104.09864) :

$$\langle f_q(x_q, q), f_k(x_p, p) \rangle = G(x_q, x_p, q - p)$$

Comme le montre la signature de la fonction $G$, cette contrainte est destinée à garantir que le score entre deux tokens dépend du contenu sémantique des tokens et de leur distance relative.

Les auteurs de RoPE ont ainsi déterminé une représentation permettant de respecter cette contrainte :

$$f_q(x_q,q) = \Big(h^{(0)} e^{i q \theta_0},\; h^{(1)} e^{i q \theta_1},\; \ldots,\; h^{(K-1)} e^{i q \theta_{K-1}}\Big)$$

$$f_k(x_p,p) = \Big(g^{(0)} e^{i p \theta_0},\; g^{(1)} e^{i p \theta_1},\; \ldots,\; g^{(K-1)} e^{i p \theta_{K-1}}\Big)$$

$h^{(k)}$ (resp. $g^{(k)}$) correspond à une paire de dimensions du vecteur de contenu projeté de la *query* (resp. de la *key*). Un peu comme dans Vaswani, on regroupe donc des dimensions par paire, mais ici on regroupe les dimensions du vecteur de contenu pas du vecteur de position (voir Note 2 plus bas). On va voir que chaque nombre complexe $e^{i p \theta_{k}}$ représente une matrice de rotation appliquée à la paire de dimensions $g^{(k)}$ ($g^{(k)}$ que par abus de notation on se permet d'identifier ici au nombre complexe associé pour que la formule de multiplication soit correcte).

Pour résumer, on applique une projection sur les embeddings de contenu, puis les composantes (organisées en paires issues de l'embedding de contenu projeté) subissent chacune une rotation indépendante dans des plans 2D, avec un angle qui est un multiple de la position.

C'est une matrice bloc-diagonale composée de rotations 2×2 qui permet d'effectuer ces rotations pour chaque paire :

$$
\mathrm{RoPE}(x,p)
=
\begin{bmatrix}
R_0(p) & 0 & \cdots & 0 \\
0 & R_1(p) & \cdots & 0 \\
\vdots & \vdots & \ddots & \vdots \\
0 & 0 & \cdots & R_{K-1}(p)
\end{bmatrix}
\begin{bmatrix}
h^{(0)} \\
h^{(1)} \\
\vdots \\
h^{(K-1)}
\end{bmatrix}
$$

où :

$$R_k(p) = \begin{pmatrix} \cos(\theta_k p) & -\sin(\theta_k p) \\ \sin(\theta_k p) & \cos(\theta_k p) \end{pmatrix}$$

et $h^{(k)} \in \mathbb{R}^2$ désigne une paire de composantes du vecteur de contenu projeté (i.e. $h = Wx$), regroupées en sous-vecteurs de dimension 2.

> **Note 1.** On n'a pas représenté explicitement la projection $h = Wx$ afin de mettre en évidence uniquement la structure en sous-espaces 2D, qui est le cœur de l'opération de RoPE.

> **Note 2.** Comme dans l'approche de Vaswani, on regroupe les dimensions par paires. Toutefois, dans RoPE, ces paires ne portent pas directement une structure sinusoïdale : celle-ci est introduite uniquement via la matrice de rotation dépendant de la position, et non via le vecteur de représentation.

Voyons maintenant ce que vaut le produit scalaire de telles représentations de la clé $q$ et de la clé $p$. On repart donc des définitions déjà données :

$$f_q(x_q,q) = \big(h^{(0)} e^{i q \theta_0}, \ldots, h^{(K-1)} e^{i q \theta_{K-1}}\big)$$

$$f_k(x_p,p) = \big(g^{(0)} e^{i p \theta_0}, \ldots, g^{(K-1)} e^{i p \theta_{K-1}}\big)$$

où :

$$h^{(k)} = \text{contenu (query)}, \qquad g^{(k)} = \text{contenu (key)}$$

Le produit scalaire (hermitien) est alors :

$$\langle f_q, f_k \rangle = \sum_{k=0}^{K-1} h^{(k)} e^{i q \theta_k} \cdot \overline{g^{(k)} e^{i p \theta_k}}$$

qui après quelques manipulations algébriques devient :

$$\sum_{k} h^{(k)} \overline{g^{(k)}} \cdot e^{i (q-p)\theta_k}$$

**Avec cette représentation RoPE, le produit scalaire se factorise naturellement en un terme de contenu et un terme de position $q-p$.**

---

## Conclusion

RoPE n'a pas découvert la notion de distance relative mais l'utilise explicitement dans le produit scalaire, alors que chez Vaswani la notion apparaît implicitement et sans garantie formalisée, comme on l'a vu dans la première section

| | **Vaswani (2017)** | **RoPE (2021)** |
|---|---|---|
| **Démarche** | Représentation imposée a priori ; propriétés observées a posteriori | Propriété cible définie a priori ; représentation construite en conséquence |
| **Injection de la position** | Addition d'un vecteur de position au vecteur de contenu : $x_p = e_p + \mathrm{PE}(p)$ | Rotation du vecteur de contenu selon la position : $f_q(x_q,q) = R(q)\,W_Q x_q$ |
| **Dépendance à $q-p$** | Implicite : présente dans le terme position-position, masquée par les termes croisés contenu-position | Algébrique, garantie par construction : $\langle f_q, f_k \rangle = \sum_k h^{(k)}\overline{g^{(k)}}\, e^{i(q-p)\theta_k}$ |

La représentation a d'autres avantages importants (*long term decay*, gestion de contextes longs, etc.) mais je réserve ça pour une autre fois !

---

**Références**

- A. Vaswani et al., *Attention Is All You Need*, NeurIPS, 2017.
- J. Su et al., *[RoFormer: Enhanced Transformer with Rotary Position Embedding](https://arxiv.org/abs/2104.09864)*, arXiv:2104.09864, 2021.
