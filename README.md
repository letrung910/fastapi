fastapi dev main.py
fastapi run

# this is use to run the fastapi application
# CMD ["uvicorn", "main:app", "--worker", "4", "--host", "0.0.0.0"]

uvicorn books:app --reload
uvicorn main:app --workers 4