# Agentic Knowledge Triage

Iyuno **AI Agent Engineer** 채용공고의 실제 요구사항을 분석하고, 이를 직접 구현한 AI Agent 포트폴리오 프로젝트입니다.

공개된 보안·AI 기술 문서를 기반으로 RAG 검색을 수행하고, 사용자 질문에 따라 적절한 Tool을 선택해 답변하는 Agent 시스템을 구현했습니다.

---

## 1. 목표 채용공고

- **회사:** Iyuno
- **직무:** AI Agent Engineer
- **근무지:** Seoul / Hybrid
- **고용형태:** Full-time

채용공고:

https://iyuno.wd3.myworkdayjobs.com/careers/job/seoul/ai-agent-engineer_jr101122

### 주요 요구사항

- LLM 기반 AI Agent 설계 및 개발
- RAG 검색 및 응답 생성
- Tool Calling
- 외부 API 연동
- Multi-step Workflow
- 평가 및 피드백
- Latency / Reliability 개선

---

## 2. 프로젝트 개요

이 프로젝트는 보안 및 AI 관련 공개 문서를 검색하고, 질문 유형에 따라 적절한 도구를 선택해 답변하는 AI Agent입니다.

### 주요 기능

- NIST / OWASP 공개 문서 기반 RAG
- PDF 문서 수집 및 Text Chunking
- Sentence Transformer Embedding
- FAISS Vector Search
- Qwen 기반 답변 생성
- 검색 근거 Source 제공
- Calculator Tool Calling
- NIST NVD CVE API 연동
- 질문 유형별 Agent Routing
- Multi-step Workflow
- Failure Handling
- 정량 평가 및 Error Analysis
- pytest 자동 테스트
- GitHub Actions CI
- Streamlit 웹 데모

---

## 3. 시스템 구조

```text
사용자 질문
     |
     v
SecurityAgent
     |
     v
   Router
  /   |   \
 /    |    \
Calculator NVD API Policy RAG
                  |
                  v
                FAISS
                  |
                  v
           관련 문서 검색
                  |
                  v
         Qwen2.5-1.5B
                  |
                  v
          답변 + Sources
```

---

## 4. 기술 스택

| 구분 | 기술 |
|---|---|
| Language | Python |
| LLM | Qwen2.5-1.5B-Instruct |
| Embedding | all-MiniLM-L6-v2 |
| Vector Search | FAISS |
| RAG | Sentence Transformers + FAISS |
| External API | NIST NVD API |
| Web UI | Streamlit |
| Testing | pytest |
| CI | GitHub Actions |
| PDF Parsing | PyMuPDF |

---

## 5. Knowledge Base

총 **20개의 공개 보안 및 AI 문서**를 사용했습니다.

주요 문서 출처는 NIST와 OWASP입니다.

### 데이터 처리 결과

- 문서 수: **20개**
- 전체 PDF 페이지: **2,517 페이지**
- 생성 Chunk: **10,871개**
- Embedding Dimension: **384**
- Vector Search: **FAISS**
- Generator: **Qwen2.5-1.5B-Instruct**

문서별 메타데이터:

```text
data/metadata.csv
```

---

## 6. Agent Tools

### Calculator

사용자의 계산 질문을 감지하면 Calculator Tool을 실행합니다.

Python의 위험한 `eval()`을 직접 사용하지 않고 AST 기반 허용 연산 방식으로 구현했습니다.

예시:

```text
Calculate 125 * 48
```

결과:

```text
6000
```

---

### NIST NVD API

CVE 관련 질문이 입력되면 NIST National Vulnerability Database API를 호출합니다.

예시:

```text
What is CVE-2026-15144?
```

Agent는 CVE ID를 추출하고 NVD API를 통해 취약점 정보를 조회합니다.

---

### Policy RAG

보안 정책이나 기술 문서 관련 질문은 RAG Pipeline으로 전달됩니다.

