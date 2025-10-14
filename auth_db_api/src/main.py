import uvicorn
from src.core import tables_check
from src.api.endpoints import app


def main():
    tables_check()
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
