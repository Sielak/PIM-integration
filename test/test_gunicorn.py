import gunicorn

def test_config():
    assert gunicorn.name == "gunicorn config for FastAPI"
    assert gunicorn.accesslog == "/home/ubuntu/logs/pim_integration/access.log"
    assert gunicorn.errorlog == "/home/ubuntu/logs/pim_integration/error.log"
    assert gunicorn.bind == "0.0.0.0:8100"
    assert gunicorn.worker_class == "uvicorn.workers.UvicornWorker"
    assert gunicorn.timeout == 120
