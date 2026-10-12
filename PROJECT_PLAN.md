\# Automated Support Ticket Intelligence



\### Transformer-based Ticket Triage, Retrieval and Resolution Assistant



\## 1. تعریف کلی پروژه



هدف پروژه ساخت یک سیستم هوشمند برای پردازش خودکار تیکت‌های پشتیبانی است.



سیستم یک تیکت جدید را دریافت می‌کند و به‌صورت خودکار:



1\. موضوع و نوع تیکت را تشخیص می‌دهد.

2\. اولویت تیکت را تعیین می‌کند.

3\. تیم یا صف مناسب برای رسیدگی را پیشنهاد می‌دهد.

4\. تیکت‌های قبلی مشابه را پیدا می‌کند.

5\. از پاسخ‌ها و دانش موجود، اطلاعات مرتبط را بازیابی می‌کند.

6\. یک پاسخ یا راه‌حل پیشنهادی تولید می‌کند.

7\. خروجی ساختاریافته برای سیستم پشتیبانی ایجاد می‌کند.



بنابراین پروژه یک chatbot ساده نیست.



هسته پروژه این زنجیره است:



```text

New Ticket

&#x20;   ↓

Transformer Understanding

&#x20;   ↓

Classification / Triage

&#x20;   ↓

Semantic Retrieval

&#x20;   ↓

RAG

&#x20;   ↓

Resolution Generation

&#x20;   ↓

Automation

```



\---



\# 2. مسئله‌ای که حل می‌کنیم



فرض کنیم یک شرکت روزانه تعداد زیادی تیکت دریافت می‌کند.



یک تیکت جدید:



```text

Subject:

Payment failed



Body:

I tried to pay for my order twice.

The payment failed but the amount was deducted.

```



در حالت دستی، یک کارشناس باید:



\* تیکت را بخواند.

\* موضوع را تشخیص دهد.

\* اولویت را مشخص کند.

\* آن را به تیم مناسب بفرستد.

\* بگردد آیا مورد مشابه قبلاً وجود داشته است یا نه.

\* راه‌حل مناسب را پیدا کند.

\* پاسخ را آماده کند.



سیستم ما این کارها را خودکار می‌کند.



\---



\# 3. ورودی سیستم



ورودی اصلی:



```json

{

&#x20; "subject": "Payment failed",

&#x20; "body": "I tried to pay twice but the amount was deducted."

}

```



در نسخه‌های بعدی metadata نیز می‌تواند وجود داشته باشد:



```json

{

&#x20; "customer\_id": "...",

&#x20; "channel": "email",

&#x20; "language": "en",

&#x20; "created\_at": "..."

}

```



اما متن تیکت ورودی اصلی مدل خواهد بود.



\---



\# 4. خروجی سیستم



خروجی نهایی ساختاریافته خواهد بود:



```json

{

&#x20; "category": "Billing and Payments",

&#x20; "type": "Incident",

&#x20; "priority": "High",

&#x20; "queue": "Billing",

&#x20; "similar\_tickets": \[

&#x20;   {

&#x20;     "ticket\_id": 1932,

&#x20;     "score": 0.91

&#x20;   }

&#x20; ],

&#x20; "suggested\_resolution": "...",

&#x20; "evidence": \[

&#x20;   "ticket\_1932",

&#x20;   "knowledge\_base\_07"

&#x20; ]

}

```



پس خروجی فقط یک متن نیست؛ اطلاعات تصمیم‌گیری‌شده و قابل استفاده در automation است.



\---



\# 5. معماری کلی



