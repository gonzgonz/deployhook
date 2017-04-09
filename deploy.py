import json
import subprocess32
import logging

# Here we define how we run our deploy command
def run_cmd(command):
    basepath = '/home/deploy/ansible/current'
    cmd = 'cd %s && %s' % (basepath, command)
    try:
        output = subprocess32.check_output(cmd, shell=True)
        logging.info(output)
    except subprocess32.CalledProcessError as e:
# Notify to hipchat (I'm using an alraedy made ansible playbook for this, use your own solution if you want)
        notify = 'cd %s && ansible-playbook -i staging tools/notify.yml -e hipchat_msg="\'<p>%s<strong> FAILED</strong></p><pre><code>%s</code></pre>\'"' % (basepath, cmd, e.output)
        subprocess32.check_output(notify, shell=True)
        logging.error(e.output)

# Here we can check if payload is worth our attention
def check(repo_name, repo_branch):
    with open("bitbucket.json") as json_file:
        json_data = json.load(json_file)
        repositories = json_data.get('repositories')
        if repo_name in repositories:
            logging.debug('Repository: %s was found in configuration file. Checking if branch: %s matches.', repo_name, repo_branch)
            if repo_branch in repositories[repo_name]['branches']:
                logging.info('Branch: %s matches.', repo_branch)
                project_name = repo_name
                command = (repositories[repo_name]['branches'][repo_branch]['command'])
                logging.info('Deploying %s ( %s )', project_name, command)
                run_cmd(command)
            else:
                logging.debug('Nothing to do with branch: %s', repo_branch)
        else:
            logging.info('Repo: %s not in config file.', repo_name)

