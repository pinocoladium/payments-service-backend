import environ


env = environ.Env()
environ.Env.read_env(env_file='.environment')
