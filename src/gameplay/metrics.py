from pygame.event import Event
import state.ui_state as UI

import pygame
import pygame_gui as gui


class Metrics():
    panel: gui.elements.UIPanel
    markers: list[gui.elements.UIPanel] = []

    def __init__(self):
        metrics_rect = pygame.Rect(0, 0, 200, 104)
        metrics_rect.bottomleft = (20, -20)

        self.panel = gui.elements.UIPanel(
            relative_rect=metrics_rect,
            starting_layer_height=1,
            manager=UI.ui_manager,
            object_id="#metrics",
            anchors={
                "left": "left",
                "right": "left",
                "top": "bottom",
                "bottom": "bottom"
            }
        )

        UI.add(self.panel)

        self.make_marker(19, 55, 176)
        self.make_marker(60, 55, 176)
        
        self.set_marker_percentage(0, 0.5)
        self.set_marker_percentage(1, 0.5)

    def set_mode(self, mode: int):
        metrics: gui.elements.UIPanel = UI.get("#metrics")
        if mode == 0:
            metrics.object_ids[0] = "#metrics"
            self.markers[0].visible = 0
            self.markers[1].visible = 0
        elif mode == 1:
            metrics.object_ids[0] = "#metrics_only_economy"
            self.markers[0].visible = 1
            self.markers[1].visible = 0
        elif mode == 2:
            metrics.object_ids[0] = "#metrics_economy_and_approval"
            self.markers[0].visible = 1
            self.markers[1].visible = 1

        metrics.combined_element_ids = metrics.ui_theme.build_all_combined_ids(
            element_ids=metrics.element_ids, class_ids=metrics.class_ids, object_ids=metrics.object_ids
        )
        metrics.rebuild_from_changed_theme_data()

    # Кординатите са на долния десен ъгъл, спрямо долния десен ъгъл на панела
    def make_marker(self, y_baseline: int, start_x: int, end_x: int):
        metrics_rect = pygame.Rect(0, 0, 3, 27)
        metrics_rect.bottomleft = (20 + start_x, -20 - y_baseline)

        marker = gui.elements.UIPanel(
            relative_rect=metrics_rect,
            starting_layer_height=1,
            manager=UI.ui_manager,
            object_id="#metrics_marker",
            anchors={
                "left": "left",
                "right": "left",
                "top": "bottom",
                "bottom": "bottom"
            },
            visible=0
        )
        UI.add(marker)

        marker.start_x = start_x
        marker.end_x = end_x

        self.markers.append(marker)

    # Индексът е или 0 - икономика, или 1 - одобрение,
    # фактор е между 0 и 1.
    def set_marker_percentage(self, index: int, factor: float):
        marker: gui.elements.UIPanel = self.markers[index]

        x = self.panel.rect.x + marker.start_x + (marker.end_x - marker.start_x) * factor
        y = marker.rect.y

        marker.set_position((x, y))
