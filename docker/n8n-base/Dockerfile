ARG NODE_VERSION=20

# 1. Use a builder step to download various dependencies
FROM node:${NODE_VERSION}-bullseye AS builder

# Install fonts (Microsoft Core Fonts)
RUN \
    apt-get update && \
    apt-get install -y --no-install-recommends wget cabextract xfonts-utils fontconfig && \
    mkdir -p /usr/share/fonts/truetype/msttcorefonts && \
    wget -q https://debian.sur5r.net/i3/pool/main/m/msttcorefonts/msttcorefonts-installer_3.7_all.deb && \
    dpkg -i msttcorefonts-installer_3.7_all.deb || true && \
    apt-get install -y -f && \
    fc-cache -f && \
    apt-get remove -y wget cabextract xfonts-utils && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install git and other OS dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends git openssh-client graphicsmagick tini tzdata ca-certificates jq && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Update npm and install full-icu
COPY .npmrc /usr/local/etc/npmrc
RUN npm install -g corepack@0.31 full-icu@1.5.0

# Activate corepack, and install pnpm
WORKDIR /tmp
COPY package.json ./
RUN corepack enable && corepack prepare --activate

# Cleanup
RUN rm -rf /tmp/* /root/.npm /root/.cache/node /opt/yarn*

# 2. Start with a new clean image and copy over the added files into a single layer
FROM node:${NODE_VERSION}-bullseye
COPY --from=builder / /

# Delete this folder to make the base image backward compatible to be able to build older version images
RUN rm -rf /tmp/v8-compile-cache*

WORKDIR /home/node
ENV NODE_ICU_DATA=/usr/local/lib/node_modules/full-icu
EXPOSE 5678/tcp