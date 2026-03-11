---
layout: post
title: "The Two Dimensions of AI Agent Traceability"
date: 2026-03-11
author: "AI Referent"
tags: [Traceability, Accountability, Context Window, Audit, Attribution]
reading_time: 4
description: "Action logging is the obvious starting point for AI agent traceability. But a list of logged actions cannot reconstruct reasoning — and that changes everything."
excerpt: "Action logging is the obvious starting point for AI agent traceability. But a list of logged actions cannot reconstruct reasoning — and that changes everything."
---

As AI agents take on increasingly consequential tasks — executing code, making financial decisions, interacting with external services, managing critical infrastructure — one of the most pressing engineering challenges is accountability. When something goes wrong, or when an audit is needed, we must be able to answer three fundamental questions: what did the agent do exactly? Was that behavior correct or within bounds? And can this be proven irrefutably, even to a third party?

In this post we focus on **traceability** (what happened). At first glance, traceability seems straightforward: log the LLM calls, log the tool calls, store inputs and outputs. Classical logging, applied to agents.

The problem is that a simple list of logged actions is not enough: We are not monitoring a traditional deterministic software system. We are monitoring something intelligent — a system whose behavior emerges from a complex interaction between its model, its task, and its information environment. reconstruct *reasoning*. What we actually need to know is: **given what the agent perceived at that moment, it decided to do X**. The goal is not just to know what the agent did, but to reconstruct the causal link.

To achieve this goal, we thus need to know the **global state that conditioned all of the agent's actions at that reasoning step**. For an LLM-based agent, an important part of that global state is the context window — and it may include past tool results, injected documents, conversation history, and system instructions. Capturing all of this faithfully at every step is expensive at scale. Also, this raises serious privacy concerns: the context may contain user data or confidential documents that should not be retained in a general-purpose log. From a technical point of view, one way to address both problems is to store, in the trace, only a cryptographic hash of the context — a compact fingerprint that uniquely identifies it without revealing its content. The full context payload is stored separately, in a secure, access-controlled store. The trace stays lightweight; the full context can be retrieved and verified against the hash whenever a formal audit requires it.

The conclusion is that traceability is more complex than it first appears. It has **two distinct dimensions**. The first is **action traceability** — logging what the agent did, along with the identity metadata that makes those actions attributable: agent instance, model version, runtime environment. Note that identity is not a separate concern; it is an intrinsic part of the action record, as natural as a timestamp. "What did the agent do?" cannot be answered without knowing which agent we are talking about. The second dimension is **epistemic state traceability** — capturing what the agent knew just before acting. This is the part most logging systems miss entirely.

To be complete, there is a separate property often mentioned about traceability: **integrity**. But this is rather a property of the logging infrastructure itself: Technically, an append-only structure, hash-chained entries, and cryptographic signing ensure that the trace cannot be silently modified or fabricated after the fact. This is needed to support  non-repudiation. It is less about what the trace contains than about whether the trace can be trusted at all. 

Numerous traceability-related questions remain open. Agents rarely work in isolation: the output of one often becomes the input of another, chaining decisions across a pipeline in ways that make attribution even harder. But this does not undermine our distinction — if anything, it sharpens it. Whether you are tracing a single agent or an entire multi-agent system, you still need to capture what it did and why it reasoned that way. That duality holds at every level of the chain. And it opens up plenty of ground for future posts.

