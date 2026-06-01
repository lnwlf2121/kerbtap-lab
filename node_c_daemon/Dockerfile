FROM python:3.10-slim

# Force unbuffered terminal logging
ENV PYTHONUNBUFFERED=1

# Install system utilities, builders, and par2 matrix engine
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
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /tmp/kerbtap-spool /tmp/nntpfusemount /root/workspace

WORKDIR /root/workspace

# Set up text editor styling inside the terminal
RUN echo "syntax on\nset tabstop=4\nset expandtab\nset shiftwidth=4\nset autoindent\nset number" > /root/.vimrc

# Install lightweight web/TUI dependencies
RUN pip install --no-cache-dir flask python-dotenv dateparser

# Copy the exact scripts into the application workspace
COPY app.py /root/workspace/app.py
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 8080
EXPOSE 9999/udp

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
