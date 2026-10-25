# Presentation guide

Your Model Didn't Change, Your Input Did: Data Contracts for Streaming AI Pipelines

## Audience and central claim

A producer changes duration from 30 seconds to 30,000 milliseconds. The Avro long field can still deserialize perfectly. A consumer interpreting it as seconds receives a value a thousand times larger. The structural contract and the semantic feature contract answer different questions.

## 30-minute run of show

### 0:00 — 30 seconds versus 30000 milliseconds

A producer changes duration from 30 seconds to 30,000 milliseconds. The Avro long field can still deserialize perfectly. A consumer interpreting it as seconds receives a value a thousand times larger. The structural contract and the semantic feature contract answer different questions.

Compare the two duration records and their common normalized value of 30 seconds.

### 4:00 — Reject an incompatible schema publication

The lab creates a unique group and an Avro Duration artifact in Registry 3.3.3, enables BACKWARD compatibility, accepts a defaulted optional addition, then attempts to add a required string without a default. The real API returns HTTP 400 for incompatibility. The script verifies the rejected version is absent and the accepted version content is unchanged.

Run demo.py against Registry and inspect the rejected version and preserved accepted content.

### 9:00 — Check the normalized feature value

A deterministic normalization function requires an explicit unit. Both 30 s and 30000 ms must yield 30 seconds. The tests reject unknown units, negative/non-finite values and booleans. This catches an omitted conversion at the model-input boundary without pretending to measure a model-accuracy change. The same fixture can become a CI contract test.

Open test_demo.py and the normalization checks, including unknown units and non-finite values.

### 15:00 — Identify the enforcement boundaries

BACKWARD compatibility means a new reader can read old data; it does not guarantee every old reader accepts new writes. A Registry rule governs schema publication, not all bytes sent to Kafka. The demo deliberately has no Kafka producer or model service, so its evidence is limited to real publication behavior and deterministic input semantics. Group deletion is enabled only for the disposable lab cleanup.

Identify the Registry publication boundary separately from producer and inference integration.

### 21:00 — Keep publication and producer enforcement separate

Summarize the decision the example supports and the assumptions behind it.

Ask which additional semantic invariant the audience would test in its own input pipeline.

### 26:00 — Questions and buffer

Ask what the demonstration establishes and what it leaves open. Do not add another feature if time is short.

## Setup and fallback

```sh
python3 -m unittest -v && python3 demo.py
```

Fresh checks passed: three semantic unit tests; real Registry 3.3.3 compatible publication; HTTP 400 incompatible publication; rejected version absent; accepted content preserved; group cleanup passed after enabling deletion in the disposable lab.

Prebuild/download dependencies. Keep a recording of an actual successful run; if unavailable, use the documented walkthrough and say it is not live execution. Never substitute fabricated success output.

## Questions to prepare

- What is the simplest alternative?
- Which failure was actually exercised?
- Which guarantee belongs to the application rather than the infrastructure?
- Which result changes with versions or workload?

## 25-minute adaptation

Use one central trace, shorten setup and reserve three minutes for questions. Move the secondary implementation example to backup.
