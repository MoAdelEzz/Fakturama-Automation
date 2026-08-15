import logging
from typing import Callable, Generic, TypeVar

from src.entities.base import FakturamaEntityUI
from src.ui.window import FakturamaWindow

T = TypeVar("T")
UI = TypeVar("UI", bound=FakturamaEntityUI)

logger = logging.getLogger(__name__)


class EntityWorkflow(Generic[T, UI]):
    def __init__(
        self,
        window: FakturamaWindow,
        data: T | None,
        ui_builder: Callable[
            [FakturamaWindow, T | None],
            UI,
        ],
    ):
        self.ui = ui_builder(window, data)

    def run(self):
        name = self.ui.entity_name
        target = self.ui.entity_target

        logger.info("Starting %s creation for '%s'...", name, target)
        self.ui.open_footer_tab()

        count = self.ui.search()

        if count > 0:
            logger.info(
                "%s '%s' found (%d match(es)) — skipping execution",
                name.capitalize(),
                target,
                count,
            )
            self.ui.resetWindow()
            return

        logger.info(
            "No %s found for '%s' — creating record",
            name,
            target,
        )

        logger.info("Opening create form for %s '%s'...", name, target)
        self.ui.open_create_form()
        logger.info("Filling form for %s '%s'...", name, target)
        self.ui.fill_form()
        self.ui.save()
        logger.info("%s '%s' created successfully", name.capitalize(), target)