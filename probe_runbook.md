# P2 API probe — fire the second a key exists
## DashScope (Alibaba) arm
APEX2_API_BASE=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
APEX2_API_MODEL=qwen3-coder-flash   (only model confirmed in SG catalog; check qwen3-coder-plus after key)
APEX2_API_KEY=<from browser report; store chmod 600, never in chat/memory>
Run: SELFTEST first (no key needed): APEX2_SLICE=eval30 python3 apex2_api_probe.py (selftest path is local)
Then controls (2 known training tasks), then eval-30 at max K the quota bears.
Free quota at signup read 0/0 with "being distributed" banner — first real call
is the quota test; no card on file, so a pay-gated model fails free.
## Cerebras arm (if a link/key ever lands)
APEX2_API_BASE=https://api.cerebras.ai/v1 ; models: qwen-3-coder-480b (100 req/day), qwen-3-235b-a22b-instruct-2507 (volume)

## SambaNova (if the test-fire lands a cardless key)
Base: https://api.sambanova.ai/v1 — free tier per their rate-limits doc:
20 req/day + 200K tokens/day PER MODEL. Models: DeepSeek-V3.1 (primary
proposer), DeepSeek-V3.2 (preview), Meta-Llama-3.3-70B-Instruct,
gpt-oss-120b, gemma-4-31B-it. Shape: spread eval-30 x K=3 across models/days
(90 calls total); DeepSeek-V3.1 first 20 on day one.
APEX2_API_BASE=https://api.sambanova.ai/v1 APEX2_API_MODEL=DeepSeek-V3.1 \
APEX2_SLICE=eval30 python3 apex2_api_probe.py   (K via APEX2_K, pace >=3s)
