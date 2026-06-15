---
name: queries-generator
description: Use when the user wants to generate Google Scholar search queries from a codebase, create a queries.txt for Parmesano, analyze a project to produce research paper topics, build a literature review query list from source code, or extract scientific concepts from an implementation.
---

# Queries Generator

Analyze a codebase and generate 100 combined academic search queries ready for
Parmesano (Google Scholar). The queries bridge concrete implementations to their
scientific foundations.

## When to use

- "Generate queries for this project"
- "Create a queries.txt from this codebase"
- "What papers should I read for this code?"
- "Analyze this repo and give me scholar queries"
- "Build literature review queries from this implementation"

## Pipeline

```
Codebase → [Step 1: Scan] → [Step 2: Extract] → [Step 3: Expand] → [Step 4: Form] → queries.txt
```

---

## Step 1: Scan the Codebase

Read these files in priority order. Extract every identifiable technique, algorithm,
framework, architecture pattern, and hyperparameter choice.

### Priority files

| Priority | Files | What to extract |
|----------|-------|-----------------|
| 1 | `README.md`, docs/ | Project purpose, algorithms, architecture |
| 2 | `requirements.txt`, `package.json`, `Cargo.toml`, `pyproject.toml` | Dependencies, frameworks |
| 3 | Source files (`*.py`, `*.js`, `*.rs`, etc.) | Imports, model layers, training loops, optimizers |
| 4 | Config files (`*.yaml`, `*.json`, `*.toml`) | Hyperparameters, architecture config, loss functions |

To scan efficiently, use glob patterns. Don't read every file — read key ones and
search imports/patterns across the rest.

### Read with these priorities

1. First read `README.md` and dependency files — broad understanding
2. Search source files for imports and key API calls (use Grep for patterns)
3. Read the most important source files (model definitions, training loops, main modules)
4. Read config files for hyperparameters

---

## Step 2: Layer 1 — Technical Extraction

Identify every concrete technique **actually used** in the code. Go beyond
dependency names — extract what specific APIs, architectures, and methods are
called.

### Extraction rules

- **Don't** just list package names (`torch`, `numpy`, `tensorflow`)
- **Do** extract what those packages are used for
- Read model architecture definitions, training loops, data pipelines
- Identify layer types, activation functions, loss functions, optimizers
- Note specific configurations (e.g., `Dropout(0.5)`, not just `Dropout`)
- Catch algorithms mentioned in comments or function names

### Examples of good extraction

```
Code: nn.Conv2d(3, 64, 3, stride=2, padding=1)
  → Convolutional Neural Networks, 2D Convolutions, Strided Convolutions, Spatial Downsampling, Feature Extraction

Code: nn.Dropout(0.5)
  → Dropout Regularization, Stochastic Regularization, Overfitting Prevention

Code: nn.BatchNorm2d(64)
  → Batch Normalization, Internal Covariate Shift, Training Stabilization

Code: nn.MultiheadAttention(embed_dim=512, num_heads=8)
  → Multi-Head Self-Attention, Transformer Architecture, Attention Mechanisms, Scaled Dot-Product Attention

Code: optim.Adam(params, lr=1e-4, weight_decay=1e-5)
  → Adam Optimizer, Adaptive Learning Rates, Weight Decay Regularization, AdamW

Code: F.cross_entropy(logits, labels)
  → Cross-Entropy Loss, Softmax Classification, Categorical Loss Functions

Code: lr_scheduler.CosineAnnealingLR(optimizer, T_max=100)
  → Cosine Annealing, Learning Rate Scheduling, Learning Rate Warmup

Code: torch.cuda.amp.autocast()
  → Mixed Precision Training, Automatic Mixed Precision, FP16 Training, Numerical Stability

Code: nn.GRU(input_size=256, hidden_size=512)
  → Gated Recurrent Units, Sequential Modeling, Recurrent Neural Networks, Gate Mechanisms

Code: nn.Embedding(vocab_size, d_model)
  → Word Embeddings, Learned Representations, Embedding Layers, Distributional Semantics

Code: nn.TransformerEncoder / nn.TransformerDecoder
  → Transformer Architecture, Encoder-Decoder Models, Self-Attention, Sequence-to-Sequence
```

### What to ignore

- Utility libraries (`os`, `sys`, `argparse`, `logging`, `tqdm`, `datetime`)
- General infrastructure (`flask`, `fastapi`, `click`) unless it's core to the domain
- I/O and data format libraries (`json`, `csv`, `yaml`) unless processing is the focus
- Linting/testing tools (`pytest`, `black`, `eslint`)

### Organize your findings

Group extracted concepts by affinity:
- **Architecture**: model types, layer types, connections, skip connections, normalization
- **Training**: optimizers, loss functions, learning rate schedules, regularization
- **Data**: augmentations, preprocessing, datasets, transformations
- **Inference**: quantization, pruning, distillation, deployment
- **Domain**: any field-specific algorithms or concepts

---

## Step 3: Layer 2 — Scientific Expansion

For each concept extracted, expand into its **academic neighborhood**. This is the
most important step — you're mapping implementation details to their research papers.

### How to expand

For each concept, ask:
- What is the foundational paper for this technique?
- What are the common variants or alternatives?
- What problem does it solve? (this often yields related concepts)
- What papers compare or improve upon this?
- What theoretical framework does it belong to?