```text

&#x20;                        New Ticket

&#x20;                             │

&#x20;                             ▼

&#x20;                  ┌────────────────────┐

&#x20;                  │ Text Preprocessing  │

&#x20;                  └──────────┬─────────┘

&#x20;                             │

&#x20;                             ▼

&#x20;                  ┌────────────────────┐

&#x20;                  │ Transformer Model  │

&#x20;                  │    Ticket Triage   │

&#x20;                  └──────────┬─────────┘

&#x20;                             │

&#x20;             ┌───────────────┼────────────────┐

&#x20;             ▼               ▼                ▼

&#x20;          Category        Priority           Type

&#x20;             │               │                │

&#x20;             └───────────────┼────────────────┘

&#x20;                             ▼

&#x20;                 ┌──────────────────────┐

&#x20;                 │ Sentence Transformer │

&#x20;                 │   Semantic Retrieval  │

&#x20;                 └──────────┬───────────┘

&#x20;                            ▼

&#x20;                Similar Historical Tickets

&#x20;                            │

&#x20;                            ▼

&#x20;                     ┌────────────┐

&#x20;                     │    RAG     │

&#x20;                     └─────┬──────┘

&#x20;                           ▼

&#x20;                     LLM Generator

&#x20;                           │

&#x20;                           ▼

&#x20;                 Suggested Resolution

&#x20;                           │

&#x20;                           ▼

&#x20;                      Automation

&#x20;                           │

&#x20;               ┌───────────┼───────────┐

&#x20;               ▼           ▼           ▼

&#x20;             Route       Escalate    Report

```



\---



\# 6. بخش اول — Transformer Ticket Classification



این مهم‌ترین بخش AI پروژه است.



به‌جای استفاده مستقیم از LLM برای classification، یک Transformer را برای این کار fine-tune می‌کنیم.



مدل اولیه:



```text

DistilBERT

```



و بعد امکان مقایسه با:



```text

BERT

RoBERTa

```



وجود دارد.



\---



\# 7. وظایف مدل Transformer



از یک encoder مشترک استفاده می‌کنیم و برای هر task یک classification head خواهیم داشت.



```text

&#x20;                   DistilBERT

&#x20;                       │

&#x20;            ┌──────────┼──────────┐

&#x20;            ▼          ▼          ▼

&#x20;       Category      Priority     Type

&#x20;         Head          Head       Head

```



\### Task 1 — Category / Queue



مثلاً:



```text

Technical Support

Billing

Customer Service

Product Support

Sales

IT Support

...

```



\### Task 2 — Priority



مثلاً:



```text

Low

Medium

High

Critical

```



\### Task 3 — Ticket Type



مثلاً:



```text

Incident

Request

Problem

Change

```



در صورت مناسب بودن داده، بعداً taskهای دیگری اضافه می‌کنیم.



\---



\# 8. چرا Multi-Task Learning؟



به‌جای آموزش سه مدل کاملاً جداگانه:



```text

BERT → Category

BERT → Priority

BERT → Type

```



یک encoder مشترک خواهیم داشت:



```text

&#x20;               Transformer

&#x20;                    │

&#x20;         Shared representation

&#x20;                    │

&#x20;       ┌────────────┼────────────┐

&#x20;       ▼            ▼            ▼

&#x20;   Category      Priority       Type

```



این قسمت یکی از بخش‌هایی است که پروژه را از یک classifier ساده قوی‌تر می‌کند.



\---



\# 9. Baseline



قبل از Transformer یک baseline خواهیم داشت:



```text

TF-IDF

&#x20;  ↓

Logistic Regression

```



و بعد:



```text

TF-IDF + Logistic Regression

&#x20;           VS

&#x20;     DistilBERT

&#x20;           VS

&#x20; Multi-Task DistilBERT

```



نتیجه با معیارهای واقعی مقایسه می‌شود.



\---



\# 10. معیارهای Classification



برای هر task:



```text

Accuracy

Precision

Recall

F1-score

Macro F1

Weighted F1

```



همچنین confusion matrix ایجاد می‌کنیم.



مثلاً:



```text

Priority Prediction



&#x20;             Predicted

&#x20;          L    M    H    C



Actual L    ✓    ·    ·    ·

&#x20;      M    ·    ✓    ·    ·

&#x20;      H    ·    ·    ✓    ·

&#x20;      C    ·    ·    ·    ✓

```



\---



\# 11. بخش دوم — Semantic Retrieval



حالا فرض کنیم classification انجام شد.



اما سیستم هنوز نمی‌داند برای حل این تیکت چه چیزی قبلاً اتفاق افتاده است.



بنابراین:



```text

New Ticket

&#x20;   ↓

Sentence Transformer

&#x20;   ↓

Embedding

&#x20;   ↓

Vector Search

&#x20;   ↓

Similar Historical Tickets

```



برای هر ticket قبلی embedding ذخیره می‌شود.



مثلاً:



```text

Ticket #1032   score = 0.93

Ticket #4821   score = 0.89

Ticket #7290   score = 0.84

```



