from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings
import json


def run():
    settings = get_project_settings()
    tasks = settings.get('TASKS')
    config_path = settings.get('CONFIG_PATH')
    print(tasks)
    for task in tasks:
        print(task)
        file = config_path + '/' + task + '.json'
        with open(file, 'r', encoding='utf-8') as f:
            config = json.loads(f.read())
            print(config)


if __name__ == '__main__':
    run()
