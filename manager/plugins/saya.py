from circus import get_arbiter
from circus.sockets import CircusSocket

arbiter = get_arbiter(
    watchers=[
        {
            "name": "SAYA-01",
            "cmd": "chaussette --fd $(circus.sockets.saya)",
            "numprocesses": 5,
            "use_sockets": True,
            "working_dir": "/home/karim/Workspace/github.com/vcar/vcar/manager/plugins",
            "virtualenv": "/home/karim/Workspace/github.com/vcar/.env",
            "copy_env": True,
        }
    ],
    sockets={
        CircusSocket(name='saya', host='127.0.0.1', port='8888'),
        # CircusSocket(name='saya_nginx', path='/tmp/saya.sock', family='AF_UNIX'),
    },
    background=True,
    statsd=True
)
try:
    arbiter.start()
finally:
    arbiter.stop()
