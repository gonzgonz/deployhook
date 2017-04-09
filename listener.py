from flask import Flask, request
import subprocess32
import deploy
import threading
import logging

# Configure logging
logging.basicConfig(filename='/home/deploy/deployhook/shared/logs/deployhook_app.log',level=logging.DEBUG)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def tracking():
    if request.method == 'POST':
        data = request.get_json()
        repo_name = data['repository']['name']
        repo_branch = data['push']['changes'][0]['new']['name']
        logging.info('Webhook received! Name: %s Branch: %s', repo_name, repo_branch)
        deploy_thread = threading.Thread(target=deploy.check, args=[repo_name, repo_branch])
        logging.debug('Starting thread %s', deploy_thread.getName())
        deploy_thread.start()
        return 'OK'

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        #debug=True,
        port=8888,
    )