예시:

```text
What does NIST recommend for zero trust access control?
```

FAISS를 통해 관련 문서를 검색하고 Qwen이 검색 Context를 기반으로 답변을 생성합니다.

---

## 7. Agent Routing

질문의 유형을 분석하여 다음 Tool 중 하나를 선택합니다.

```text
calculator
nvd_api
policy_rag
```

이를 통해 하나의 Agent가 서로 다른 유형의 요청을 처리할 수 있도록 구현했습니다.

---

## 8. Multi-step Workflow

단순 Tool 실행뿐만 아니라 여러 단계를 연결하는 Workflow도 구현했습니다.

예:

```text
CVE 질문
   ↓
CVE ID 추출
   ↓
NVD API 호출
   ↓
관련 보안 문서 검색
   ↓
Qwen 답변 생성
```

Agent 실행 과정에는 Latency와 Retrieval Count도 기록됩니다.

---

## 9. 평가

총 **30문항의 평가 데이터셋**을 구성했습니다.

평가 항목은 다음과 같습니다.

- RAG Retrieval
- Citation
- Tool Selection
- Multi-step Workflow
- Context
- Failure Handling

### 평가 결과

| 평가 항목 | 결과 |
|---|---:|
| Recall@5 | 100.0% |
| Tool Selection Accuracy | 100.0% |
| Citation Success Rate | 100.0% |
| Faithfulness Proxy | 78.1% |
| Multi-step Success Rate | 100.0% |
| Failure Handling Rate | 100.0% |

평가 결과 파일:

```text
evaluation/metrics.json
evaluation/evaluation_metrics.png
evaluation/error_analysis.md
```

> 100% 결과는 본 프로젝트에서 구성한 평가 데이터셋 기준이며, 모든 질문에 대한 일반적인 정확도 100%를 의미하지 않습니다.

---

## 10. Faithfulness 평가

생성된 답변이 검색된 Context에 의해 실제로 뒷받침되는지 확인하기 위해 Faithfulness Proxy 평가를 수행했습니다.

결과:

```text
지원되는 Claim: 25 / 32
Faithfulness Proxy: 78.1%
```

총 32개의 Claim 중 7개는 검색 Context에서 충분한 근거를 확인하지 못했습니다.

이를 숨기지 않고 Error Analysis에 기록했습니다.

### 현재 확인된 한계

- Top-5 검색 결과에 필요한 정보가 포함되지 않을 수 있음
- PDF Header / Footer가 검색 품질에 영향을 줄 수 있음
- Dense Retrieval만 사용하고 있음
- Reranker를 사용하지 않음
- LLM이 검색 Context보다 넓은 내용을 생성할 가능성이 있음

향후 개선 방향:

- Hybrid Search
- Cross Encoder Reranking
- PDF 전처리 개선
- Claim-level Citation Verification

---

## 11. 자동 테스트

pytest를 이용해 Agent 주요 기능에 대한 자동 테스트를 구현했습니다.

현재 결과:

```text
20 passed
```

테스트 항목:

- Calculator 정상 계산
- 위험한 Calculator 입력 차단
- Agent Routing
- NVD 질문 Routing
- Policy 질문 Routing
- Citation Format
- 중복 Citation 제거
- 잘못된 Tool 처리
- 빈 질문 처리
- Failure Handling

테스트 실행:

```bash
python -m pytest tests -v
```

---

## 12. GitHub Actions CI

GitHub Actions를 이용해 자동 테스트 Workflow를 구성했습니다.

Workflow 파일:

```text
.github/workflows/test.yml
```

GitHub Repository에 Push하면 pytest 테스트가 자동으로 실행됩니다.

---

## 13. Streamlit Demo

Streamlit을 이용해 실제로 사용할 수 있는 Web UI를 구현했습니다.

실행:

```bash
streamlit run app/streamlit_app.py
```

웹 화면에서 다음 내용을 확인할 수 있습니다.

