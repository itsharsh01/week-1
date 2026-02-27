🛡 PhonePe Fraud Detection System — 6-Layer Product Teardown

This is a real-time financial risk decision system.
It must score transactions in <50–150ms, minimize fraud loss, avoid blocking legitimate users, and comply with RBI regulations — all at national scale.

Fraud detection is fundamentally a risk scoring + graph intelligence + behavioral modeling problem under extreme latency constraints.

Layer 1: Data Foundation
Overview

This layer ingests high-frequency transactional and behavioral data, enriches it, and makes it available for real-time scoring and offline training.

Key Components

Event ingestion: Apache Kafka / AWS Kinesis

Stream processing: Apache Flink

Data lake: Amazon S3 (Parquet, partitioned by date/hour)

Warehouse: Snowflake / BigQuery

Operational DB: Cassandra / DynamoDB

Feature store: Feast + Redis

Graph store (for link analysis): Neo4j / Amazon Neptune

Orchestration: Airflow

How It Works

Every payment generates an event containing:

Sender ID

Receiver ID

Device fingerprint

IP address

Geo-location

Time

Amount

Historical transaction summary

Real-time stream jobs compute rolling aggregates:

Transactions in last 5 minutes

Velocity features (amount/time)

Device reuse frequency

Failed attempts

Graph edges are updated:

User ↔ Device

User ↔ Bank account

User ↔ Merchant

These signals are stored in low-latency feature stores for inference.

Engineering Challenge Identified

Real-time feature freshness under heavy load.
Fraud signals (e.g., rapid repeated attempts) are highly time-sensitive.
If feature updates lag by even seconds, the fraudster succeeds.

Layer 2: Statistics & Analysis
Overview

Statistical monitoring detects anomalies and system-wide fraud trends.

Key Components

SQL analytics (Snowflake / BigQuery)

Python (SciPy, pandas, statsmodels)

Control charts for anomaly detection

Bayesian drift detection systems

Risk dashboards (Looker / Superset)

How It Works

Analysts monitor:

Fraud rate by geography

Merchant-level chargeback spikes

Sudden changes in device usage

Payment method anomaly

Baseline distributions are built for:

Normal transaction sizes

Normal transaction times

Typical user behavior windows

Statistical drift detection flags shifts in fraud patterns.

Engineering Challenge Identified

Concept drift.
Fraud strategies evolve quickly.
Static thresholds become obsolete within weeks.

Layer 3: Machine Learning Models
Overview

Core layer — predicts probability of fraud:

P(fraud | user, device, transaction context, graph signals)

Key Components

Gradient Boosted Trees (XGBoost / LightGBM)

Deep Neural Networks (PyTorch / TensorFlow)

Graph Neural Networks (PyG / DGL)

Imbalanced learning frameworks

SHAP for explainability

Model serving via TensorFlow Serving / TorchServe

How It Works
1️⃣ Feature-based model (primary)

GBDT handles:

Transaction amount deviation

Velocity

Device reuse

Geo anomalies

Historical fraud flags

GBDT is preferred because:

Handles heterogeneous tabular features well

Strong performance on imbalanced data

Fast inference

2️⃣ Graph-based fraud detection

Fraud networks operate in clusters.
Graph models detect:

Shared device among multiple risky accounts

Money laundering rings

Circular transaction patterns

GNNs compute risk propagation across connected entities.

3️⃣ Ensemble

Final risk score may combine:

Behavioral score

Graph score

Rule engine override

Engineering Challenge Identified

Extreme class imbalance.
Fraud rate may be <0.1%.
Training must avoid overfitting and maintain high recall without killing precision.

False positives hurt user trust. False negatives cost money.

Layer 4: LLM / Generative AI
Overview

LLMs are NOT core to real-time fraud scoring.

However, they may be used for:

Fraud analyst investigation summaries

Automated case explanation

Customer support chatbot (“Why was my payment blocked?”)

Key Components

GPT-based APIs or fine-tuned Llama

RAG over fraud case logs

Vector DB (Pinecone / Milvus)

How It Works

When a transaction is flagged:

LLM generates a human-readable explanation

Assists internal analysts with risk summary

Suggests possible fraud patterns

LLMs are offline/assistive, not inline decision engines.

Engineering Challenge Identified

Explainability + compliance.
RBI requires reasoning for blocked transactions.
LLM explanations must align with model output — hallucinations are unacceptable.

Layer 5: Deployment & Infrastructure
Overview

This is a mission-critical, low-latency decision engine.

Key Components

Kubernetes (EKS / GKE)

gRPC microservices

Redis for feature caching

Kafka for event streams

Circuit breakers (Envoy)

Prometheus + Grafana

Blue/Green deployments

HPA auto-scaling

Multi-AZ replication

How It Works

Transaction Flow:

User → UPI request → Risk Service API →
Fetch features (Redis) → Run model inference →
Return risk score → Approve / Block / Step-up verification

Fallback mechanism:

If model fails → rule-based backup

If feature store unavailable → degraded scoring

All decisions logged immutably for compliance.

Engineering Challenge Identified

Sub-100ms SLA under peak load.
UPI transactions spike during sales or IPL matches.
Latency directly affects payment success rates.

Layer 6: System Design & Scale
Overview

This system must scale nationally and remain resilient.

Key Components

Microservices architecture

Active-active multi-region deployment

Event-driven architecture

Feature versioning

Model registry (MLflow)

Automated retraining pipelines

Real-time feedback loop

How It Works

Design trade-offs:

Favor availability over strict consistency (CAP theorem)

Slight delay in fraud labeling acceptable

Real-time scoring must never block due to training pipeline

Fraud labeling feedback loop:

Confirmed fraud → retraining dataset

Chargeback data → model recalibration

Disaster recovery:

Cross-region failover

Idempotent transaction scoring

Engineering Challenge Identified

Adversarial system design.
Fraudsters adapt to model behavior.
This is a continuous arms race.

The hardest problem:

Designing a system that learns fast without being gamed.

🔥 Overall Analysis
Most Critical Layer

Layer 3 — Machine Learning Models

Because:

Fraud cost scales linearly with detection failure.

Precision-recall balance directly affects revenue and user trust.

Graph intelligence is key differentiator.

Complexity Rating

Advanced to Near Bleeding Edge

Why?

Financial risk

Real-time inference

Graph-based detection

Adversarial environment

Regulatory constraints

This is harder than recommendation systems due to compliance and monetary risk.

If Rebuilding From Scratch

The first thing to get right is:

Low-latency, real-time feature computation with graph signal integration.

Fraud detection is only as good as its freshest signals.

Without real-time velocity + graph awareness → fraud wins.

If you'd like, we can next:

Compare PhonePe vs Paytm fraud architecture

Go deeper into graph neural network usage

Or design a fraud detection system for a fintech startup

Your move.