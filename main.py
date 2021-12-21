import uvicorn
from src import app

scrapieApi = app.App()

if __name__ == "__main__":
    uvicorn.run(scrapieApi, host="0.0.0.0", port=8000, log_level="info")
