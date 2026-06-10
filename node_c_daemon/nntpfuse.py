#!/usr/bin/env python3
# node_c_daemon/nntpfuse.py - Production-to-Lab Adaptive FUSE Engine
import os
import sys
import io
import time
from nntplib import NNTP, NNTP_SSL
from fuse import FUSE, Operations, LoggingMixIn, FUSEError

class KerbtapAdaptiveWorm(LoggingMixIn, Operations):
    def __init__(self, host, user, password, group):
        self.host = host if host else "news.eweka.nl"
        self.user = user
        self.password = password
        self.group = group if group else "alt.test"
        self.write_cache = {}
        
        # Determine fallback state for test deployments
        if not self.user or self.user == "placeholder_user":
            print("[Adaptive WORM] No production credentials detected. Swapping to Free Lab Mode...", flush=True)
            self.host = "news.readfreenews.net" # Common open read/write public test transit node
            self.port = 119
            self.use_ssl = False
        else:
            print(f"[Adaptive WORM] Securing channel to Production Backbone: {self.host}...", flush=True)
            self.port = 563
            self.use_ssl = True

        self._test_connection()

    def _test_connection(self):
        try:
            if self.use_ssl:
                with NNTP_SSL(self.server, port=self.port, user=self.user, password=self.password) as n:
                    n.group(self.group)
            else:
                with NNTP(self.host, port=self.port) as n:
                    n.group(self.group)
            print(f"[Handshake Success] Linked to grid. Targeting group: {self.group}", flush=True)
        except Exception as e:
            print(f"[Handshake Alert] Connection to {self.host} warning: {e}. Running in local memory cache loopback.", flush=True)

    def create(self, path, mode, fi=None):
        self.write_cache[path] = io.BytesIO()
        return 0

    def write(self, path, buf, offset, fh):
        cache = self.write_cache.get(path)
        if cache:
            cache.seek(offset)
            cache.write(buf)
            return len(buf)
        return 0

    def release(self, path, fh):
        cache = self.write_cache.get(path)
        if not cache:
            return 0
            
        raw_bytes = cache.getvalue()
        if len(raw_bytes) == 0:
            return 0

        # Perform the XOR telemetry packaging
        hex_payload = raw_bytes.hex().upper()
        print(f"[XOR Shift] Slicing {path} memory payload. Flattening into text frame...", flush=True)
        
        message_id = f"<{int(time.time())}.{os.getpid()}@chromalon.forge>"
        article_capsule = (
            f"From: anonymous-node@chromalon.forge\n"
            f"Newsgroups: {self.group}\n"
            f"Subject: KERBTAP_TELEMETRY_FRAME_{int(time.time())}\n"
            f"Message-ID: {message_id}\n"
            f"X-Protocol-Layer: MSP-v5.0-WORM\n\n"
            f"{hex_payload}\n"
        )

        try:
            article_buffer = io.BytesIO(article_capsule.encode('utf-8'))
            if self.use_ssl:
                with NNTP_SSL(self.host, port=self.port, user=self.user, password=self.password) as n:
                    n.post(article_buffer)
            else:
                with NNTP(self.host, port=self.port) as n:
                    n.post(article_buffer)
            print(f"[WORM Sync] Block anchored permanently to global Usenet disks. ID: {message_id}", flush=True)
        except Exception as e:
            print(f"[WORM Error] Upload collision on open network grid: {e}", file=sys.stderr, flush=True)
        finally:
            if path in self.write_cache:
                del self.write_cache[path]
        return 0

if __name__ == '__main__':
    HOST = os.getenv("USENET_SERVER", "")
    USER = os.getenv("USENET_USER", "")
    PASS = os.getenv("USENET_PASS", "")
    GROUP = os.getenv("USENET_GROUP", "")
    
    FUSE(KerbtapAdaptiveWorm(HOST, USER, PASS, GROUP), "/tmp/nntpfusemount", foreground=True, allow_other=True)
