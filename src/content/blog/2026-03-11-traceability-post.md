---
title: "The Two Dimensions of AI Agent Traceability"
date: 2026-03-11
author: "AI Referent"
tags: [Traceability, Audit]
reading_time: 4
description: "Action logging is the obvious starting point for AI agent traceability. But a list of logged actions cannot reconstruct reasoning — and that changes everything."
excerpt: "Action logging is the obvious starting point for AI agent traceability. But a list of logged actions cannot reconstruct reasoning — and that changes everything."
---

As AI agents take on increasingly consequential tasks — executing code, making financial decisions, interacting with external services, managing critical infrastructure — one of the most pressing engineering challenges is accountability. When something goes wrong, or when an audit is needed, we must be able to answer three fundamental questions: what did the agent do exactly? Was that behavior correct or within bounds? And can this be proven irrefutably, even to a third party?

In this post we focus on the first question, **traceability** (determine what happened). At first glance, traceability seems straightforward: log the LLM calls, log the tool calls, store inputs and outputs. Classical logging, applied to agents.

The problem is that a simple list of logged actions is not enough: We are not monitoring a traditional deterministic software system. We are monitoring something intelligent — a system whose behavior is not easily predictable, and emerges from a complex interaction between its model, its task, and its information environment. Thus, we need to determine not just what happened, but why it happened. We need to reconstruct the *reasoning*, tracing the causal links.

To achieve this goal, we need to know the *global state that conditioned all of the agent's actions at that reasoning step*. For an LLM-based agent, an important part of that global state is the context window — and it may include past tool results, injected documents, conversation history, and system instructions. Capturing all of this faithfully at every step is expensive at scale. Also, this raises serious privacy concerns: the context may contain user data or confidential documents that should not be retained in a general-purpose log. From a technical point of view, one way to address both problems is to store, in the trace, only a cryptographic hash of the context — a compact fingerprint that uniquely identifies it without revealing its content. The full context payload is stored separately, in a secure, access-controlled store. The trace stays lightweight; the full context can be retrieved and verified against the hash whenever a formal audit requires it.

The conclusion is that traceability is more complex than it first appears. It has **two distinct dimensions**. The first is **action traceability** — logging what the agent did, along with the identity metadata that makes those actions attributable: agent instance, model version, runtime environment. The second dimension is **epistemic state traceability** — capturing what the agent knew just before acting. This is the part most logging systems miss.

Numerous traceability-related questions remain open. Agents rarely work in isolation: the output of one often becomes the input of another, chaining decisions across a pipeline in ways that make  traceability even harder. This opens up plenty of ground for future posts.
