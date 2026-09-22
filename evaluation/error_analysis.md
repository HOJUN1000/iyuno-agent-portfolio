# Error Analysis

## Evaluation Summary

- Faithfulness Proxy: 78.1%
- Supported Claims: 25
- Total Claims: 32
- Unsupported Claims: 7
- Similarity Threshold: 0.45

> The faithfulness score is an embedding-based proxy, not a direct factual-accuracy or entailment score.

## Unsupported Claims

### Error 1

**Question ID:** faith_01

**Question:** How can prompt injection attacks against generative AI systems be mitigated?

**Generated Claim:** Limiting the release of public information and artifacts.

**Best Retrieved Source:** [NIST | NIST AI 100-2 E2025 | p.62]

**Similarity Score:** 0.2953

**Observed Issue:** The generated claim did not reach the configured claim-to-context similarity threshold.

**Potential Causes:**

- The retrieved chunks may not directly support the claim.
- The language model may have generalized beyond the retrieved evidence.
- Relevant evidence may exist outside the Top-5 retrieved chunks.
- Repeated headers, footers, or document boilerplate may reduce retrieval quality.

**Potential Improvements:**

- Add reranking after vector retrieval.
- Remove repeated PDF headers and footers during ingestion.
- Require claim-level citations in the generation prompt.
- Add an entailment-based faithfulness evaluator.
- Tune retrieval depth and chunking using a validation set.

---

### Error 2

**Question ID:** faith_01

**Question:** How can prompt injection attacks against generative AI systems be mitigated?

**Generated Claim:** Implementing integrity checks to detect and prevent manipulation of the primary task of the language model.

**Best Retrieved Source:** [NIST | NIST AI 100-2 E2025 | p.67]

**Similarity Score:** 0.4075

**Observed Issue:** The generated claim did not reach the configured claim-to-context similarity threshold.

**Potential Causes:**

- The retrieved chunks may not directly support the claim.
- The language model may have generalized beyond the retrieved evidence.
- Relevant evidence may exist outside the Top-5 retrieved chunks.
- Repeated headers, footers, or document boilerplate may reduce retrieval quality.

**Potential Improvements:**

- Add reranking after vector retrieval.
- Remove repeated PDF headers and footers during ingestion.
- Require claim-level citations in the generation prompt.
- Add an entailment-based faithfulness evaluator.
- Tune retrieval depth and chunking using a validation set.

---

### Error 3

**Question ID:** faith_02

**Question:** What does NIST recommend for zero trust access control?

**Generated Claim:** This includes tracking network location, time, reported active attacks, and other relevant attributes.

**Best Retrieved Source:** [NIST | SP 800-207 | p.16]

**Similarity Score:** 0.3649

**Observed Issue:** The generated claim did not reach the configured claim-to-context similarity threshold.

**Potential Causes:**

- The retrieved chunks may not directly support the claim.
- The language model may have generalized beyond the retrieved evidence.
- Relevant evidence may exist outside the Top-5 retrieved chunks.
- Repeated headers, footers, or document boilerplate may reduce retrieval quality.

**Potential Improvements:**

- Add reranking after vector retrieval.
- Remove repeated PDF headers and footers during ingestion.
- Require claim-level citations in the generation prompt.
- Add an entailment-based faithfulness evaluator.
- Tune retrieval depth and chunking using a validation set.

---

### Error 4

**Question ID:** faith_03

**Question:** What security practices are recommended for application containers?

**Generated Claim:** **Data Encryption**: Encrypt data both at rest and in transit to protect sensitive information.

**Best Retrieved Source:** [NIST | SP 800-204C | p.14]

**Similarity Score:** 0.3323

**Observed Issue:** The generated claim did not reach the configured claim-to-context similarity threshold.

**Potential Causes:**

- The retrieved chunks may not directly support the claim.
- The language model may have generalized beyond the retrieved evidence.
- Relevant evidence may exist outside the Top-5 retrieved chunks.
- Repeated headers, footers, or document boilerplate may reduce retrieval quality.

