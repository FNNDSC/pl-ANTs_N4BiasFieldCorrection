FROM fnndsc/antspy:0.2.7

WORKDIR /usr/local/src
COPY . .
RUN pip --no-cache-dir install .

CMD ["bfc", "--help"]
