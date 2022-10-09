FROM pytorch/torchserve:latest-cpu

COPY config.properties config.properties
COPY embedder_cosine_normilize_handler.py embedder_cosine_normilize_handler.py
RUN pip install torch-model-archiver -q
RUN pip install torch torchvision --upgrade
USER root
RUN apt-get update -y
RUN apt-get install curl -y
RUN curl -L -o edgenext_arcface_embelms.pt "https://drive.google.com/uc?export=download&id=1CGz3_QrEFUFSqeJY52tb0j4KiWjxi730"
RUN torch-model-archiver --model-name edgenext_arcface --version 1.0 --serialized-file edgenext_arcface_embelms.pt --handler embedder_cosine_normilize_handler.py
RUN mkdir /tmp/model_store
RUN mv edgenext_arcface.mar /tmp/model_store/
