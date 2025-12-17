<center>

# **My First project**

</center>

1) we are using python = 3.11.14
```python
pip install python3 = 3.11.14
```
2) we crate a vertual inveronment 
```bash
uv init
uv sync
uv run python --version
```
3) take allok to the req.txt file
```bash
cp req.txt req.txt
```
4) install the requirements 
```bash
uv pip install ./requirements.txt
```
5) Setup the environment variables
```bash
cp .env.example .env
```
6) POSTMAN Collection

<center>

### Run the API server 

</center>

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```
