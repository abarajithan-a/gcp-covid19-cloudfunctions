import subprocess
import sys
import yaml

def parse_yaml(yaml_path):

	with open(yaml_path) as f:
		yaml_dict = yaml.load(f, Loader=yaml.FullLoader)

	return yaml_dict

def main(argv=None):

    df_config = parse_yaml('./config.yaml')

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
            '--allow-unauthenticated',
            ])

        cf_env_vars_list = []

        # For global environment variables for all cloud functions
        # set in env.prod.yaml file

        global_env_var_dict = parse_yaml(cf_env_vars_file)
        if bool(global_env_var_dict):
        	for (env_name, env_value) in global_env_var_dict.items():
        		cf_env_vars_list.append('{}={}'.format(env_name, env_value))

        # For cloud function specific environment variables
        # set in config.yaml

        env_var_dict = fn['environment_variables']
        if bool(env_var_dict):
        	for (env_name, env_value) in env_var_dict.items():
        		cf_env_vars_list.append('{}={}'.format(env_name, env_value))

        if cf_env_vars_list:
        	cf_arg_list += ' --set-env-vars=' + ','.join(cf_env_vars_list)

        subprocess.run(['sh', 'deploy-cloud-functions.sh', cf_name, cf_arg_list])

if __name__ == '__main__':
    sys.exit(main())