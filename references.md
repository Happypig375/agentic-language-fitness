# References and starting points

This is a working bibliography, not a claim that every source directly tests the full hypothesis.

## Agent cost and language

- **The Best Programming Language for Tokenmaxxing** (2026)  
  https://arxiv.org/abs/2607.22807  
  Directly studies programming-language effects on coding-agent token cost and full trajectories.

## Repository-scale context

- **LongCodeBench** (2025)  
  https://arxiv.org/abs/2505.07897  
  Repository/long-context coding benchmark; useful for the claim that effective performance degrades with larger required contexts.

- **LongCodeZip** (2025)  
  https://arxiv.org/abs/2510.00446  
  Structure/relevance-aware code-context compression.

## Tokenization and source representation

- **TokDrift** (ACL 2026)  
  https://aclanthology.org/2026.acl-long.2199/  
  Studies behavior changes from tokenization differences in semantically equivalent programs.

- **Token Sugar: Making Source Code Sweeter for LLMs through Token-Efficient Shorthand** (ASE 2025)  
  https://arxiv.org/abs/2512.08266  
  Learns reversible shorthand for frequent code patterns while preserving code-generation performance.

## Multilingual code generation / transfer

- **MultiPL-E**  
  https://github.com/nuprl/MultiPL-E  
  Parallel multilingual execution-tested code-generation benchmark infrastructure.

- **Knowledge Transfer from High-Resource to Low-Resource Programming Languages for Code LLMs (MultiPL-T)**  
  Search via Microsoft Research / paper index; relevant to language familiarity and transfer controls.

## Static feedback / repair

- **CoCoGen: Code Context Generation for Large Language Models with Static Analysis** (2024)  
  https://arxiv.org/abs/2403.16792  
  Relevant to compiler/static-analysis feedback improving project-context code generation.

## F# / agentic programming context

- Don Syme / GitHub Next profile  
  https://githubnext.com/people/dsyme/

- Don Syme, **On Specifications, Software and Tools / Intent-Actualisation Toolchains** (2025)  
  https://dsyme.net/2025/09/24/on-specifications-software-and-tools/

- Don Syme, **What Kind of Programming is Natural Language Programming?** (2025)  
  https://dsyme.net/2025/09/02/what-kind-of-programming-is-natural-language-programming/

## Corpus proxies

- **The Stack v3** statistics  
  https://huggingface.co/datasets/HuggingFaceCode/stack-v3-train  
  Useful as an open-source corpus proxy; do not treat it as disclosure of any proprietary model's training mixture.

## Notes for literature review

Future review should distinguish:

1. one-shot code generation;
2. agent trajectory cost;
3. repository comprehension;
4. compiler/tool feedback;
5. tokenizer efficiency;
6. source-code maintainability;
7. longitudinal/fresh-context maintenance.

The central project question sits at the intersection of these literatures rather than being answered by any one of them.
