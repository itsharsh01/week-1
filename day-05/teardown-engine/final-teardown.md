🧠 Zomato Restaurant Recommendation System — 6-Layer Product Teardown

This is a real-time, geo-aware, marketplace ranking system. It balances personalization, restaurant supply constraints, delivery logistics, ads, and revenue optimization — all under strict latency constraints (<150ms mobile SLA).

Layer 1: Data Foundation
Overview

This layer ingests and organizes massive behavioral, transactional, and geo-spatial data in both batch and real time.

Key Components

Event ingestion: Apache Kafka / AWS Kinesis

Stream processing: Apache Flink / Spark Streaming

Data lake: Amazon S3 (Parquet format)

Warehouse: Snowflake / BigQuery

Feature store: Feast + Redis / DynamoDB

Operational DB: Cassandra / Aurora PostgreSQL

Orchestration: Apache Airflow

How It Works

Every user action (search, click, scroll, order) generates an event pushed into Kafka.
Stream processors compute rolling metrics (e.g., 30-min CTR per restaurant per locality).
Batch jobs aggregate long-term signals (user cuisine affinity, price sensitivity).
Features are stored in low-latency stores for real-time inference.

Restaurant metadata (menu, rating, prep time, availability) lives in operational databases and is continuously synced into the feature layer.

Engineering Challenge Identified

Real-time + historical feature consistency.
The hardest issue is ensuring that training features and live inference features are identical (avoiding training-serving skew). Even minor schema drift can degrade model performance at scale.

Layer 2: Statistics & Analysis
Overview

Before ML, statistical systems monitor trends, demand shifts, and experimental impact.

Key Components

SQL-based analytics in Snowflake/BigQuery

Python (pandas, SciPy, statsmodels)

Bayesian A/B testing frameworks

Internal experimentation platform

Looker / Superset dashboards

How It Works

Statistical pipelines compute:

CTR (Click-through rate)

CVR (Conversion rate)

Supply-demand imbalance

Geo heatmaps

Time-of-day ordering curves

Every ranking change is evaluated via controlled experiments (multi-city segmented A/B tests). Bayesian methods reduce false positives in high-variance markets.

Engineering Challenge Identified

Causal attribution in a marketplace.
Did the model increase orders — or did demand spike due to a cricket match in Mumbai?
Marketplace dynamics introduce confounding variables that make clean experimentation difficult.

Layer 3: Machine Learning Models
Overview

This is the core ranking intelligence. It predicts:

P(order | user, restaurant, time, location, device, context)

Key Components

Candidate generation: FAISS (ANN search), matrix factorization

Ranking model: LightGBM / XGBoost

Deep ranking: TensorFlow / PyTorch (Wide & Deep, DLRM)

Embeddings store: Redis / Vector DB (Milvus)

Feature store: Feast

How It Works

Multi-stage ranking pipeline:

Candidate generation

Filter by location radius + availability

Collaborative filtering (users with similar behavior)

ANN similarity over embeddings

Reduce 10,000 restaurants → ~200 candidates

Learning-to-rank model

Gradient boosted trees handle high-cardinality categorical features

Predicts likelihood of order

Incorporates:

User cuisine affinity

Restaurant historical conversion

ETA penalty

Price sensitivity

Discount impact

Re-ranking layer

Diversity constraints

Sponsored placement blending

Fairness to new restaurants

Engineering Challenge Identified

Cold start & popularity bias.
New restaurants have no history. Popular restaurants get richer exposure.
The system must balance exploration vs exploitation without hurting revenue.

Layer 4: LLM / Generative AI
Overview

LLMs are supporting components, not core ranking drivers.

Key Components

BERT / RoBERTa for semantic query understanding

GPT-based models (API or fine-tuned Llama) for:

Review summarization

Intent extraction

Vector database (Pinecone / Milvus)

How It Works

LLMs interpret natural language queries:

“Cheap late-night biryani near me”

The model extracts:

Price intent

Time context

Cuisine preference

LLMs also summarize thousands of reviews into digestible highlights.

They do NOT directly compute ranking scores; instead they generate structured signals fed into ML ranking.

Engineering Challenge Identified

Latency + cost control.
LLMs are expensive. Running them per request is infeasible.
Most inference must be cached or distilled into lightweight embeddings.

Layer 5: Deployment & Infrastructure
Overview

This system runs at high QPS with strict SLA constraints and heavy peak-time bursts.

Key Components

Kubernetes (EKS / GKE)

Docker containers

gRPC microservices

Redis caching layer

API Gateway (NGINX / Envoy)

Prometheus + Grafana (metrics)

ELK stack (logging)

Autoscaling (HPA)

CDN (Cloudflare / Akamai)

How It Works

Mobile App → API Gateway → Ranking Service → Feature Store → Model Service → Re-ranker → Response

Heavy caching ensures:

Popular restaurant lists are partially precomputed

Trending lists are refreshed periodically

Canary deployments roll out new models gradually to specific cities.

Engineering Challenge Identified

Tail latency under peak load (8–10 PM).
One slow downstream service (feature store miss) can blow SLA.
System must degrade gracefully (fallback rankings).

Layer 6: System Design & Scale
Overview

Zomato operates a two-sided marketplace — balancing users and restaurants.

Key Components

Microservices architecture

Geo-sharded infrastructure

Multi-region deployment

Circuit breakers & bulkheads

Blue-Green deployments

Async retraining pipelines

How It Works

The architecture separates:

Search

Ranking

Ads

Payments

Logistics ETA

Geo-based sharding ensures cities operate semi-independently to reduce blast radius.

Trade-offs:

Slight staleness allowed in trending lists

Prioritize availability over strict consistency (CAP trade-off)

Engineering Challenge Identified

Marketplace equilibrium.
Too much exposure to high-conversion restaurants → smaller restaurants starve.
Too much fairness → revenue drops.
Balancing business incentives with algorithmic optimization is the hardest non-obvious problem.

🔥 Overall Analysis
Most Critical Layer

Layer 3 — Machine Learning Ranking

Because:

Small lift in conversion = massive revenue impact.

This layer directly influences marketplace liquidity.

It encodes personalization, monetization, and logistics trade-offs.

Complexity Rating

Advanced

Why?

Mature recommender science exists.

But production-scale, geo-aware, real-time marketplace ranking is non-trivial.

Requires coordination across ML, infra, experimentation, and economics.

Not bleeding edge like autonomous driving — but highly sophisticated.

If Rebuilding From Scratch

The first thing to get right is:

Accurate, real-time feature instrumentation with clean event logging.

Bad data = broken personalization = biased ranking = revenue leakage.

Everything else depends on this foundation.

If you'd like, next we can:

Compare Zomato vs Swiggy architectures

Redesign this for a startup with 50K users

Or deep dive into the ranking math (learning-to-rank loss functions, etc.)