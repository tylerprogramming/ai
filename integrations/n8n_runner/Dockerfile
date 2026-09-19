FROM n8nio/runners:2.0.0

USER root

# install Python packages using uv pip into the task runner's virtual environment
RUN cd /opt/runners/task-runner-python && \
    uv pip install --python .venv/bin/python yt-dlp numpy pandas pydub

# copy custom configuration that allowlists the packages
COPY n8n-task-runners.json /etc/n8n-task-runners.json

USER runner
