# Cuda for gpu support. Does not come with python
FROM ubuntu:20.04

ENV TZ="Europe/Copenhagen"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get -y update && \
    apt-get -y install \
    make \
    build-essential\
    libssl-dev \ 
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \ 
    wget\
    curl \ 
    llvm \ 
    libncursesw5-dev \ 
    xz-utils \ 
    tk-dev \ 
    libxml2-dev \ 
    libxmlsec1-dev \ 
    libffi-dev \ 
    liblzma-dev \
    git \
    && rm -rf /var/lib/apt/lists/*


# Install pyenv & add env variables
RUN git clone --depth=1 https://github.com/pyenv/pyenv.git .pyenv
ENV PYENV_ROOT="${HOME}/.pyenv"
ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${PATH}"

# Can be used with buildargs to easily change the python version.
RUN pyenv install 3.8.10
RUN pyenv global 3.8.10

# By setting poetry virtual env to false, we don't need to run python through the poetry shell.
# Setting POETRY_VERSION as an env variable will install the version we define.
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_HOME=/poetry \
    POETRY_VERSION=1.1.11
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
ENV PATH="${POETRY_HOME}/bin:${PATH}"


WORKDIR /workspace
# Copy in the config files
COPY pyproject.toml poetry.lock ./
# Install only dependencies
RUN poetry install --no-root

# Copy in everything else and install our own package. Will make it faster to build after code changes.
COPY . .
RUN poetry install

ENTRYPOINT ["python", "feature_engieering_example/main.py", "main"]
