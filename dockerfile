FROM python:3.11-alpine as backend-builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
 CMD ["python", "app.py"]

# FROM python:3.11-slim as builder
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install --no-cache-dir  --user  -r requirements.txt
# COPY . .

# FROM python:3.11-alpine
# WORKDIR /app
# COPY --from=builder /root/.local /root/.local
# ENV PATH=/root/.local/bin:$PATH
# COPY . .
# CMD ["python", "app.py"]


# #  FROM python:3.11-slim as builder
# #  WORKDIR /app
# #  COPY requirements.txt .
# #  RUN pip install --no-cache-dir -r requirements.txt
# #  COPY . .
# # 
# #  FROM gcr.io/distroless/python3
# #  WORKDIR /app
# #  COPY --from=builder /app /app
# #  CMD ["app.py"]
