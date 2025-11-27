FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive \
    SHELL=/bin/bash

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        openssh-server \
        sudo \
        python3 \
        python3-venv \
        python3-pip \
        pipx \
        git \
        curl \
        rsync \
        ca-certificates \
        postgresql-client \
        iproute2 \
        iputils-ping \
        netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Non-root user to mimic a remote machine login
RUN useradd -ms /bin/bash dev && \
    echo "dev:dev" | chpasswd && \
    usermod -aG sudo dev && \
    echo "dev ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

RUN mkdir -p /var/run/sshd /srv && chown dev:dev /srv

COPY entrypoint.sh /usr/local/bin/remote-host-entrypoint
RUN chmod +x /usr/local/bin/remote-host-entrypoint

EXPOSE 22

CMD ["/usr/local/bin/remote-host-entrypoint"]

