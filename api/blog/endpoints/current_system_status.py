import logging
from flask_login import login_required, current_user
from flask import request, current_app
from flask_restplus import Resource
from multiprocessing.pool import ThreadPool
from subprocess import check_call
import os
import json
import psutil

from ..serializers.sys_stat_serializer import sys_stat_get_schema, Current_sys_stat_get_schema, waitCurrentProcess_post_schema
from ...restplus import rest_api




log = logging.getLogger(__name__)

ns = rest_api.namespace('sys/info', description='Operations related to add a new plugin')

@login_required
@ns.route('/')
class SystemStatus(Resource):

	@rest_api.marshal_list_with(sys_stat_get_schema)
	def get(self):
		"""
		Returns currents System Status (Memory in bytes / CPU usage).

		rss : RSS is the Resident Set Size and is used to show how much memory is allocated
			to that process and is in RAM. It does not include memory that is swapped out,
		usedCPU : Return a float representing the current process CPU utilization as a percentage.
		"""

		try:            
			info = {"rss": psutil.virtual_memory().used, "usedCPU":psutil.cpu_percent(interval=0.5)}
			#print(info)
			
		except Exception:
			return None, 404

		return info

@login_required
@ns.route('/<int:pid>')
@rest_api.response(404, 'The currents System Status not accessible.')
class CurrentSystemStatus(Resource):

	@rest_api.marshal_with(Current_sys_stat_get_schema)
	def get(self, pid):
		"""
		Desc. the Current Process info (Memory in bytes/ CPU usage/ ...) of a given programme.
		name : The process name,
		status : The process current status (runnig, ...),
		userName : The name of the user that owns the process,
		rss : RSS is the Resident Set Size and is used to show how much memory is allocated
			to that process and is in RAM. It does not include memory that is swapped out,
		usedCPU : Return a float representing the current process CPU utilization as a percentage,
		numThreads : Return the number of threads used by this process.
		"""
		try:
			py = psutil.Process(pid)
			#  RSS is the Resident Set Size and is used to show how much memory is allocated
			#  to that process and is in RAM. It does not include memory that is swapped out.
			memoryUse = py.memory_info()  # bytes
			# memoryUse e.g.  pmem(rss=2252800, vms=2487709696, pfaults=144955, pageins=26)
			cpuUse = py.cpu_percent(interval=0.5)   # The returned value is explicitly NOT split evenly between all available logical CPUs.
			
			info = {"name":py.name(), "status":py.status(), "userName":py.username(), 
			'rss': int(memoryUse.rss), "usedCPU": cpuUse, "numThreads":py.num_threads()}
		except Exception:
			return None, 404
		
		return info

@login_required
@ns.route('/suspend/<int:pid>/')
@rest_api.response(404, 'The currents Process not accessible.')
@rest_api.response(201, 'Suspend process successfully.')
class SuspendProcess(Resource):
	def get(self, pid):
		"""Suspend process execution with SIGSTOP pre-emptively checking
        whether PID has been reused.
        On Windows this has the effect ot suspending all process threads.
        """
		try:
			py = psutil.Process(pid)
			py.suspend()
			return None, 201
		except Exception:
			return None, 404

@login_required
@ns.route('/resume/<int:pid>/')
@rest_api.response(404, 'The currents Process not accessible.')
@rest_api.response(201, 'Resume process successfully.')
class ResumeProcess(Resource):
	def get(self, pid):
		"""Resume process execution with SIGCONT pre-emptively checking
        whether PID has been reused.
        On Windows this has the effect of resuming all process threads.
        """
		try:
			py = psutil.Process(pid)
			py.resume()
			return None, 201
		except Exception:
			return None, 404

@login_required
@ns.route('/terminate/<int:pid>/')
@rest_api.response(404, 'The currents Process not accessible.')
@rest_api.response(201, 'Process terminate successfully.')
class TerminateProcess(Resource):
	def get(self, pid):
		"""Terminate the process with SIGTERM pre-emptively checking
        whether PID has been reused.
        On Windows this is an alias for kill().
        """
		try:
			py = psutil.Process(pid)
			py.terminate()
			return None, 201
		except Exception:
			return None, 404

@login_required
@ns.route('/kill/<int:pid>/')
@rest_api.response(404, 'The currents Process not accessible.')
@rest_api.response(201, 'Process killed successfully.')
class KillProcess(Resource):
	def get(self, pid):
		"""Kill the current process with SIGKILL pre-emptively checking
        whether PID has been reused.
        """
		try:
			py = psutil.Process(pid)
			py.kill()
			return None, 201
		except Exception:
			return None, 404
	
@login_required
@ns.route('/wait/')
@rest_api.response(404, 'The currents process not accessible.')
@rest_api.response(201, 'Wait process successfully.')
@rest_api.response(203, 'Error ! This process is still alive')
@rest_api.expect(waitCurrentProcess_post_schema, validate=True)
class WaitCurrentProcess(Resource):

	def post(self, pid, time_to_wait):
		"""Wait for process to terminate and, if process is a children
        of os.getpid(), also return its exit code, else None.

        If the process is already terminated immediately return None
        instead of raising NoSuchProcess.

        If *timeout* (in seconds) is specified and process is still
        alive raise TimeoutExpired.

        To wait for multiple Process(es) use psutil.wait_procs().
        """
		try:
			data = request.json
			py = psutil.Process(data["pid"])
			py.wait(timeout=data["timeout"])
		except Exception:
			return None, 203
		
		return None, 201	
		
