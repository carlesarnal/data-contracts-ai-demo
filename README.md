# Same Schema, Different Meaning

Companion to **Your Model Didn't Change, Your Input Did**. Two independent controls:

1. Apicurio Registry checks Avro reader/writer compatibility at publication.
2. A feature-input invariant checks explicitly declared units before inference.

## Run

Python 3.9+ runs the semantic checks without installing dependencies:

```sh
python3 demo.py
python3 -m unittest -v
```

For the real Registry publication check, start Docker/Podman and run:

```sh
docker compose up -d --wait
python3 demo.py --registry http://localhost:18181
docker compose down -v
```

The script uses a unique group per run, verifies a compatible addition, rejects an
incompatible required field, and checks that the rejected version was not created.
It deletes only its own group in a `finally` block. Do not point it at a production
registry: this is an unauthenticated localhost lab.

## What it establishes

`30 s` and `30000 ms` both normalize to `30 s`. Ignoring units fails an explicit
input assertion even though the Avro numeric type is unchanged. Unknown units,
negative values, non-finite values and booleans are rejected.

This is not a Kafka enforcement proxy, an inference benchmark, or evidence of
model-accuracy improvement. The Registry test exercises actual HTTP APIs; the
semantic fixture is deterministic application logic. See `VERIFICATION.md` for
executed checks, and `PRESENTATION_GUIDE.md` for delivery.

License: Apache-2.0; see LICENSE.
