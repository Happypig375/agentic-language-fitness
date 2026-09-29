FROM mcr.microsoft.com/dotnet/sdk:10.0.302

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-venv git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
COPY . .
RUN python3 -m venv /opt/ise-venv \
    && /opt/ise-venv/bin/pip install --no-cache-dir . \
    && mkdir -p /opt/tiktoken-cache \
    && TIKTOKEN_CACHE_DIR=/opt/tiktoken-cache /opt/ise-venv/bin/python -c "import tiktoken; tiktoken.get_encoding('o200k_base')"

ENV PATH=/opt/ise-venv/bin:$PATH \
    PYTHONPATH=/workspace/src \
    PYTHONDONTWRITEBYTECODE=1 \
    TIKTOKEN_CACHE_DIR=/opt/tiktoken-cache
ENTRYPOINT ["/opt/ise-venv/bin/python", "scripts/ise.py"]
CMD ["doctor", "--strict"]
