 #!/bin/sh
 uvicorn mserve:app --host 0.0.0.0 --port 8000 --reload --reload-dir mstack/src