import multiprocessing



bind = "192.168.56.101:8000"
workers = multiprocessing.cpu_count() * 2 + 1
