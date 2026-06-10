FROM rust:1.75-alpine

# Install system dependencies required for compilation and FUSE hooks
RUN apk add --no-cache musl-dev gcc fuse fuse-dev git file

# Define a singular, flat workspace path
WORKDIR /usr/src/prizmatic-engine

# Initialize a clean, explicit cargo manifest template inside the active directory
COPY Cargo.toml .
# Inject your true local operational source code
RUN mkdir src && echo "fn main() {}" > src/main.rs


# Pre-compile baseline dependencies to lock down layer caching
RUN cargo build --release
RUN rm -f target/release/deps/prizmatic_protocol_engine*

# Inject your true local operational source code
COPY src ./src

# Execute the definitive release compilation
RUN cargo build --release

# Expose the user-space UDP sieve port boundary
EXPOSE 9999/udp

# Execute the binary from an absolute, un-nested destination target
CMD ["/usr/src/prizmatic-engine/target/release/prizmatic-protocol-engine"]
