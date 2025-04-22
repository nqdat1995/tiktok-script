ARG NODE_VERSION=20
FROM node:${NODE_VERSION}-bullseye

ARG N8N_VERSION
RUN if [ -z "$N8N_VERSION" ] ; then echo "The N8N_VERSION argument is missing!" ; exit 1; fi

LABEL org.opencontainers.image.title="n8n"
LABEL org.opencontainers.image.description="Workflow Automation Tool"
LABEL org.opencontainers.image.source="https://github.com/n8n-io/n8n"
LABEL org.opencontainers.image.url="https://n8n.io"
LABEL org.opencontainers.image.version=${N8N_VERSION}

ENV N8N_VERSION=${N8N_VERSION}
ENV NODE_ENV=production
ENV N8N_RELEASE_TYPE=stable

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3 \
    python3-pip \
    python3-venv \
    wget \
    ca-certificates \
    openssl \
	bash-completion \
	libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    ccache \
	ffmpeg \
    tini && \
	echo "source /etc/bash_completion" >> /root/.bashrc && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir --upgrade pip setuptools wheel

# Install paddlepaddle and paddleocr
RUN pip3 install --no-cache-dir paddlepaddle==3.0.0rc1 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/

RUN pip3 install --no-cache-dir \
    paddleocr \
    opencv-python-headless

# Install n8n
RUN set -eux; \
    npm install -g --omit=dev n8n@${N8N_VERSION} --ignore-scripts && \
    npm rebuild --prefix=/usr/local/lib/node_modules/n8n sqlite3 && \
    rm -rf /usr/local/lib/node_modules/n8n/node_modules/@n8n/chat && \
    rm -rf /usr/local/lib/node_modules/n8n/node_modules/@n8n/design-system && \
    rm -rf /usr/local/lib/node_modules/n8n/node_modules/n8n-editor-ui/node_modules && \
    find /usr/local/lib/node_modules/n8n -type f -name "*.ts" -o -name "*.js.map" -o -name "*.vue" | xargs rm -f && \
    rm -rf /root/.npm

# Setup the Task Runner Launcher
ARG TARGETPLATFORM
ARG LAUNCHER_VERSION=1.1.1
COPY n8n-task-runners.json /etc/n8n-task-runners.json

# Download and install launcher
RUN \
    if [ "$TARGETPLATFORM" = "linux/amd64" ]; then export ARCH_NAME="amd64"; \
    elif [ "$TARGETPLATFORM" = "linux/arm64" ]; then export ARCH_NAME="arm64"; fi; \
    mkdir -p /launcher-temp && \
    cd /launcher-temp && \
    wget https://github.com/n8n-io/task-runner-launcher/releases/download/${LAUNCHER_VERSION}/task-runner-launcher-${LAUNCHER_VERSION}-linux-${ARCH_NAME}.tar.gz && \
    wget https://github.com/n8n-io/task-runner-launcher/releases/download/${LAUNCHER_VERSION}/task-runner-launcher-${LAUNCHER_VERSION}-linux-${ARCH_NAME}.tar.gz.sha256 && \
    echo "$(cat task-runner-launcher-${LAUNCHER_VERSION}-linux-${ARCH_NAME}.tar.gz.sha256) task-runner-launcher-${LAUNCHER_VERSION}-linux-${ARCH_NAME}.tar.gz" > checksum.sha256 && \
    sha256sum -c checksum.sha256 && \
    tar xvf task-runner-launcher-${LAUNCHER_VERSION}-linux-${ARCH_NAME}.tar.gz --directory=/usr/local/bin && \
    cd - && \
    rm -rf /launcher-temp

# Create and set up entrypoint
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh && \
    mkdir -p /home/node/.n8n && \
    chown -R node:node /home/node/.n8n

# Verify Python and pip are installed correctly
RUN python3 --version && pip3 --version

ENV SHELL /bin/bash
USER node
WORKDIR /home/node
ENTRYPOINT ["tini", "--", "/docker-entrypoint.sh"]