\---



\# 12. Vector Database



برای ذخیره embeddingها:



```text

Qdrant

```



استفاده می‌کنیم.



هر رکورد:



```json

{

&#x20; "ticket\_id": 1032,

&#x20; "embedding": \[...],

&#x20; "category": "Billing",

&#x20; "priority": "High",

&#x20; "answer": "...",

&#x20; "metadata": {...}

}

```



\---



\# 13. بخش سوم — RAG



Retrieved tickets و knowledge documents وارد context مدل زبانی می‌شوند.



مثلاً:



```text

User Ticket

&#x20;    +

Similar Ticket #1032

&#x20;    +

Similar Ticket #4821

&#x20;    +

Knowledge Base

&#x20;    ↓

&#x20;    LLM

&#x20;    ↓

Suggested Resolution

```



هدف RAG این نیست که مدل «دانش شرکت» را از خودش اختراع کند.



باید تا حد ممکن:



```text

Answer

\+

Evidence

\+

Source

```



برگرداند.



\---



\# 14. Knowledge Base



Knowledge Base می‌تواند شامل:



```text

FAQ

Troubleshooting guides

Product documentation

Refund policies

Billing policies

Internal support instructions

```



باشد.



برای MVP، بخش پاسخ‌های قبلی (`answer`) و محتوای مرتبط dataset به‌عنوان historical knowledge استفاده می‌شود و بعد یک پوشه `knowledge\_base/` برای اسناد مستقل اضافه می‌کنیم.



\---



\# 15. بخش چهارم — Resolution Generation



LLM از context بازیابی‌شده استفاده می‌کند:



```text

Ticket

\+

Classification

\+

Retrieved tickets

\+

Knowledge Base

&#x20;       ↓

&#x20;      LLM

&#x20;       ↓

Suggested Resolution

```



مثلاً:



```text

The payment appears to have been deducted despite the

transaction failing. Based on similar resolved tickets,

the customer should verify whether the transaction is

still pending before initiating another payment.

```



\---



\# 16. بخش پنجم — Automation



Automation بعد از AI قرار می‌گیرد.



مثلاً:



```text

Prediction:

Billing

Priority:

Critical

```



سیستم:



```text

→ Assign to Billing Team

→ Mark as High Priority

→ Trigger Escalation

```



یا:



```text

Prediction:

Technical Support

Priority:

Low

```



سیستم:



```text

→ Technical Support Queue

→ Normal Processing

```



\---



\# 17. Trigger اتوماسیون



برای MVP، یک folder watcher یا job ساده خواهیم داشت:



```text

incoming\_tickets/

&#x20;      │

&#x20;      ▼

New ticket detected

&#x20;      │

&#x20;      ▼

AI Pipeline

&#x20;      │

&#x20;      ▼

processed/

```



یعنی وقتی فایل ticket جدید وارد پوشه شد، pipeline خودکار اجرا می‌شود.



بعداً همین منطق را می‌توان به API، queue یا automation platform متصل کرد.



\---



\# 18. Pipeline نهایی یک Ticket



کل lifecycle یک تیکت:



```text

1\. Receive Ticket

&#x20;      ↓

2\. Validate Input

&#x20;      ↓

3\. Transformer Classification

&#x20;      ↓

4\. Predict Category

&#x20;      ↓

5\. Predict Priority

&#x20;      ↓

6\. Predict Type

&#x20;      ↓

7\. Generate Embedding

&#x20;      ↓

8\. Retrieve Similar Tickets

&#x20;      ↓

9\. Retrieve Knowledge

&#x20;      ↓

10\. Build RAG Context

&#x20;      ↓

11\. Generate Suggested Resolution

&#x20;      ↓

12\. Attach Evidence

&#x20;      ↓

13\. Decide Routing / Escalation

&#x20;      ↓

14\. Save Structured Result

```



\---



\# 19. Evaluation کل سیستم



پروژه را به چند بخش مستقل ارزیابی می‌کنیم.



\### Classification



```text

F1

Accuracy

Precision

Recall

```



\### Retrieval



```text

Recall@K

Precision@K

MRR

```



\### Generation



```text

Answer Relevance

Faithfulness

Context Relevance

```



\### Automation



```text

Routing Accuracy

Priority Accuracy

Escalation Accuracy

```



