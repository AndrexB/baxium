Baxium integration/staging tree

What is Baxium?
---------------------

Baxium connects to its peer-to-peer network to download and fully
validate blocks and transactions. It also includes a wallet and graphical user
interface, which can be optionally built.

Baxium replaces Bitcoin's double SHA256 hashing with SHA3-512 for proof-of-work.

Further information about Baxium is available in the [doc folder](/doc).

Build
-----

Building Baxium requires the Boost headers (version 1.73 or newer). On
Debian/Ubuntu systems these can be installed with `apt install libboost-all-dev`.
After installing dependencies, the project can be configured and built with

```sh
cmake -B build
cmake --build build
ctest --test-dir build
```