### Expansion examples

| Implementation | Scientific Expansion |
|---------------|----------------------|
| `Dropout` | Dropout Regularization, Stochastic Depth, Monte Carlo Dropout, DropConnect, Variational Dropout, Overfitting Prevention, Neural Network Regularization, Ensemble Averaging |
| `BatchNorm` | Batch Normalization, Internal Covariate Shift, Layer Normalization, Instance Normalization, Group Normalization, Weight Standardization, Normalization-Free Networks |
| `Adam` | Adam Optimizer, Adaptive Learning Rates, AdamW Decoupled Weight Decay, SGD Momentum, Nesterov Accelerated Gradient, RMSprop, Learning Rate Annealing |
| `Transformer` | Transformer Architecture, Self-Attention Mechanism, Multi-Head Attention, Positional Encoding, Attention Is All You Need, Sequence Modeling |
| `Conv2d` | Convolutional Neural Networks, Spatial Feature Extraction, Receptive Fields, Translation Equivariance, Filter Kernels, Depthwise Separable Convolution |
| `CrossEntropyLoss` | Cross-Entropy Loss, Softmax Classification, Label Smoothing, Focal Loss, Class Imbalance, Calibrated Probabilities |
| `ReLU` | Rectified Linear Unit, Activation Functions, Vanishing Gradients, LeakyReLU, GELU, Swish, SiLU, Dead Neurons |
| `Residual connection` | Residual Networks, Skip Connections, Deep Network Training, Highway Networks, DenseNets, Gradient Flow |
| `Momentum` | SGD Momentum, Nesterov Momentum, Accelerated Gradient Descent, Polyak Averaging, Heavy Ball Method |
| `cosine annealing` | Cosine Annealing, Learning Rate Scheduling, Warm Restarts, SGDR, Cyclic Learning Rates, Super-Convergence |
| `mixed precision` | Mixed Precision Training, FP16 Training, Automatic Mixed Precision, Loss Scaling, BFloat16, Numerical Stability |
| `data augmentation` | Data Augmentation, Cutout, Mixup, CutMix, RandAugment, AutoAugment, Training Data Diversity, Invariance Learning |
| `transfer learning` | Transfer Learning, Pretrained Models, Fine-Tuning, Feature Extraction, Domain Adaptation, Few-Shot Learning |
| `early stopping` | Early Stopping, Overfitting Prevention, Validation-Based Stopping, Generalization Gap, Patience |
| `weight decay` | Weight Decay, L2 Regularization, Decoupled Weight Decay, Tikhonov Regularization, Parameter Shrinkage |

### Quality rules

- Every expansion must produce at least 3 and ideally 5-8 related concepts
- All concepts must be academically searchable (appear in real paper titles)
- Cover the full range: foundations, variants, alternatives, improvements
- Include theory when it exists (e.g., "Internal Covariate Shift" for BatchNorm)
- Include related architectures when relevant

---

## Step 4: Form 100 Combined Queries

Take the expanded concept pool and form **exactly 100** combined queries. Write
them to `queries.txt`, one per line.

### Query formation rules

1. **2-4 concepts per line** — enough to be specific, not so many that zero results
2. **Academically coherent** — the combination should read like a plausible paper title or keyword section
3. **No quotes** — let Google Scholar apply its own relevance ranking
4. **No duplicates** — swapped word order is still a duplicate
5. **No near-duplicates** — "Dropout Overfitting" and "Overfitting Dropout" are the same
6. **Diverse coverage** — spread across architecture, training, data, inference, and domain
7. **Specific over generic** — "Stochastic Gradient Descent Momentum Nesterov" over "Optimization"
8. **Bridge implementation to theory** — when a concept has a theoretical foundation, pair them

### Quality checklist per query

- Would a real paper have these terms in its keywords or title?
- Is the combination specific enough to get <100k results on Scholar?
- Are the terms actually related conceptually (not random mashups)?
- Would a researcher in this area recognize the combination as meaningful?

### Example output (first 10 of 100)

```
Dropout Regularization Stochastic Depth Overfitting Prevention
Batch Normalization Internal Covariate Shift Training Stability
Convolutional Neural Networks Feature Extraction Translation Equivariance
Adam Optimizer Adaptive Learning Rates Weight Decay Regularization
Transformer Architecture Multi-Head Attention Positional Encoding
Cross-Entropy Loss Label Smoothing Class Imbalance Calibration
ReLU Activation Function Vanishing Gradients Dead Neurons
Residual Networks Skip Connections Gradient Flow Deep Network Training
Cosine Annealing Learning Rate Scheduling Warm Restarts SGDR
Mixed Precision Training FP16 Loss Scaling Numerical Stability
```

### Output

Write all 100 queries to a file named `queries.txt` in the project root.
One query per line. No numbering, no bullets, no markdown formatting — just
plain text, one query per line.

After writing, tell the user:
```
Done. queries.txt written with 100 queries. Run:
  python -m parmesano -i queries.txt -o results.json --max-results 20
```

---

## Important reminders

- You are extracting from **real implementation details**, not guessing what might be there
- Every concept must be traceable to something actually in the codebase
- The expansion is where you add academic depth — don't skimp here
- 100 queries is the target, but variety and quality matter more than hitting exactly 100
- If the codebase is small, generate fewer but still aim high with deep expansions
