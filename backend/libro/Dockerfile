FROM python:3-slim
WORKDIR /programas/api-libro
RUN pip3 install fastapi
RUN pip3 install pydantic
RUN pip3 install mysql-connector-python
COPY . .
CMD ["fastapi", "run", "./libro.py", "--port", "8000"]
