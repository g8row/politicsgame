import state.ui_state as UI
from prompts.prompt_ending import PromptEnding


def show_good_ending():
    UI.prompt(PromptEnding(title="Добрият край", type="good", desc_html="Добри сте, издържахте мандата!"))


def show_bad_ending():
    UI.prompt(PromptEnding(title="Убит сте в атентат", type="bad", desc_html="Изглежда станахте враг с грешните хора."))


def show_protest_ending():
    UI.prompt(PromptEnding(title="Край", type="protest", desc_html="Протести избухват в триъгълника на властта и вашата кариера беше дотук."))