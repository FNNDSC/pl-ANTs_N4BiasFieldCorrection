FROM fnndsc/antspy:0.2.7 as builder

WORKDIR /usr/local/src
COPY . .
RUN pip --no-cache-dir install .

FROM debian:buster-slim
COPY --from=builder /opt /opt
ENV PATH=/opt/conda/bin:$PATH
CMD ["bfc", "--help"]
