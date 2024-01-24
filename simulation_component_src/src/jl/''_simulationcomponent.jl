# AUTO GENERATED FILE - DO NOT EDIT

export ''_simulationcomponent

"""
    ''_simulationcomponent(;kwargs...)

A SimulationComponent component.

Keyword arguments:
- `id` (String; optional): Unique ID to identify this component in Dash callbacks.
- `accelerations` (Array of Dicts; required)
- `tick_data` (Array of Dicts; required)
- `tick_speed` (Real; required)
"""
function ''_simulationcomponent(; kwargs...)
        available_props = Symbol[:id, :accelerations, :tick_data, :tick_speed]
        wild_props = Symbol[]
        return Component("''_simulationcomponent", "SimulationComponent", "simulation_component", available_props, wild_props; kwargs...)
end

