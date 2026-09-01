# Workstream D v3 remote portability incident (2026-08-31)

The frozen v3 H ledger was staged on an authorized higher-memory Linux/AMD64
host for a model-free preflight. The exact source commit, H manifest, retained
attempt inventories, and image-archive byte hash matched. No authentication,
new attempt, candidate process, or provider/model call was started.

The preflight found two ordinary portability defects:

1. The host's legacy Docker image store exposed the loaded archive by its
   config digest, while the originating containerd store exposed the OCI index
   digest. The archive bytes were identical; a store-specific `.Id` was not a
   portable scientific identity.
2. The remote checkout was owned by UID/GID 1000 while the image's named
   `codex` user was UID/GID 1655, so the container could not write the mounted
   candidate workspace.

The matching image archive is 630,053,888 bytes with SHA-256
`55ee85f0656cef429d1cd40edced79782d54abb7b2180c9770c14bea06828ddf`.
The legacy store exposed config digest
`sha256:5d3e97d195dbbe7e47e47055e46f8c6f15fb9553be0c7ef19ed0060756fc7116`;
the containerd store exposed OCI index digest
`sha256:0320a60c5b2628cebeb2c897bbf80da949f3b9bb99fa61f5a3475c7276328756`.

Under the corrected governance, this closes the old v3 runner/environment
revision, not the Terra/Luna scientific specification. Attempts `-01` and
`-02` remain retained and excluded. A later sequential attempt is eligible
only after the replacement runner/environment is reviewed, passes an exact
end-to-end shakedown, and is cleanly frozen; observations from different
runner/environment revisions are not pooled by default.
