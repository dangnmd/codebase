#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codebase_api.settings")
	from django.core.management import execute_from_command_line
	
	execute_from_command_line(sys.argv)
	import patch_force_index
	patch_force_index.apply_patch()
	from codebase_lib.managers.localization_manager import init_locales
	init_locales()
