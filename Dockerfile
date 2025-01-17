FROM	debian:12-slim

RUN	apt update
RUN	apt install -y ca-certificates
RUN	apt install -y gcc libhdf5-dev libgsl-dev
RUN	apt install -y rsync make

ADD	RAPTOR-NkS /RAPTOR-NkS
ENV	RAPTOR=/RAPTOR-NkS
WORKDIR	/RAPTOR-NkS/SgrA-test
RUN	bash setup.sh