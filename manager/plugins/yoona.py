from circus.process import Process

process = Process(
    'SAYA-01',
    'saya',
    'todfd',
    shell=True
)
print(process.info())
process.age()