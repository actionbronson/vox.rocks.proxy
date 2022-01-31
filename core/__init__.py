import logging
import yaml
import os
import confuse

logger = logging.getLogger(__name__)

vox_config = confuse.Configuration('VoxCloudProxy', __name__)
core_config_file = os.environ.get("VOX_CONFIG_FILE", os.path.join(os.path.dirname(__file__), "etc", "core.yaml"))
vox_config.set_file(core_config_file)
logger.info(f"Loaded core config file: '{core_config_file}'")
vox_sessions = {}