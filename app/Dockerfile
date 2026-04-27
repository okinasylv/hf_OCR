FROM python:3.6.15-slim-buster
RUN pip3 install flask requests
RUN apt-get install -y tesseract-ocr
RUN pip3 install flask pytesseract pillow
RUN useradd pythonuser -ms /bin/bash
RUN mkdir -p /home/pythonuser/app/uploads && chmod 777 /home/pythonuser/app/uploads
WORKDIR /home/pythonuser/app
USER pythonuser
COPY app.py app.py
CMD python -u app.py