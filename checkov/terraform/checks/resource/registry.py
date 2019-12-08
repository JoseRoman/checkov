import logging


class Registry:
    checks = {}

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def register(self, check):
        for resource in check.supported_resources:
            if resource not in self.checks.keys():
                self.checks[resource] = []
            self.checks[resource].append(check)

    def get_checks(self, resource):
        if resource in self.checks.keys():
            return self.checks[resource]
        return []

    def scan(self, block, scanned_file):
        resource = list(block.keys())[0]
        resource_conf = block[resource]
        results = {}
        for check in self.get_checks(resource):
            resource_name = list(resource_conf.keys())[0]
            resource_conf_def = resource_conf[resource_name]
            self.logger.debug("Running check: {} on file {}".format(check.name, scanned_file))
            result = check.run(scanned_file=scanned_file, resource_configuration=resource_conf_def,
                               resource_name=resource_name, resource_type=resource)
            results[check] = result
        return results


resource_registry = Registry()