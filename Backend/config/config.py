import logging, yaml
from model.errors  import MissingConfigError
from model.dotdict import DotDict
from pathlib       import Path

logger = logging.getLogger("Configuration")

def check_elastic():
    _check_paths(['elastic.url', 'elastic.index.main', 'elastic.index.taxonomy'])
    key = _get_nested_attr(config, 'elastic.api_key')
    if not key:
        user     = _get_nested_attr(config, 'elastic.user')
        password = _get_nested_attr(config, 'elastic.password')
        if not password or not user:
            raise Exception(f"either elastic.api_key or (elastic.user and elastic.password) need to be set in the configuration!")

def check_email():
    _check_paths(['email.smtp.user','email.smtp.password','email.smtp.host','email.smtp.port','email.sender','email.feedback'])

def check_ena():
    _check_paths(['ena.webin.user','ena.webin.password','ena.webin.path'])

def check_fastapi():# check fastapi configuration
    _check_paths(['fastapi.bind_address','fastapi.port'])

def check_matomo(): # check matomo configuration
    if config.matomo:
        _check_paths(['matomo.url','matomo.site_id'])

def check_oidc():
    _check_paths(['oidc.provider','oidc.client.id','oidc.client.secret'])

def check_session():
    _check_paths(['session.storage','session.duration.secs'])

def check_storage():
    _check_paths(['storage.dataset'])

def check_webhook():
    _check_paths(['webhook.secret','webhook.frontend.local','webhook.frontend.hook','webhook.frontend.file','webhook.schema.file','webhook.schema.hook','webhook.schema.local'])

def _check_paths(paths: list[str]):
    for path in paths:
        value = _get_nested_attr(config, path)
        if not value:
            raise MissingConfigError(f"{path}")

def _get_nested_attr(obj, path):
    for part in path.split("."):
        obj = getattr(obj, part)
    return obj

def _load_config(config_path: str = "config.yml") -> dict:
    """Load and parse a YAML configuration file."""
    logger.info(f'loading {config_path}…')
    try:
        # Use Path to handle file paths cross-platform
        with open(Path(config_path), "r") as f:
            # safe_load() parses YAML into Python dict/list/primitives
            return yaml.safe_load(f)
    except FileNotFoundError:
        path = Path(config_path).absolute()
        raise RuntimeError(f"Config file not found at: {path}")
    except yaml.YAMLError as e:
        raise RuntimeError(f"Failed to parse YAML: {e}")

config = DotDict(_load_config())

