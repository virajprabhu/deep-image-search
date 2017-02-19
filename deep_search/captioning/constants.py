from django.conf import settings
import os

CAPTIONING_GPUID = 2

CAPTIONING_CONFIG = {
    'input_sz': 224,
    'backend': 'cudnn',
    'layer': 30,
    'model_path': os.path.join(settings.BASE_DIR, 'deep_search', 'captioning', 'neuraltalk2/model_id1-501-1448236541.t7'),
    'seed': 123,
    'image_dir': os.path.join(settings.BASE_DIR, 'media', 'grad_cam', 'captioning')
}

CAPTIONING_LUA_PATH = os.path.join(settings.BASE_DIR, 'deep_search', 'captioning', 'captioning.lua')

if CAPTIONING_GPUID == -1:
    CAPTIONING_CONFIG['backend'] = "nn"
else:
    CAPTIONING_CONFIG['backend'] = "cudnn"
