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
	for item in df_config['cloud_functions']:
		cf_name = item['name']
		cf_arg_list = ' '.join([
		    '--source=' + item['source'],
		    '--entry-point=' + item['entry-point'],
		    '--' + item['trigger-type'] + ' ' + item['trigger-name'],
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