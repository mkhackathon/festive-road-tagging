FROM tensorflow/tensorflow:latest-devel-py3
LABEL maintainer="yijun.yu@open.ac.uk"
RUN cd /tensorflow && bazel build --config opt tensorflow/examples/image_retraining:retrain
RUN cd /tensorflow && bazel build --config opt tensorflow/examples/image_retraining:label_image
