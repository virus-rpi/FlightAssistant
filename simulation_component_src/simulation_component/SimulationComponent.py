# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class SimulationComponent(Component):
    """A SimulationComponent component.


Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- accelerations (list of dicts; required)

- tick_data (list of dicts; required)

- tick_speed (number; required)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'simulation_component'
    _type = 'SimulationComponent'
    @_explicitize_args
    def __init__(self, tick_data=Component.REQUIRED, tick_speed=Component.REQUIRED, accelerations=Component.REQUIRED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'accelerations', 'tick_data', 'tick_speed']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'accelerations', 'tick_data', 'tick_speed']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['accelerations', 'tick_data', 'tick_speed']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(SimulationComponent, self).__init__(**args)
