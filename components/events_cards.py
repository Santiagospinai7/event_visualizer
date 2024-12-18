import streamlit as st
from utils.time_utils import convert_time_to_region

# Función para parsear el evento
def parse_event_id(event_id):
    parts = event_id.split("_")
    return {
        "season": parts[0],
        "tournament": "_".join(parts[1:-2]),
        "event_window": parts[-2],
        "region": parts[-1],
    }

# Función principal para mostrar cartas de eventos
def render_events(events_by_region, show_region_time):
    region_list = ["ASIA", "BR", "EU", "ME", "NAC", "NAW", "OCE"]

    # Mostrar contenedor
    st.markdown("<div class='container'><div class='row'>", unsafe_allow_html=True)

    for region in region_list:
        st.markdown("<div class='col-md-4 mb-4'>", unsafe_allow_html=True)
        st.markdown(f"<h5 class='text-center'>{region}</h5>", unsafe_allow_html=True)

        # Verificar si hay eventos para la región
        if region in events_by_region and events_by_region[region]:
            for window in events_by_region[region]:
                begin_time = window.get('beginTime', None)
                end_time = window.get('endTime', None)

                parsed_event = parse_event_id(window["eventWindowId"])
                round_name = parsed_event["event_window"]

                # Convertir a tiempo de región o mantener UTC
                start_time = convert_time_to_region(begin_time, region) if show_region_time else begin_time
                end_time = convert_time_to_region(end_time, region) if show_region_time else end_time

                # Mostrar tarjeta
                st.markdown(f"""
                    <div class="card bg-dark text-white">
                        <div class="card-body text-center">
                            <h6 class="card-title">{round_name}</h6>
                            <p class="card-text">
                                <strong>Start:</strong> {start_time}<br>
                                <strong>End:</strong> {end_time}
                            </p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            # Mostrar mensaje si no hay eventos
            st.markdown("""
                <div class="card bg-secondary text-white">
                    <div class="card-body text-center">
                        <p>No Events Available</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)