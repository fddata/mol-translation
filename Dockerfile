FROM tensorflow/tensorflow:2.14.0-gpu

WORKDIR /mol-translation

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

# needed for 'libXrender.so.1: cannot open shared object file: No such file or directory' bug
RUN apt-get update && apt-get install -y --no-install-recommends libxrender1 libxext6 libexpat1

EXPOSE 8888

ENTRYPOINT ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--no-browser"]
