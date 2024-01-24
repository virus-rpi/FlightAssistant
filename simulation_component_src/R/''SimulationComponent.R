# AUTO GENERATED FILE - DO NOT EDIT

#' @export
''SimulationComponent <- function(id=NULL, accelerations=NULL, tick_data=NULL, tick_speed=NULL) {
    
    props <- list(id=id, accelerations=accelerations, tick_data=tick_data, tick_speed=tick_speed)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'SimulationComponent',
        namespace = 'simulation_component',
        propNames = c('id', 'accelerations', 'tick_data', 'tick_speed'),
        package = 'simulationComponent'
        )

    structure(component, class = c('dash_component', 'list'))
}
