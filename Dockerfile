FROM heartexlabs/label-studio:latest

ENV LABEL_STUDIO_DISABLE_CSRF=true

CMD ["label-studio", "start", "--host", "0.0.0.0", "--port", "8080"]
