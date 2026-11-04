FROM pytorch/pytorch:2.7.1-cuda12.8-cudnn9-runtime

WORKDIR /mol-translation

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

# needed for 'libXrender.so.1: cannot open shared object file: No such file or directory' bug
RUN apt-get update && apt-get install -y --no-install-recommends libxrender1 libxext6 libexpat1 libgl1 libglib2.0-0

# needed to register defaul kernel in notebooks
RUN /opt/conda/bin/python -m ipykernel install \
        --sys-prefix \
        --name conda \
        --display-name "Python (Conda)"