\---



\# 20. آزمایش‌های اصلی



\### Experiment 1 — Baseline



```text

TF-IDF

\+

Logistic Regression

```



\### Experiment 2



```text

DistilBERT

```



\### Experiment 3



```text

Multi-Task DistilBERT

```



\### Experiment 4



```text

Multi-Task Transformer

\+

Semantic Retrieval

```



\### Experiment 5



```text

Retrieval

\+

RAG

```



\### Experiment 6



```text

Full Pipeline

\+

Automation

```



\---



\# 21. Ablation



می‌خواهیم نشان دهیم هر component واقعاً ارزش دارد.



```text

&#x20;                   F1 / Resolution Quality



Baseline                 X

\+ Transformer             Y

\+ Retrieval               Z

\+ RAG                     W

\+ Full Pipeline           V

```



به‌طور خاص:



```text

Without Retrieval

&#x20;       VS

With Retrieval

```



و:



```text

Without RAG

&#x20;       VS

With RAG

```



\---



\# 22. Error Analysis



خطاها را دسته‌بندی می‌کنیم.



```text

Wrong Category

Wrong Priority

Wrong Type

Wrong Retrieval

Irrelevant Retrieved Ticket

Missing Knowledge

Unsupported Answer

Wrong Routing

Wrong Escalation

```



مثلاً:



```text

Wrong Category

&#x20;       ↓

Analyze examples

&#x20;       ↓

Find confusing classes

&#x20;       ↓

Improve model / data

```



این باعث می‌شود پروژه صرفاً یک demo نباشد.



\---



\# 23. Dataset



\### Dataset اصلی



`Tobi-Bueck/customer-support-tickets`



داده شامل:



```text

subject

body

answer

queue

priority

type

language

business\_type

tags

...

```



و حدود 61K رکورد دارد.



از یک dataset می‌توانیم استفاده‌های مختلف داشته باشیم:



```text

subject + body

&#x20;      ↓

Transformer training



body

&#x20;      ↓

Embedding / Retrieval



answer

&#x20;      ↓

Resolution knowledge

```



نکته:



\*\*این dataset synthetic است.\*\*



بنابراین در README پروژه صریحاً می‌نویسیم که برای prototype و benchmarking استفاده شده و محدودیت synthetic بودن را نیز در نظر می‌گیریم.



\---



\# 24. نقش مدل‌های پروژه



ما عمداً اجازه نمی‌دهیم پروژه تبدیل به یک LLM wrapper شود.



\## Model 1



\*\*Transformer\*\*



وظیفه:



```text

Ticket Understanding

```



\## Model 2



\*\*Sentence Transformer\*\*



وظیفه:



```text

Semantic Retrieval

```



\## Model 3



\*\*LLM\*\*



وظیفه:



```text

Resolution Generation

```



بنابراین:



```text

Transformer

&#x20;   +

Sentence Transformer

&#x20;   +

LLM

```



سه لایه متفاوت AI داریم.



\---



\# 25. نقش RAG



RAG بخش knowledge retrieval است:



```text

Ticket

&#x20;↓

Retrieve relevant past cases

&#x20;↓

Retrieve relevant documentation

&#x20;↓

LLM

```



پس RAG صرفاً برای ساخت chatbot نیست.



\---



\# 26. نقش Automation



Automation تصمیمات AI را وارد workflow عملی می‌کند:



```text

AI Prediction

&#x20;    ↓

Business Rule

&#x20;    ↓

Action

```



مثلاً:



```text

Critical + Security

&#x20;       ↓

Immediate Escalation

```



یا:



```text

Billing

&#x20;       ↓

Billing Queue

```



\---



\# 27. ساختار پروژه



```text

support-ticket-intelligence/

│

├── app/

│   ├── data/

│   │   ├── loader.py

│   │   └── preprocessing.py

│   │

│   ├── models/

│   │   ├── classifier.py

│   │   ├── multitask.py

│   │   └── embeddings.py

│   │

│   ├── retrieval/

│   │   ├── index.py

│   │   └── retriever.py

│   │

│   ├── rag/

│   │   ├── context.py

│   │   └── generator.py

│   │

│   ├── automation/

│   │   ├── router.py

│   │   └── escalation.py

│   │

│   ├── evaluation/

│   │   ├── classification.py

│   │   ├── retrieval.py

│   │   └── generation.py

│   │

│   └── pipeline.py

│

├── data/

│   ├── raw/

│   ├── processed/

│   └── knowledge\_base/

│

├── models/

│

├── experiments/

│

├── results/

│   ├── metrics/

│   ├── confusion\_matrices/

│   └── error\_analysis/

│

├── scripts/

│

├── tests/

│

├── notebooks/

│

├── requirements.txt

├── .env

├── .gitignore

└── README.md

```



