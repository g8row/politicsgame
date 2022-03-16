import state.game_state as GS


def report_error(line: int, message: str):
    print(f"[data/script] Грешка на ред: {line}: {message}.")


def commit_prompt(properties: dict[str, str | int]):
    if len(properties) == 0:
        return

    day = int(properties["day"])
    if day not in GS.script_parsed:
        GS.script_parsed[day] = [properties]
    else:
        GS.script_parsed[day].append(properties)

    # TODO: Провери тук дали има пропъртита и т.н. репортни грешки..


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

    last_prompt_type: str = ""
    last_prompt: dict[str, str | int] = {}

    for l in lines:
        l = l.strip()
        line += 1

        if len(l) == 0:
            continue
        if l[0] == "#":
            continue     # Коментар

        if l[0] == "[":
            commit_prompt(last_prompt)
            last_prompt_type = ""
            last_prompt = {}

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
                    report_error(line, "Липсва запетая между деня и типа. Пр. [day = 1, type = JustOk]")
                tokens = tokens[4:]

            if not day.isdigit():
                report_error(line, f"Липсва правилен ден ({day} не е правилно число). Пр. [day = 3, ...]")
                return False

            day = int(day)

            if len(tokens) < 3 or tokens[0] != "type" or tokens[1] != "=":
                report_error(line, "Липсва тип на promptа. Пр. [..., type = JustOk]")
                return False

            prompt_type = tokens[2]
            if prompt_type[-1] == "]":
                prompt_type = prompt_type[:-1]
            last_prompt_type = prompt_type

            last_prompt["day"] = day
            last_prompt["prompt"] = prompt_type
            continue

        tokens = l.split()
        first = tokens[0].strip()
        if first == "title" or first == "desc_html" or first == "button_text":
            if last_prompt_type == None:
                report_error(line, "Липсва header на promptа преди този ред. Пр. [day = 1, type = JustOk]")
                return False

            if last_prompt_type != "JustOk":
                report_error(line, "Тази опция е валидна само за тип на prompt 'JustOk'")

            if tokens[1].strip() != '=':
                report_error(line, f"Невалиден ред. Ако си забравил, сложи =! Пр. title = \"...\"")

            rest = ' '.join(tokens[2:])
            last_prompt[first] = rest
        else:
            report_error(line, f"Невалиден ред. Ако си забравил, сложи space-ове около =! Пр. title = \"...\"")

    commit_prompt(last_prompt)

    GS.script = GS.script_parsed

    # print(GS.script)

    return True