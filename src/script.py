import state.game_state as GS

# @Volatile: Всички възможни prompt-ове от script-а трябва да са import-нати тук и в script.py
from prompts.prompt_ask_for_identity import PromptAskForIdentity
from prompts.prompt_just_ok import PromptJustOk


def report_error(line: int, message: str):
    print(f"[data/script] Грешка на ред: {line}: {message}.")


def commit_prompt(day: int, type: str, parameters: list[str], line: int) -> bool:
    if len(type) == 0:
        return True     # Не е грешка ако няма prompt

    constructor = f"{type}({','.join(parameters)})"

    # Пробвай да създадеш такъв prompt с тези параметри,
    # така хващаме грешката още при четене вместо да
    # чакаме до съответния ден да се появи, само да разберем,
    # че нещо не е наред.
    try:
        eval(constructor)
    except Exception as exception:
        report_error(line, f"нещо в параметрите се оплаква: {exception}")
        return False

    if day not in GS.script_parsed:
        GS.script_parsed[day] = [constructor]
    else:
        GS.script_parsed[day].append(constructor)

    return True


def parse() -> bool:
    with open("data/script", encoding="utf-8") as f:
        content = f.read()

    GS.script_parsed = {}

    lines = content.splitlines(keepends=False)

    first_line = lines[0].strip()
    lines = lines[1:]

    if first_line[0:2] != "@v":
        report_error(1, "Tрябва да е с версията на файловия формат. Примерно: @v1")
        return False

    version = int(first_line[2:])
    if version != 1:
        report_error(1, f"Твърде нова версия: @v{version}, не знаем какво да я правим.. :(. Може би пускаш стара версия на играта?")
        return False

    line = 1

    last_prompt_day: int = 0
    last_prompt_type: str = ""
    last_prompt_parameters: list[str] = []
    last_prompt_line: int = 0

    for l in lines:
        l = l.strip()
        line += 1

        if len(l) == 0:
            continue
        if l[0] == "#":
            continue     # Коментар

        if l[0] == "[":
            if not commit_prompt(last_prompt_day, last_prompt_type, last_prompt_parameters, last_prompt_line):
                return False

            last_prompt_day = 0
            last_prompt_type = ""
            last_prompt_parameters = []
            last_prompt_line = line

            if l[-1] != "]":
                report_error(line, "Липсва затваряща скоба ']'")
                return False
            tokens = [t.strip() for t in l.split()]

            day_ident = tokens[0]
            if day_ident != "[":
                day_ident = day_ident[1:]
            else:
                day_ident = tokens[1]
                tokens = tokens[1:]

            if len(tokens) < 3 or day_ident != "day" or tokens[1] != "=":
                report_error(line, "Липсва правилен ден. Пр. [day = 3, ...]")
                return False

            day = tokens[2]
            if day[-1] == ",":
                day = day[:-1]
                tokens = tokens[3:]
            else:
                if tokens[3] != ",":
                    report_error(line, "Липсва запетая между деня и типа. Пр. [day = 1, type = PromptJustOk]")
                tokens = tokens[4:]

            if not day.isdigit():
                report_error(line, f"Липсва правилен ден ({day} не е правилно число). Пр. [day = 3, ...]")
                return False

            day = int(day)

            if len(tokens) < 3 or tokens[0] != "type" or tokens[1] != "=":
                report_error(line, "Липсва тип на promptа. Пр. [..., type = PromptJustOk]")
                return False

            last_prompt_day = day

            prompt_type = tokens[2]
            if prompt_type[-1] == "]":
                prompt_type = prompt_type[:-1]
            last_prompt_type = prompt_type

            last_prompt_type = prompt_type
            continue

        if last_prompt_type != "":
            l_stripped = l.strip()
            if l_stripped[-1] == ",":
                l_stripped = l_stripped[:-1]
            last_prompt_parameters.append(l_stripped)

    if not commit_prompt(last_prompt_day, last_prompt_type, last_prompt_parameters, last_prompt_line):
        return False

    GS.script = GS.script_parsed
    # print(GS.script)

    return True
