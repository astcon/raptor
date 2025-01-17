FROM	debian:12-slim

RUN	apt update &&\
	apt install -y gcc-12 libhdf5-dev libgsl-dev
