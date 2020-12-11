import subprocess
import sys
import yaml

def parse_config():

	with open('./config.yaml') as f:
		config = yaml.load(f, Loader=yaml.FullLoader)

	return config

def main(argv=None):

	df_config = parse_config()

	cf_region = df_config['region']
	cf_runtime = df_config['runtime']
	cf_memory = df_config['memory']
	cf_timeout = df_config['timeout']
	cf_env_vars_file = df_config['env_vars_file']

	# deploy each cloud function in config.yaml iteratively
	for fn in df_config['cloud_functions']:
		cf_name = fn['name']

		if fn['trigger-type'] == 'trigger-http':
			cf_trigger = fn['trigger-type']
		else:
			cf_trigger = fn['trigger-type'] + ' ' + fn['trigger-name']

		cf_arg_list = ' '.join([
		    '--source=' + fn['source'],
		    '--entry-point=' + fn['entry-point'],
		    '--' + cf_trigger,
		    '--region=' + cf_region,
		    '--runtime=' + cf_runtime,
		    '--memory=' + cf_memory,
		    '--timeout=' + cf_timeout,
		    '--env-vars-file=' + cf_env_vars_file,
		    '--allow-unauthenticated',
		    ])

		subprocess.run(['sh', 'deploy-cloud-functions.sh', cf_name, cf_arg_list])

if __name__ == '__main__':
    sys.exit(main())