- 사용자 질문 입력
- Agent Route
- 선택된 Tool
- 답변
- 검색 Source
- 실행 Latency
- Execution Details

---

## 14. 설치 방법

Python 3.11 환경을 권장합니다.

```bash
git clone https://github.com/HOJUN1000/iyuno-agent-portfolio.git

cd iyuno-agent-portfolio

pip install -r requirements.txt
```

첫 실행 시 Hugging Face Model 다운로드가 필요할 수 있습니다.

GPU 사용을 권장하지만 CPU에서도 실행 가능합니다.

---

## 15. 프로젝트 구조

```text
iyuno-agent-portfolio/
├── app/
│   └── streamlit_app.py
│
├── data/
│   ├── metadata.csv
│   └── processed/
│       ├── chunks_v2.json
│       └── faiss_v2.index
│
├── evaluation/
│   ├── questions.json
│   ├── metrics.json
│   ├── evaluation_metrics.png
│   ├── error_analysis.md
│   └── agent_execution_logs.jsonl
│
├── src/
│   ├── agent/
│   │   ├── router.py
│   │   ├── generator.py
│   │   └── security_agent.py
│   │
│   ├── retrieval/
│   │   ├── retriever.py
│   │   └── citation.py
│   │
│   ├── tools/
│   │   ├── calculator.py
│   │   └── nvd.py
│   │
│   └── ingestion/
│
├── tests/
│   ├── test_agent.py
│   ├── test_citation.py
│   └── test_tools.py
│
├── .github/
│   └── workflows/
│       └── test.yml
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 16. 채용공고 요구사항과 구현 Mapping

| Iyuno 요구사항 | 프로젝트 구현 |
|---|---|
| LLM 기반 AI Agent | SecurityAgent + Qwen |
| RAG 검색 / 응답 | MiniLM + FAISS + Qwen |
| Tool Calling | Calculator / NVD / Policy RAG |
| API Integration | NIST NVD REST API |
| Multi-step Workflow | Router → Tool → Retrieval → Generation |
| 평가 및 Feedback | 30문항 평가 + Error Analysis |
| Reliability | Failure Handling + pytest |
| Latency 확인 | Agent Execution Logging |
| 실제 Demo | Streamlit Web Application |

---

## 17. 데이터 및 출처

원본 PDF는 Repository 용량과 재배포 문제를 고려하여 GitHub에 직접 포함하지 않습니다.

대신 각 문서의 다음 정보를 `data/metadata.csv`에 기록합니다.

- Document ID
- 문서명
- 기관
- Version
- Published Date
- Source URL
- Usage Terms
- Collection Date

---

## 18. 현재 한계

현재 프로젝트에는 다음과 같은 한계가 있습니다.

- Faithfulness 평가는 Embedding Similarity 기반 Proxy 방식
- Claim-level Citation 검증은 아직 구현되지 않음
- Dense Retrieval만 사용
- 별도의 Reranker 없음
- 평가 데이터셋 규모가 제한적임
- NVD API는 외부 서비스 상태에 영향을 받음
- GPU가 없을 경우 Qwen 추론 속도가 느릴 수 있음
- 현재 Agent는 기본적으로 Single-turn 중심으로 구성됨

---

## 19. 프로젝트 결과

현재 구현 완료 항목:

- RAG Pipeline
- 20개 공개 문서 Knowledge Base
- FAISS Vector Search
- Qwen Answer Generation
- Tool Calling
- NVD API Integration
- Agent Routing
- Multi-step Workflow
- Failure Handling
- 30문항 Evaluation
- Error Analysis
- pytest 20개 테스트 통과
- GitHub Actions 설정
- Streamlit Web Demo

이 프로젝트는 실제 AI Agent Engineer 채용공고의 요구사항을 분석하고, 이를 실행 가능한 GitHub 프로젝트로 구현하는 것을 목표로 제작했습니다.
