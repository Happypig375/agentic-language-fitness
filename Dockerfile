FROM mcr.microsoft.com/dotnet/sdk:10.0.302

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
COPY . .
ENV PYTHONPATH=/workspace/src
ENTRYPOINT ["python3", "scripts/alf.py"]
CMD ["doctor", "--strict"]
