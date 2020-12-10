# START
____
### 1 Clone the repository
```bash
git clone https://github.com/MykolaZ12/backend_hackaton.git
```
____
### 2 Install requirements
```bash
pip install -r requirements.txt
```
____
### 3 In /config/ directory rename local_config.py-example to local_config.py and fill  

____
### 4 Create migrations
```bash
alembic revision --autogenerate
```
____
### 5 Apply migrations
```bash
alembic upgrade head
```
____
### 6 Start app
```bash
uvicorn main:app --reload
```
____