**Potential Improvements:**

- Add reranking after vector retrieval.
- Remove repeated PDF headers and footers during ingestion.
- Require claim-level citations in the generation prompt.
- Add an entailment-based faithfulness evaluator.
- Tune retrieval depth and chunking using a validation set.

---

### Error 5

**Question ID:** faith_03

**Question:** What security practices are recommended for application containers?

**Generated Claim:** **Least Privilege Principle**: Use least privilege principle to ensure that only essential services have access to resources.

**Best Retrieved Source:** [NIST | SP 800-190 | p.4]

**Similarity Score:** 0.285

**Observed Issue:** The generated claim did not reach the configured claim-to-context similarity threshold.

**Potential Causes:**

- The retrieved chunks may not directly support the claim.
- The language model may have generalized beyond the retrieved evidence.
- Relevant evidence may exist outside the Top-5 retrieved chunks.
- Repeated headers, footers, or document boilerplate may reduce retrieval quality.

**Potential Improvements:**

- Add reranking after vector retrieval.
- Remove repeated PDF headers and footers during ingestion.
- Require claim-level citations in the generation prompt.
- Add an entailment-based faithfulness evaluator.
- Tune retrieval depth and chunking using a validation set.

---

### Error 6

**Question ID:** faith_03

**Question:** What security practices are recommended for application containers?

**Generated Claim:** **Secure Boot**: Enable secure boot mechanisms if applicable to prevent unauthorized modifications to the kernel.

**Best Retrieved Source:** [NIST | SP 800-190 | p.48]

**Similarity Score:** 0.395

**Observed Issue:** The generated claim did not reach the configured claim-to-context similarity threshold.

**Potential Causes:**

- The retrieved chunks may not directly support the claim.
- The language model may have generalized beyond the retrieved evidence.
- Relevant evidence may exist outside the Top-5 retrieved chunks.
- Repeated headers, footers, or document boilerplate may reduce retrieval quality.

**Potential Improvements:**

- Add reranking after vector retrieval.
- Remove repeated PDF headers and footers during ingestion.
- Require claim-level citations in the generation prompt.
- Add an entailment-based faithfulness evaluator.
- Tune retrieval depth and chunking using a validation set.

---

### Error 7

**Question ID:** faith_04

**Question:** What practices are recommended for secure software development?

**Generated Claim:** **Least Privilege Principle** - Emphasizes enforcing the principle of least privilege among development personnel and resources.

**Best Retrieved Source:** [NIST | SP 800-218 | p.18]

**Similarity Score:** 0.3379

**Observed Issue:** The generated claim did not reach the configured claim-to-context similarity threshold.

**Potential Causes:**

- The retrieved chunks may not directly support the claim.
- The language model may have generalized beyond the retrieved evidence.
- Relevant evidence may exist outside the Top-5 retrieved chunks.
- Repeated headers, footers, or document boilerplate may reduce retrieval quality.

**Potential Improvements:**

- Add reranking after vector retrieval.
- Remove repeated PDF headers and footers during ingestion.
- Require claim-level citations in the generation prompt.
- Add an entailment-based faithfulness evaluator.
- Tune retrieval depth and chunking using a validation set.

---

## Current System Limitations

1. Citation presence does not guarantee that every generated claim is supported.
2. Faithfulness is currently measured with embedding similarity rather than textual entailment.
3. Retrieval uses dense vector similarity without a reranker.
4. PDF boilerplate such as headers and footers can appear in retrieved chunks.
5. The local Qwen model may generalize beyond retrieved evidence.
6. Evaluation sets are curated and relatively small, so results should not be interpreted as universal system accuracy.

## Next Improvements

- Hybrid retrieval (dense + keyword search)
- Cross-encoder reranking
- Claim-level citation verification
- Better PDF preprocessing
- Larger and more adversarial evaluation dataset
- Latency optimization and model caching