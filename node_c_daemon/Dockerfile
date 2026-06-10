FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

# Install systems tools along with raw FUSE system libraries
RUN apt-get update && apt-get install -y \
    tmux \
    mc \
    libcom-err2 \
    libcom-dev \
    vim \
    nano \
    netcat-traditional \
    make \
    gcc \
    par2 \
    fuse3 \
    libfuse-dev \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /tmp/kerbtap-spool /tmp/nntpfusemount /root/workspace

WORKDIR /root/workspace

# Set up text editor styling inside the terminal
RUN echo "syntax on\nset tabstop=4\nset expandtab\nset shiftwidth=4\nset autoindent\nset number" > /root/.vimrc

# Install fusepy to communicate directly with kernel VFS hooks
RUN pip install --no-cache-dir flask python-dotenv fusepy dateparser


COPY app.py /root/workspace/app.py
COPY nntpfuse.py /root/workspace/nntpfuse.py
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 8080
EXPOSE 9999/udp

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
