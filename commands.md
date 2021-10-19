# Convert ProtoBuf File to Python code

```bash
# install requirements
sudo apt-get install autoconf automake libtool curl make g++ unzip
git clone https://github.com/protocolbuffers/protobuf.git
cd protobuf
git submodule update --init --recursive
./autogen.sh

./configure --prefix=/usr

# convert
protoc --proto_path=protos --python_out=protobuf_pnrd_net protos/owner.proto protos/payload.proto protos/record.proto
```
