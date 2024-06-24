 #!/bin/sh
 # vars :: {"sample_app":"package_name"}
 uvicorn src.sample_app.serve:app --host 0.0.0.0 --port 8000