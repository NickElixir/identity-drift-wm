# Early Research Report

Please submit this form to the Canvas assignment in your Thesis course (MSc Thesis Class 2025: MSc program) by [submission deadline].

Student's first name: Nikolaj

Student's last name: Luczenko

Date of report submission: 29 May 2026

Project supervisor's full name: [Project supervisor's full name]

Project supervisor's work place and position: [Supervisor's workplace and position]

Project name in English (mandatory): HoverAI: Retrieval-Augmented Assistant and Generative World Models for XR and Robot Navigation

Project name in Russian: [Russian project name]

## Project Description

During the early research period, I worked on two connected prototype projects related to AI-assisted interaction, VR/AR, and robotics.

The first project is `hoverai_rag`. It is a retrieval-augmented generation system for a HoverAI assistant. The system uses a local knowledge base about Skoltech events, local embeddings, a SQLite-based storage layer, optional web fallback, and a local LLM interface. It also includes an API server and a book-like Linux viewer prototype for showing answers in a readable form.

The second project is `identity-drift-wm`. It studies identity drift in generative world models. The main idea is to test whether an image-conditioned world model can preserve the identity and geometry of important objects after generating a navigable 3D scene. In the current pilot, selected 2D car reference images are used as inputs for World Labs Marble. The generated worlds are inspected through controlled orbit recordings and frame annotations. The longer-term goal is to connect generated Gaussian splat worlds and exported collision meshes with ROS2 and OMPL trajectory planning.

The common research direction is how AI systems can support spatial and embodied interaction, where either textual answers or generated 3D environments must be reliable enough for practical use. In this sense, the two projects are connected by one question: how can we evaluate the reliability of AI-generated outputs when they are used in an interactive or navigation-related setting?

## Project Goals and My Personal Goals in the Projects. My Role

The general project goals were:

- to build a working RAG-based assistant prototype with local knowledge, source-aware answers, and a simple interaction interface;
- to prepare and verify a small Skoltech events dataset for retrieval;
- to investigate whether generative world models preserve object identity when creating navigable 3D scenes;
- to design a basic evaluation protocol for identity drift in generated worlds;
- to connect the research question with VR/AR, Gaussian splatting, and robot navigation.

My personal goals were more practical. As a first-year MSc student, I wanted to understand how to move from an idea to a reproducible prototype. Before these projects, I had not built a complete RAG pipeline or designed an empirical evaluation protocol for generated 3D scenes. I also had limited experience with research-style documentation, dataset verification, and explaining experimental limitations in an academic way.

My role included software development, dataset preparation, prompt and protocol design, experiment planning, documentation, and presentation preparation. In `hoverai_rag`, I worked on the architecture of the RAG pipeline, the local knowledge base, retrieval behavior, web fallback, API interaction, and viewer-related components. In `identity-drift-wm`, I worked on the research framing, Marble generation pipeline, input selection, QA protocol, result logging, and the connection between generated worlds and robot navigation.

## What I Accomplished and Progress Toward the Objective

In the `hoverai_rag` repository, I accomplished the following:

- implemented and organized a RAG prototype with a local LLM interface, local text embeddings, and a SQLite knowledge database;
- added structured data models for retrieved results and answer payloads, including source URLs, image metadata, verification status, venue, room, retrieval score, and timing information;
- added web fallback logic for cases where the local knowledge base does not provide a reliable answer;
- prepared a Skoltech events dataset in JSONL format and created scripts for event metadata curation, image curation, local image backfilling, ingestion, and retrieval inspection;
- prepared a fact-check report for the Skoltech events dataset, checking 18 records and identifying confirmed, partially confirmed, and contradicted records;
- implemented a FastAPI server with endpoints for health checks, state, commands, queries, and WebSocket updates;
- developed a book-like viewer prototype where generated answers can be shown as pages and controlled with simple commands such as open, close, left, and right.

In the `identity-drift-wm` repository, I accomplished the following:

- defined the research problem as identity drift in generative world models, with a focus on consequences for robot navigation;
- prepared selected input images for the Marble pilot and documented them in the repository;
- created prompts and protocols for generating and evaluating Marble worlds;
- added scripts for generating Marble worlds, polling existing operations, selecting inputs, editing scene images, preparing VLM review batches, and extracting orbit frames from recordings;
- generated and documented a first successful Marble world using `marble-1.1`;
- recorded and trimmed a Marble walkthrough video for the first car example;
- extracted 8 controlled orbit frames from the first recording and prepared annotation tables for identity, wheel preservation, body shape, and major failures;
- documented a drone-world pipeline from input photo to Marble world, exported collider mesh, ROS2 + OMPL path planning, and trajectory visualization;
- prepared presentation material explaining Gaussian splatting, identity drift, and why geometry preservation matters for robot navigation.

The engineering outputs include reusable scripts, datasets, prompts, result tables, and prototype interfaces. The research outputs include an initial evaluation protocol, a small taxonomy of observed failure modes, and documented limitations of the current pilot.

The work is currently at the pilot-study stage. Therefore, I do not treat the results as final experimental evidence. However, they already show several concrete failure modes that can be used to design a more systematic evaluation. In one Marble result, the car remains recognizable from some views, but extra cars and visible body/front geometry drift appear. This supports the need for evaluation criteria that go beyond visual plausibility.

## Significant Problems Faced and Solutions Found

One important problem in the RAG project was factual reliability. Some event records were incomplete, too generic, or pointed to weak source URLs. I addressed this by preparing a fact-check report and separating records by verification status. This helped me understand that a RAG system is not only a question-answering model. It also requires careful data preparation, source tracking, and verification.

Another problem was retrieval confidence. A local knowledge base can return a result even when it is not sufficiently relevant. To reduce this risk, I worked with retrieval scores, thresholds, verification bonuses, and web fallback. This made the system more robust and helped avoid unsupported answers.

In the world model project, the main problem was that generative 3D scenes are unpredictable. A world can be visually impressive but still include object duplication, distorted car geometry, incorrect wheel preservation, or route ambiguity. I addressed this by creating a structured QA protocol and frame annotation table instead of relying only on subjective visual impressions.

Another practical problem was external API usage. Marble world generation can spend credits and create external operations. To reduce the risk of accidental reruns, the repository includes safety instructions, generation scripts, and polling scripts. The workflow separates generation from inspection.

A broader challenge was that both projects were new for me. I had to learn how to organize code, data, prompts, experiment results, and documentation so that another person could understand the work. I solved this gradually by using repository-level documentation, protocol files, result tables, and small reusable scripts.

The main limitation of the current work is scale. The world-model experiment is still small, the evaluation is mostly manual, and only one main world model has been tested so far. The next step is to increase the number of generated scenes, complete the frame annotations, and connect the visual drift observations more directly with collision-mesh and trajectory-planning checks.

## Outcomes of the Project for Me

The main outcome for me was learning how to connect software prototyping with research methodology: defining a narrower question, documenting assumptions, keeping reproducible artifacts, and reporting limitations honestly.

Technically, I learned more about RAG systems, local LLMs, embeddings, SQLite storage, FastAPI, WebSocket communication, data ingestion, and source-aware answer formatting. I also learned about Gaussian splatting, World Labs Marble, 3D world generation, collision meshes, and the basic relationship between generated environments and robot motion planning.

From the research side, I learned how to turn a broad idea into a smaller research question. For example, instead of asking whether generative worlds are "good", I learned to ask whether they preserve object identity, geometry, and route feasibility. I also learned that negative or mixed results are still useful if they are documented clearly.

I also improved my project organization skills. I learned to keep separate folders for inputs, prompts, protocols, results, recordings, scripts, and documentation. This was important because the projects include many different types of artifacts.

In terms of teamwork, I learned that technical work needs clear communication. It is not enough to build a script or generate an example. The team also needs to know what was generated, what failed, what is safe to rerun, and what should be evaluated next. I became more aware of the importance of handoff notes, concise documentation, and concrete experiment records.

Overall, this early research period gave me first practical experience with AI research prototypes. I now understand better how much work is needed between a demo idea and a research-ready result.

## Format of the Report to the Project Supervisor

The report to the project supervisor will be provided in the following formats:

- this written early research report;
- GitHub repositories with code, datasets, protocols, prompts, and results;
- a presentation for the VR & Haptics course project;
- optional short demo materials, including Marble walkthrough recordings and screenshots from the RAG / viewer prototype.

## Student's Confirmation

Hereby I confirm that the report is approved by the project supervisor and academic or research (thesis) advisor (if known).

[Student signature / confirmation]
