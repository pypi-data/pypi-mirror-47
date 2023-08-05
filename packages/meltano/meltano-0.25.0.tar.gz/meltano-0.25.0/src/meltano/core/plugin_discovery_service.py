import os
import yaml
import requests
from typing import Dict, List, Optional
from itertools import groupby

import meltano.core.bundle as bundle
from .plugin import Plugin, PluginType
from .plugin.factory import plugin_factory


class PluginNotFoundError(Exception):
    pass


class DiscoveryInvalidError(Exception):
    """Occurs when the discovery.yml fails to be parsed."""

    pass


class DiscoveryUnavailableError(Exception):
    """Occurs when the discovery.yml cannot be found or downloaded."""

    pass


MELTANO_DISCOVERY_URL = "https://www.meltano.com/discovery.yml"


class PluginDiscoveryService:
    def __init__(self, project, discovery: Optional[Dict] = None):
        self.project = project
        self._discovery = discovery

    @property
    def discovery(self):
        if self._discovery:
            return self._discovery

        try:
            local_discovery = self.project.root.joinpath("discovery.yml")

            if local_discovery.is_file():
                with local_discovery.open() as local:
                    self._discovery = yaml.load(local) or {}
            else:
                response = requests.get(MELTANO_DISCOVERY_URL)
                response.raise_for_status()
                self._discovery = yaml.load(response.text)

            return self._discovery
        except yaml.YAMLError as e:
            raise DiscoveryInvalidError("discovery.yml is not well formed.") from e
        except requests.exceptions.HTTPError as e:
            raise DiscoveryUnavailableError(
                f"{MELTANO_DISCOVERY_URL} returned status {e.response.status_code}"
            ) from e

    def plugins(self) -> List[Plugin]:
        """Parse the discovery file and returns it as `Plugin` instances."""
        # this will parse the discovery file and create an instance of the
        # corresponding `plugin_class` for all the plugins.
        return (
            plugin_factory(plugin_type, plugin_def)
            for plugin_type, plugin_defs in self.discovery.items()
            for plugin_def in sorted(plugin_defs, key=lambda k: k["name"])
            if PluginType.value_exists(plugin_type)
        )

    def find_plugin(self, plugin_type: PluginType, plugin_name: str):
        try:
            return next(
                plugin
                for plugin in self.plugins()
                if (plugin.type == plugin_type and plugin.name == plugin_name)
            )
        except StopIteration:
            raise PluginNotFoundError()

    def discover(self, plugin_type: PluginType):
        """Return a pretty printed list of available plugins."""
        enabled_plugin_types = (
            (
                PluginType.EXTRACTORS,
                PluginType.LOADERS,
                PluginType.TRANSFORMERS,
                PluginType.MODELS,
                PluginType.TRANSFORMS,
                PluginType.ORCHESTRATORS,
            )
            if plugin_type == PluginType.ALL
            else (plugin_type,)
        )
        return {
            plugin_type: [p.name for p in plugins]
            for plugin_type, plugins in groupby(self.plugins(), lambda p: p.type)
            if plugin_type in enabled_plugin_types
        }

    def list_discovery(self, discovery):
        return "\n".join(
            plugin.name for plugin in self.plugins() if plugin.type == discovery
        )
