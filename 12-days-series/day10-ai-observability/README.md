# Day 10: AI Observability

## 🎯 Learning Objectives
- Understand the importance of observability in AI/ML systems
- Learn key metrics for monitoring LLM applications
- Implement logging, tracing, and monitoring for RAG pipelines
- Detect and debug common AI system failures
- Set up alerts and dashboards for production AI systems

## 📚 Table of Contents
1. [Why AI Observability Matters](#why-ai-observability-matters)
2. [Core Concepts of Observability](#core-concepts-of-observability)
3. [Monitoring LLM Applications](#monitoring-llm-applications)
4. [Building Observability into RAG Systems](#building-observability-into-rag-systems)
5. [Lab Exercises](#lab-exercises)
6. [Knowledge Check](#knowledge-check)

---

## Why AI Observability Matters

### The Challenge with AI Systems

Traditional software monitoring isn't enough for AI applications because:

**Non-Deterministic Behavior**
```python
# Same input can produce different outputs
response1 = llm.invoke("Explain quantum computing")
response2 = llm.invoke("Explain quantum computing")
# response1 != response2 (potentially)
```

**Hidden Failure Modes**
- Hallucinations (confident but wrong answers)
- Context window overflow
- Embedding drift over time
- Prompt injection attacks
- Cost overruns from excessive token usage

**Complex Dependencies**
```
User Query → Embedding Model → Vector DB → LLM → Response
     ↓            ↓              ↓         ↓        ↓
  Latency     Quality       Freshness   Cost    Accuracy
```

### Real-World Incidents

| Incident | Impact | Could Be Prevented By |
|----------|--------|----------------------|
| Hallucinated legal citations | Lawsuit dismissal | Output validation + human review |
| Leaked PII in responses | GDPR violation | Content filtering + monitoring |
| Runaway API costs ($50k/day) | Budget crisis | Cost alerts + rate limiting |
| Biased hiring recommendations | Discrimination claims | Fairness metrics + audits |
| Slow response times (>30s) | User churn | Latency monitoring + auto-scaling |

---

## Core Concepts of Observability

### The Three Pillars (+2 for AI)

#### 1. Logs
Record of discrete events with timestamps:

```python
import logging
from datetime import datetime

logging.info({
    "timestamp": datetime.now().isoformat(),
    "event": "query_processed",
    "query_id": "abc123",
    "query_length": 45,
    "retrieved_docs": 3,
    "response_time_ms": 234,
    "tokens_used": 512,
    "cost_usd": 0.002
})
```

#### 2. Metrics
Aggregated numerical measurements:

```python
# Key metrics to track
metrics = {
    "latency_p50": 150,      # Median response time
    "latency_p99": 890,      # 99th percentile
    "error_rate": 0.02,      # 2% failure rate
    "token_usage_avg": 450,  # Average tokens per request
    "cost_per_hour": 12.50,  # Hourly API cost
    "cache_hit_rate": 0.67,  # 67% cache efficiency
    "retrieval_precision": 0.85  # Quality metric
}
```

#### 3. Traces
End-to-end request flow tracking:

```
Trace: user_query_123
├─ Span: embed_query (15ms)
├─ Span: vector_search (45ms)
│  ├─ Span: index_lookup (30ms)
│  └─ Span: rerank (15ms)
├─ Span: llm_generate (320ms)
│  ├─ Span: prompt_construction (10ms)
│  └─ Span: api_call (310ms)
└─ Span: response_validation (8ms)

Total: 388ms
```

#### 4. Quality Scores (AI-Specific)
- **Faithfulness**: Is the answer grounded in context?
- **Relevance**: Does it answer the question?
- **Toxicity**: Is the output safe/appropriate?
- **Confidence**: How certain is the model?

#### 5. Cost Metrics (AI-Specific)
- Token consumption by endpoint
- Cost per query/user/session
- Budget utilization rate
- ROI calculations

---

## Monitoring LLM Applications

### Essential Metrics Dashboard

#### Performance Metrics
```python
from prometheus_client import Histogram, Counter, Gauge

# Response latency
LATENCY = Histogram(
    'llm_response_latency_seconds',
    'Time to generate response',
    buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

# Token usage
TOKENS_USED = Counter(
    'llm_tokens_total',
    'Total tokens consumed',
    ['type']  # prompt, completion, total
)

# Error tracking
ERRORS = Counter(
    'llm_errors_total',
    'Total errors',
    ['type']  # timeout, rate_limit, api_error, etc.
)

# Active requests
ACTIVE_REQUESTS = Gauge(
    'llm_active_requests',
    'Number of concurrent requests'
)
```

#### Quality Metrics
```python
def calculate_faithfulness(response, context):
    """Measure if response is grounded in provided context"""
    # Use NLI model or LLM-based evaluation
    pass

def calculate_hallucination_rate(responses_batch):
    """Track percentage of potentially hallucinated content"""
    hallucinated = 0
    for response in responses_batch:
        if has_unsupported_claims(response):
            hallucinated += 1
    return hallucinated / len(responses_batch)

def track_retrieval_quality(query, retrieved_docs, relevance_scores):
    """Monitor retrieval effectiveness"""
    return {
        "precision_at_3": sum(relevance_scores[:3]) / 3,
        "mean_reciprocal_rank": calculate_mrr(relevance_scores),
        "ndcg": calculate_ndcg(relevance_scores)
    }
```

### Cost Monitoring

```python
class CostTracker:
    def __init__(self, budget_limit=1000.0):
        self.budget_limit = budget_limit
        self.current_spend = 0.0
        
    def track_usage(self, prompt_tokens, completion_tokens, model):
        """Track and alert on API costs"""
        pricing = {
            "gpt-4o": {"prompt": 0.000005, "completion": 0.000015},
            "gpt-4o-mini": {"prompt": 0.00000015, "completion": 0.0000006},
            "claude-3-haiku": {"prompt": 0.00000025, "completion": 0.00000125}
        }
        
        cost = (prompt_tokens * pricing[model]["prompt"] + 
                completion_tokens * pricing[model]["completion"])
        
        self.current_spend += cost
        
        # Alert at 80% budget
        if self.current_spend > self.budget_limit * 0.8:
            send_alert(f"⚠️ Budget warning: ${self.current_spend:.2f} spent")
            
        return cost
```

---

## Building Observability into RAG Systems

### Complete Observability Stack

See `examples/rag_monitoring.py` for a full implementation.

#### 1. Structured Logging

```python
import json
from datetime import datetime

class RAGLogger:
    def __init__(self, log_file="rag_logs.jsonl"):
        self.log_file = log_file
    
    def log_query(self, query_id, query, metadata):
        """Log incoming query with context"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "query_received",
            "query_id": query_id,
            "query": query,
            "metadata": metadata
        }
        self._write_log(log_entry)
    
    def log_retrieval(self, query_id, docs, latency_ms, scores):
        """Log retrieval results"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "retrieval_complete",
            "query_id": query_id,
            "num_docs": len(docs),
            "avg_score": sum(scores) / len(scores) if scores else 0,
            "latency_ms": latency_ms,
            "doc_ids": [doc.id for doc in docs]
        }
        self._write_log(log_entry)
    
    def log_generation(self, query_id, response, tokens, latency_ms, cost):
        """Log LLM generation"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "generation_complete",
            "query_id": query_id,
            "response_length": len(response),
            "prompt_tokens": tokens["prompt"],
            "completion_tokens": tokens["completion"],
            "total_tokens": tokens["total"],
            "latency_ms": latency_ms,
            "cost_usd": cost
        }
        self._write_log(log_entry)
    
    def _write_log(self, entry):
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
```

#### 2. Distributed Tracing

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporters.jaeger.thrift import JaegerExporter

# Setup tracing
provider = TracerProvider()
exporter = JaegerExporter(agent_host_name="localhost", agent_port=6831)
processor = BatchSpanProcessor(exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

@tracer.start_as_current_span("rag_pipeline")
def process_query(query):
    with tracer.start_as_current_span("embed_query") as span:
        embedding = generate_embedding(query)
        span.set_attribute("embedding_dim", len(embedding))
    
    with tracer.start_as_current_span("vector_search") as span:
        docs = search_vector_store(embedding)
        span.set_attribute("num_results", len(docs))
    
    with tracer.start_as_current_span("generate_response") as span:
        response = call_llm(query, docs)
        span.set_attribute("response_length", len(response))
    
    return response
```

#### 3. Real-time Dashboards

**Grafana Dashboard Panels:**

```yaml
# dashboard.yml
panels:
  - title: "Request Rate"
    type: graph
    query: "rate(llm_requests_total[5m])"
    
  - title: "P99 Latency"
    type: gauge
    query: "histogram_quantile(0.99, llm_latency_bucket)"
    
  - title: "Error Rate"
    type: stat
    query: "sum(rate(llm_errors_total[5m])) / sum(rate(llm_requests_total[5m]))"
    
  - title: "Token Usage"
    type: timeseries
    query: "sum(rate(llm_tokens_total[5m])) by (type)"
    
  - title: "Cost Burn Rate"
    type: gauge
    query: "llm_cost_total / llm_budget_total"
    
  - title: "Retrieval Quality"
    type: heatmap
    query: "avg(retrieval_precision_score)"
```

#### 4. Alerting Rules

```yaml
# alerting_rules.yml
groups:
  - name: rag_alerts
    rules:
      - alert: HighLatency
        expr: histogram_quantile(0.95, llm_latency_bucket) > 5
        for: 5m
        annotations:
          summary: "P95 latency above 5 seconds"
          
      - alert: HighErrorRate
        expr: sum(rate(llm_errors_total[5m])) / sum(rate(llm_requests_total[5m])) > 0.05
        for: 2m
        annotations:
          summary: "Error rate above 5%"
          
      - alert: BudgetWarning
        expr: llm_cost_total > llm_budget_total * 0.8
        annotations:
          summary: "80% of monthly budget consumed"
          
      - alert: RetrievalDegradation
        expr: avg(retrieval_precision_score) < 0.7
        for: 10m
        annotations:
          summary: "Retrieval quality degraded"
```

---

## Lab Exercises

### Lab 1: Build a Monitoring System

**Objective**: Implement comprehensive monitoring for a RAG application

**Files**: See `labs/lab1_monitoring/starter_code.py`

**Tasks**:
1. Add structured logging to all pipeline stages
2. Create Prometheus metrics for key indicators
3. Set up OpenTelemetry tracing
4. Build a simple Grafana dashboard
5. Configure alerting rules

**Success Criteria**:
- ✅ All queries logged with unique IDs
- ✅ Latency tracked at p50, p95, p99 percentiles
- ✅ Token usage and costs recorded
- ✅ End-to-end traces visible in Jaeger
- ✅ Alerts fire on threshold breaches

### Lab 2: Quality Evaluation Pipeline

**Objective**: Implement automated quality assessment

**Tasks**:
1. Add faithfulness scoring using NLI models
2. Detect potential hallucinations
3. Measure answer relevance
4. Track toxicity/safety metrics
5. Create quality trend reports

**Deliverable**: Quality dashboard with historical trends

### Lab 3: Production Incident Simulation

**Objective**: Practice debugging real-world issues

**Scenarios**:
1. Sudden latency spike investigation
2. Cost anomaly detection and root cause
3. Retrieval quality degradation analysis
4. Hallucination pattern identification

---

## Knowledge Check

### Questions

1. **What are the three pillars of observability, and what additional pillars matter for AI?**
   <details>
   <summary>Click to reveal answer</summary>
   
   **Traditional Three Pillars:**
   - **Logs**: Discrete event records with timestamps
   - **Metrics**: Aggregated numerical measurements
   - **Traces**: End-to-end request flow tracking
   
   **AI-Specific Additions:**
   - **Quality Scores**: Faithfulness, relevance, toxicity, confidence
   - **Cost Metrics**: Token usage, budget tracking, ROI
   
   </details>

2. **Why is traditional monitoring insufficient for LLM applications?**
   <details>
   <summary>Click to reveal answer</summary>
   
   Traditional monitoring assumes:
   - Deterministic behavior (same input → same output)
   - Clear error states (success/failure binary)
   - Predictable performance patterns
   
   LLMs violate these assumptions because they:
   - Produce non-deterministic outputs
   - Can fail silently (plausible but wrong answers)
   - Have complex quality dimensions beyond uptime
   - Have variable costs per request
   
   </details>

3. **How would you detect a hallucination in production?**
   <details>
   <summary>Click to reveal answer</summary>
   
   **Detection Strategies:**
   - **NLI Models**: Check if response is entailed by context
   - **Fact Verification**: Cross-reference with knowledge base
   - **Citation Analysis**: Verify cited sources exist and support claims
   - **Confidence Scoring**: Low confidence may indicate uncertainty
   - **Consistency Checks**: Compare multiple runs for contradictions
   - **Human Feedback**: User thumbs up/down ratings
   
   **Implementation:**
   ```python
   def detect_hallucination(response, context):
       nli_model = load_nli_model()
       entailment = nli_model.predict(context, response)
       return entailment == "contradiction"
   ```
   
   </details>

4. **What metrics would you include in an executive dashboard vs. engineering dashboard?**
   <details>
   <summary>Click to reveal answer</summary>
   
   **Executive Dashboard:**
   - Total cost vs. budget
   - User satisfaction score
   - System availability %
   - Queries processed per day
   - ROI metrics
   
   **Engineering Dashboard:**
   - P50/P95/P99 latencies
   - Error rates by type
   - Token usage breakdown
   - Cache hit rates
   - Retrieval precision/recall
   - Model version performance
   - Infrastructure utilization
   
   </details>

5. **Describe your approach to debugging a sudden increase in response latency.**
   <details>
   <summary>Click to reveal answer</summary>
   
   **Systematic Debugging Approach:**
   
   1. **Check dashboards**: Identify when spike started, affected endpoints
   2. **Examine traces**: Find which stage slowed down (embedding, retrieval, LLM)
   3. **Review recent changes**: Deployments, config updates, data changes
   4. **Check dependencies**: API provider status, database performance
   5. **Analyze patterns**: Specific queries, users, or times affected?
   6. **Resource monitoring**: CPU, memory, network, disk I/O
   7. **External factors**: Rate limits, quota exhaustion, network issues
   8. **Test hypothesis**: Reproduce in staging, try fixes incrementally
   
   **Tools to use:**
   - Distributed traces (Jaeger, Zipkin)
   - APM tools (DataDog, New Relic)
   - Log aggregation (ELK, Splunk)
   - Infrastructure monitoring (Prometheus, Grafana)
   
   </details>

---

## Next Steps

### Further Learning
- Study MLOps best practices for model monitoring
- Learn about A/B testing for LLM applications
- Explore automated remediation strategies
- Understand compliance requirements (GDPR, HIPAA)

### Practice Projects
1. Build a complete observability stack for a demo RAG app
2. Create automated quality evaluation pipeline
3. Design incident response runbooks for AI failures
4. Implement cost optimization recommendations engine

### Resources
Check the `resources/` folder for:
- Monitoring tool documentation
- Dashboard templates
- Alerting rule examples
- Case studies from production deployments

---

**Congratulations!** You've learned how to build comprehensive observability for AI systems. Continue to Day 11 to learn about AI Security & Guardrails.
