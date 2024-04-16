import os
import subprocess

def run_scrapy_finale():
    os.chdir('NGO_Final/NGO_ArticlesLinks/RedisDB_Filters/scaling-python-scrapy-redis/redis-python-scrapy-examples')
    command = ['scrapy', 'crawl', 'ArticlesData']
    current_path = os.getcwd()
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    print(error.decode())
    os.chdir('../../../../')

