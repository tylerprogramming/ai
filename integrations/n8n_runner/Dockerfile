# Must be the same version as the n8nio/n8n image (set N8N_VERSION in .env; docker-compose passes it in)
ARG N8N_VERSION=2.44.4
FROM n8nio/runners:${N8N_VERSION}

USER root

# install Python packages using uv pip into the task runner's virtual environment
RUN cd /opt/runners/task-runner-python && \
    uv pip install --python .venv/bin/python yt-dlp numpy pandas pydub

# Custom runner config: based on the default config shipped with n8nio/runners 2.44.4,
# with the package allowlists opened up for these Code nodes (see N8N_RUNNERS_*_ALLOW).
# If you change N8N_VERSION, re-check it against that version's docker/images/runners/n8n-task-runners.json.
COPY n8n-task-runners.json /etc/n8n-task-runners.json

USER runner
