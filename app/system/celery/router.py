from pathlib import Path
from typing import List, Dict, Any

import yaml
from celery.schedules import crontab


class TaskRouter:

    def __init__(self, modules: List[str], task_directory: str = 'tasks') -> None:
        """Generates appropriate routing keys and import for setting up the celery server.

        Args:
            modules (List[str]): _description_
            task_directory (str, optional): _description_. Defaults to 'tasks'.
        """
        self.task_directory = task_directory
        self.modules = modules

        root_path = Path('./')
        tasks_path = Path(self.task_directory)
        self.path_to_modules_task_directory = []
        for module in self.modules:
            module_path = Path(module)
            self.path_to_modules_task_directory.append(root_path / module_path / tasks_path)

    def routes(self) -> Dict[str, Dict[str, str]]:
        """Celery task_routes generator

        Returns:
            Dict[str, Dict[str, str]]: to be used for celery task_routes config.
        """
        return {f"{module}.{self.task_directory}.*": {'queue': module} for module in self.modules}

    def imports(self) -> List[str]:
        """Celery imports generator

        Returns:
            List[str]: to be used for celery imports config.
        """
        all_imports = []
        for module in self.path_to_modules_task_directory:
            for path in list(module.rglob('*.py')):
                all_imports.append(str(path).replace('/', '.')[:-3].replace('.__init__', ''))
        return all_imports

    @staticmethod
    def schedule_parser(file: Path) -> Dict[str, Dict[str, Any]]:
        """Reads a schedule YAML file and parses it to the appropriate input for celery conf.beat_schedule method.

        Args:
            file (Path): Path to the YAML file.

        Returns:
            Dict[str, Dict[str, Any]]: to be used as input for celery conf.beat_schedule method.
        """
        with open(file, 'r') as f:
            schedule_dict = yaml.safe_load(f)
            if isinstance(schedule_dict, dict):
                for spec in schedule_dict.values():
                    schedule_expression = spec.get("schedule", None)
                    if isinstance(schedule_expression, dict):
                        spec["schedule"] = crontab(**spec["schedule"])
                return schedule_dict
        return {}

    def schedules(self) -> Dict[str, Dict[str, Any]]:
        """Combines all schedules defined in all modules.

        Returns:
            Dict[str, Dict[str, Any]]: to be used as input for celery conf.beat_schedule method.
        """
        all_schedules = {}
        for module in self.path_to_modules_task_directory:
            for schedule_file in list(module.rglob('*.yml')) + list(module.rglob('*.yaml')):
                all_schedules = all_schedules | self.schedule_parser(schedule_file)
        return all_schedules
