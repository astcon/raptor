# RAPTOR Docker Container

Run the following:

    docker buildx build --platform=linux/amd64,linux/arm64 -t raptor .

to build the `raptor` container.
Use

    docker run -v .:/RAPTOR-NkS/SgrA-test/data -it --rm raptor

to run the container.