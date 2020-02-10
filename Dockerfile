FROM ubuntu

ENV CORENLP_URL=http://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip \
    CORENLP_HOME=/corenlp \
    QUASIMODO_DATA=/quasimodo_data\
    REDIS_URL=redis://redis:6379/0

RUN apt -yqq update && \
    apt -yqq upgrade && \
    apt -yqq install python3 \
        git \
        openjdk-8-jdk \
        python3-setuptools \
        python3-dev \
        build-essential \
        python3-pip \
        unzip \
        wget \
        locales \
    && rm -rf /var/lib/apt/lists/*  

# Set the locale
RUN locale-gen en_US.UTF-8
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8    

# Install CORENLP
RUN wget $CORENLP_URL -O corenlp.zip && \
    unzip corenlp.zip && \
    rm corenlp.zip && \
    mv stanford* $CORENLP_HOME

# Create data directories
RUN mkdir $QUASIMODO_DATA && \
    mkdir $QUASIMODO_DATA/properties && \
    mkdir $QUASIMODO_DATA/question2statement

# Invalidate Cache from here
ADD https://time.is/ /tmp/bustcache
# Get code
RUN git clone https://github.com/Aunsiels/CSK.git

# Install python libraries
RUN cd CSK && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt && \
    python3 -m spacy download en_core_web_sm && \
    python3 -m spacy download en_core_web_lg && \
    python3 -m nltk.downloader all
  
# Send config file
COPY quasimodo/parameters_docker.tsv CSK/quasimodo/parameters.tsv

# Send data
COPY quasimodo/data/properties/ $QUASIMODO_DATA/properties/

# Flickr API
COPY keys.py /usr/local/lib/python3.6/dist-packages/flickr_api/keys.py

CMD cd CSK && rq worker -u $REDIS_URL quasimodo-tasks
