FROM alpine
RUN apk add -U --no-cache gawk
RUN apk add -U --no-cache wget
ADD . /festive
ENV DATA /festive/festival-of-giants-2017-hand-tags.txt
WORKDIR /data
CMD ["sh", "-c", "awk -f /festive/festival.awk ${DATA}"]
