# RAPTOR Docker Container

Run the following:

    docker build -t raptor .

to build the `raptor` container.
Use

    docker run -v .:/RAPTOR-NkS/SgrA-test/data -it --rm raptor

to run the container.

For cross-platform build, run

    docker buildx build --platform=linux/amd64,linux/arm64 -t raptor .
