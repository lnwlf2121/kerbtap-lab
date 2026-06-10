# Compile down to a minimal, standalone WebAssembly binary without heavy runtimes
clang --target=wasm32 -O3 -nostdlib \
  -Wl,--no-entry \
  -Wl,--export=entropy \
  -Wl,--export=get_seed \
  -o kerbtab_engine.wasm kerbtab_engine.c

# Convert the resulting binary file into a clean Hex representation for your HTML array
xxd -i kerbtab_engine.wasm
