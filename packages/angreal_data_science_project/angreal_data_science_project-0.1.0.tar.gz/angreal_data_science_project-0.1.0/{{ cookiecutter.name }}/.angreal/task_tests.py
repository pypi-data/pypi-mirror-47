import sys
import os
import angreal



import subprocess


from angreal import win,warn,error

HERE = os.path.dirname(__file__)
DEV_DOCKER_FILE = os.path.join(HERE,'..','docker','DevelopmentImage')
CONTEXT = os.path.join(HERE,'..')



# small work around to import local files
sys.path.append(os.path.abspath(HERE))
from helpers import  BASE_DEV_GPU_IMAGE, BASE_DEV_CPU_IMAGE, CLIENT,  image_build, in_container




@angreal.command()
@angreal.option('--verbose',is_flag=True,help="Verbose outputs get you logs from build and container.")
@angreal.option('--cpu', is_flag=True, help="Force usage of CPU")
@angreal.option('--no_docker',is_flag=True, help="Don't attempt to run inside of a docker container")
def angreal_cmd(verbose, cpu, no_docker):
    """
    run tests in tests/unit
    """
    if cpu:
        warn("Using CPU only")
        gpu_available = lambda : False
    else :
        from helpers import gpu_available



    if no_docker or in_container():
        #Just try to run the tests
        os.chdir(os.path.join(HERE, '..'))
        subprocess.run('pytest  -s -vvv --cov={{cookiecutter.name}} --cov-report=html --cov-report=term tests/unit/ ',
                       shell=True)

        return

    else :
        #Other wise build+run

        if gpu_available():
            try:
                image = image_build(DEV_DOCKER_FILE,CONTEXT,{'BASE_CONTAINER' : BASE_DEV_GPU_IMAGE}, verbose=verbose)

            except Exception as e:
                warn("GPU build/start failed for some reason, falling back to CPU.")
                error(str(e))
                image = image_build(DEV_DOCKER_FILE,CONTEXT,{'BASE_CONTAINER': BASE_DEV_CPU_IMAGE}, verbose=verbose)
                pass

        else:
            image = image_build(DEV_DOCKER_FILE,CONTEXT,{'BASE_CONTAINER': BASE_DEV_CPU_IMAGE},verbose=verbose)






        args = [image.id, 'tests']
        kwargs = dict(
                      detach=True,
                      volumes = {CONTEXT: { 'bind': '/home/elrond/project', 'mode': 'rw' }}
                    )

        if gpu_available():
            kwargs['runtime'] = 'nvidia'


        container = CLIENT.containers.run(*args,**kwargs)





        log = container.logs(stream=True)


        for message in log:
                angreal.echo(message.strip())