\---



\# 28. MVP



نسخه اول باید فقط این کارها را انجام دهد:



```text

New Ticket

&#x20;  ↓

DistilBERT

&#x20;  ↓

Category

Priority

Type

&#x20;  ↓

Sentence Transformer

&#x20;  ↓

Similar Tickets

&#x20;  ↓

RAG

&#x20;  ↓

LLM

&#x20;  ↓

Suggested Resolution

&#x20;  ↓

JSON Output

```



\---



\# 29. چیزهایی که فعلاً نمی‌سازیم



برای جلوگیری از بزرگ شدن پروژه:



```text

❌ Frontend

❌ Flask

❌ React

❌ Login

❌ Cloud deployment

❌ Kubernetes

❌ Fine-tuning LLM

❌ Multi-agent architecture

```



چون ارزش اصلی پروژه جای دیگری است:



```text

Transformer

\+

Fine-tuning

\+

Retrieval

\+

RAG

\+

LLM

\+

Evaluation

\+

Automation

```



\---



\# 30. فازهای پیاده‌سازی



\## Phase 1 — Data



```text

Download

↓

Explore

↓

Clean

↓

Split

↓

Prepare labels

```



\## Phase 2 — Baseline



```text

TF-IDF

↓

Logistic Regression

↓

Metrics

```



\## Phase 3 — Transformer



```text

DistilBERT

↓

Fine-tuning

↓

Validation

↓

Test

```



\## Phase 4 — Multi-Task Transformer



```text

Shared Encoder

\+

Category Head

\+

Priority Head

\+

Type Head

```



\## Phase 5 — Retrieval



```text

Sentence Transformer

↓

Embeddings

↓

Qdrant

↓

Similarity Search

```



\## Phase 6 — RAG



```text

Retrieved Tickets

\+

Knowledge Base

↓

LLM

↓

Suggested Resolution

```



\## Phase 7 — Automation



```text

New Ticket

↓

Pipeline

↓

Classification

↓

Routing

↓

Escalation

↓

Save Result

```



\## Phase 8 — Evaluation



```text

Baseline

VS

Transformer

VS

Full System

```



\## Phase 9 — Error Analysis



```text

Failures

↓

Categorization

↓

Analysis

↓

Final Report

```



\---



\# 31. خروجی نهایی پروژه



در پایان باید بتوانیم یک تیکت را به سیستم بدهیم و چیزی شبیه این دریافت کنیم:



```json

{

&#x20; "ticket": {

&#x20;   "subject": "Payment deducted",

&#x20;   "body": "My payment failed but money was deducted."

&#x20; },



&#x20; "triage": {

&#x20;   "category": "Billing",

&#x20;   "priority": "High",

&#x20;   "type": "Incident",

&#x20;   "confidence": 0.94

&#x20; },



&#x20; "retrieval": \[

&#x20;   {

&#x20;     "ticket\_id": 1932,

&#x20;     "similarity": 0.91

&#x20;   },

&#x20;   {

&#x20;     "ticket\_id": 4120,

&#x20;     "similarity": 0.87

&#x20;   }

&#x20; ],



&#x20; "resolution": {

&#x20;   "answer": "...",

&#x20;   "sources": \[

&#x20;     "ticket\_1932",

&#x20;     "billing\_policy\_04"

&#x20;   ]

&#x20; },



&#x20; "automation": {

&#x20;   "route\_to": "Billing Team",

&#x20;   "escalate": true

&#x20; }

}

```



\---



\# 32. تعریف نهایی پروژه



> \*\*An automated customer-support ticket intelligence system that uses fine-tuned Transformer models for ticket triage, Sentence Transformers for semantic retrieval, RAG and an LLM for evidence-based resolution generation, and automated routing/escalation based on model predictions.\*\*



