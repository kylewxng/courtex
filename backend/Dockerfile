FROM public.ecr.aws/lambda/python:3.13

COPY requirements.txt .
RUN pip install -r requirements.txt

ENV HF_HOME=/var/task/.hf_cache
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

COPY backend/ .

CMD ["api.main.handler"]