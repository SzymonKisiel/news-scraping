# Dockerfile
FROM python:3.9

RUN mkdir /application
WORKDIR /application

# Upgrade pip
RUN pip install --upgrade pip

# Clean up
RUN apt-get -y update \
    && apt-get clean; rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/*

# Downlad model
# RUN apk update
# RUN apk add git
# RUN git lfs install
# RUN git clone https://huggingface.co/Voicelab/herbert-base-cased-sentiment /tmp/model
# RUN rm -rf /tmp/model/.git
# RUN mkdir ~/.cache/huggingface/transformers
# COPY /tmp/model ~/.cache/huggingface/transformers
# RUN python3 -c "
#     from sentence_transformers import SentenceTransformer
#     model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
#     model.save('models')
# "

# Add sources
ADD requirements.txt /application/
ADD app.py /application/
ADD main.py /application/
ADD models /application/models
ADD services /application/services

RUN pip install --no-cache-dir -r /application/requirements.txt
RUN pip install --no-cache-dir gunicorn

# Download sentiment models
RUN python -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification; AutoTokenizer.from_pretrained('Voicelab/herbert-base-cased-sentiment'); AutoModelForSequenceClassification.from_pretrained('Voicelab/herbert-base-cased-sentiment')"

EXPOSE 5003

#ENTRYPOINT  [ "python", "main.py" ]
ENTRYPOINT [ "gunicorn", "--bind", "0.0.0.0:5003", "--log-level", "debug", "main:app" ]