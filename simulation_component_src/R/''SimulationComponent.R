# AUTO GENERATED FILE - DO NOT EDIT

#' @export
''SimulationComponent <- function(id=NULL, tick_data=NULL) {
    
    props <- list(id=id, tick_data=tick_data)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'SimulationComponent',
        namespace = 'simulation_component',
        propNames = c('id', 'tick_data'),
        package = 'simulationComponent'
        )

    structure(component, class = c('dash_component', 'list'))
}
