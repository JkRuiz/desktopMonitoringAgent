from flask import Flask, request, flash
import json


app = Flask(__name__)


@app.route('/createMetric', methods=['POST'])
def register():
    preJson = json.dumps(request.json)
    reqJson = json.loads(preJson)
    fileName = 'metrics.txt'
    print(reqJson)
    with open((fileName), "a") as metrics:
        ip = str(reqJson['ip'])
        ram = str(reqJson['ram'])
        time = str(reqJson['timestamp'])
        swap = str(reqJson['swap'])
        disk = str(reqJson['disk'])
        unacloud_disk = str(reqJson['unacloud_disk'])
        cpu = str(reqJson['cpu'])
        cpu_details = str(reqJson['cpu_details'])
        net_io_counters = str(reqJson['net_io_counters'])
        running_vms = str(reqJson['running_vms'])
        virtualbox_status = str(reqJson['virtualbox_status'])
        vbox_process_count = str(reqJson['vbox_process_count'])
        unacloud_status = str(reqJson['unacloud_status'])
        rtt = str(reqJson['rtt'])
        energy = str(reqJson['energy'])
        user_logged = reqJson['user_logged']
        metrics.write('Cliente - ' + ip + '\n')
        metrics.write('Fecha - ' + time + '\n')
        metrics.write('ram - ' + ram + '\n')
        metrics.write('swap - ' + swap + '\n')
        metrics.write('disk - ' + disk + '\n')
        metrics.write('unacloud_disk - ' + unacloud_disk + '\n')
        metrics.write('cpu - ' + cpu + '\n')
        metrics.write('cpu_details - ' + cpu_details + '\n')
        metrics.write('net_io_counters - ' + net_io_counters + '\n')
        metrics.write('running_vms - ' + running_vms + '\n')
        metrics.write('virtualbox_status - ' + virtualbox_status + '\n')
        metrics.write('vbox_process_count - ' + vbox_process_count + '\n')
        metrics.write('unacloud_status - ' + unacloud_status + '\n')
        metrics.write('rtt - ' + rtt + '\n')
        metrics.write('energy - ' + energy + '\n')
        metrics.write('user_logged - ' + str(user_logged) + '\n')
        metrics.write('--------------------------------------------------' + '\n')
    return('', 204)


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(host='157.253.205.13')
