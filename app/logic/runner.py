import docker


class Runner:
    def __init__(self):
        self.client = docker.from_env()

    def prepare_container(self, task):
        try:
            c = self.client.containers.run('python:3', '/bin/bash', tty=True, detach=True, auto_remove=True)

            download_solution_result = c.exec_run('curl -f -s {} -o solution.py'.format(task['solution']))
            if download_solution_result.exit_code != 0:
                raise ValueError("Can't download soluton")

            download_checker_result = c.exec_run('curl -f -s {} -o checker.py'.format(task['checker']))
            if download_checker_result.exit_code != 0:
                raise ValueError("Can't download checker")

            return c
        except:
            c.stop()

    def run_task(self, task):
        try:
            c = self.prepare_container(task)

            run_result = c.exec_run('python3 checker.py solution.py') # TODO: запустить чекер на решении

            c.stop()
            return run_result.exit_code == 0, run_result.output

        except Exception as e:
            return False, 'Error while processing: {}'.format(e)
