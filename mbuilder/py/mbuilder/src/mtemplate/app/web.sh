 #!/bin/sh
 uvicorn src.sample_app.serve:app --host 0.0.0.0 --port 8000 --reload --reload-dir ./src --reload-dir /app/mbuilder/py/mbuilder/src