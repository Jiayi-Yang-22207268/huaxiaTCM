import multiprocessing

# Log configuration
bind = "127.0.0.1:5000"  # Binding port
workers = multiprocessing.cpu_count() * 2 + 1  # Number of workers
accesslog = "./logs/gunicorn_access.log"  # Access log path
errorlog = "./logs/gunicorn_error.log"  # Error log path
loglevel = "info"  # Log level
capture_output = True  # Capture the print/logging output of Flask
timeout = 30  # Timeout Period (seconds)

limit_request_line = 4094  # Maximum request header size
