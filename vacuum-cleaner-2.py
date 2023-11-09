import random


def create_ambient(num_rooms, num_dirt):
    ambient = ['☐'] * num_rooms

    for _ in range(num_dirt):
        while True:
            random_room = random.randint(0, num_rooms - 1)

            if ambient[random_room] == '☐':
                ambient[random_room] = '⛝'
                break

    return ambient


def print_ambient(ambient, pos, hide_dirt=False):
    print("\nAmbiente:")

    if hide_dirt:
        ambient_to_print = []

        for room, index in zip(ambient, range(len(ambient))):
            if room == '⛝':
                if ambient[pos] == '⛝' and pos == index:
                    ambient_to_print.append('⛝')
                else:
                    ambient_to_print.append('☐')
            else:
                ambient_to_print.append(room)
    else:
        ambient_to_print = ambient

    for i, room in enumerate(ambient_to_print):
        if i == pos:
            print(f' 🤖{room}🧹', end=" ")
        else:
            print(f'  {room}  ', end=" ")

    print()


def clear_room(ambient, pos):
    if ambient[pos] == '⛝':
        ambient[pos] = '☐'
        return True
    else:
        return False


def simulate_sensor_failure():
    return random.randint(1, 10) == 1


def spawn_more_dirt():
    return random.randint(1, 8) == 1


def generate_possible_failure(ambient, vacuum_cleaner_pos):
    if simulate_sensor_failure():
        new_vacuum_cleaner_pos = random.randint(1, len(ambient) - 1)
        print(f"Falha no sensor! Movendo-se para sala {new_vacuum_cleaner_pos}.")
        return {'type': 'sensor', 'pos': new_vacuum_cleaner_pos}
    elif spawn_more_dirt():
        dirt_pos = random.randint(0, len(ambient) - 1)
        print(f"Mais sujeira apareceu na sala {dirt_pos}!")
        return {'type': 'dirt', 'pos': dirt_pos}

    return {'type': 'none'}


def treat_failure(possible_failure, vacuum_cleaner_pos, num_rooms, rooms_to_clear, ambient, move=False):
    if possible_failure.get('type') == 'dirt':
            ambient[possible_failure.get('pos')] = '⛝'
            if move:
                rooms_to_clear[possible_failure.get('pos')] = 1
            else:
                rooms_to_clear.add(possible_failure.get('pos'))
    elif possible_failure.get('type') == 'sensor':
        while vacuum_cleaner_pos != possible_failure.get('pos'):
            if possible_failure.get('pos') > vacuum_cleaner_pos:
                vacuum_cleaner_pos += 1
            else:
                vacuum_cleaner_pos -= 1

            if move:
                print_ambient(ambient, vacuum_cleaner_pos, hide_dirt=True)
            else:
                print_ambient(ambient, vacuum_cleaner_pos)

        if move:
            move = greedy_direction(num_rooms, vacuum_cleaner_pos)

    return vacuum_cleaner_pos, rooms_to_clear, ambient, move


def manual_mode(ambient, vacuum_cleaner_pos):
    num_rooms = len(ambient)

    while '⛝' in ambient:
        possible_failure = generate_possible_failure(ambient, vacuum_cleaner_pos)

        vacuum_cleaner_pos, _, ambient, _ = treat_failure(possible_failure, vacuum_cleaner_pos, num_rooms, set(), ambient)

        print_ambient(ambient, vacuum_cleaner_pos)

        if clear_room(ambient, vacuum_cleaner_pos):
            print("Aspirador limpa a sala.")
        else:
            print("Aspirador se move para outra sala.")

        if '⛝' in ambient:
            move = input("Digite 'd' para mover para a direita, 'e' para mover para a esquerda: ")

            if move == 'd':
                if (vacuum_cleaner_pos + 1) >= num_rooms:
                    print("Não é possível mover para a direita.")
                else:
                    vacuum_cleaner_pos += 1
            elif move == 'e':
                if (vacuum_cleaner_pos - 1) < 0:
                    print("Não é possível mover para a esquerda.")
                else:
                    vacuum_cleaner_pos -= 1

    print_ambient(ambient, vacuum_cleaner_pos)

    print("Todas as salas estão limpas!")


def greedy_direction(num_rooms, vacuum_cleaner_pos):
    if vacuum_cleaner_pos >= num_rooms // 2:
        return 'direita'
    else:
        return 'esquerda'


def base_mode(ambient, vacuum_cleaner_pos):
    num_rooms = len(ambient)

    rooms_to_clear = [1] * len(ambient)

    move = greedy_direction(num_rooms, vacuum_cleaner_pos)

    while rooms_to_clear.count(1) > 0:
        possible_failure = generate_possible_failure(ambient, vacuum_cleaner_pos)

        vacuum_cleaner_pos, rooms_to_clear, ambient, move = treat_failure(possible_failure, vacuum_cleaner_pos, num_rooms, rooms_to_clear, ambient, move)

        print_ambient(ambient, vacuum_cleaner_pos, hide_dirt=True)

        print(f"O aspirador está na sala {vacuum_cleaner_pos} e vai para a {move}.")

        if clear_room(ambient, vacuum_cleaner_pos):
            print("Aspirador limpa a sala.")
        else:
            print("Aspirador se move para outra sala.")

        rooms_to_clear[vacuum_cleaner_pos] = 0

        if rooms_to_clear.count(1) > 0:
            if vacuum_cleaner_pos == num_rooms - 1:
                move = 'esquerda'
            elif vacuum_cleaner_pos == 0:
                move = 'direita'
            if move == 'direita':
                vacuum_cleaner_pos += 1
            else:
                vacuum_cleaner_pos -= 1
        else:
            print_ambient(ambient, vacuum_cleaner_pos)

    print("Todas as salas estão limpas!")


def omniscient_mode(ambient, vacuum_cleaner_pos):
    rooms_to_clear = set(index for index, room in enumerate(ambient) if room == '⛝')

    while rooms_to_clear:
        possible_failure = generate_possible_failure(ambient, vacuum_cleaner_pos)

        vacuum_cleaner_pos, rooms_to_clear, ambient, _ = treat_failure(possible_failure, vacuum_cleaner_pos, len(ambient), rooms_to_clear, ambient)

        print_ambient(ambient, vacuum_cleaner_pos)

        closest_room = min(rooms_to_clear, key=lambda room: abs(room - vacuum_cleaner_pos))

        print(f"O aspirador está na sala {vacuum_cleaner_pos} e a sala mais próxima com sujeira é {closest_room}.")

        if closest_room > vacuum_cleaner_pos:
            print("O aspirador se move para a direita.")
            vacuum_cleaner_pos += 1
        elif closest_room < vacuum_cleaner_pos:
            print("O aspirador se move para a esquerda.")
            vacuum_cleaner_pos -= 1
        else:
            print("O aspirador está na sala mais próxima com sujeira.")

        if clear_room(ambient, vacuum_cleaner_pos):
            print("Aspirador limpa a sala.")
            rooms_to_clear.discard(vacuum_cleaner_pos)
        else:
            print("Aspirador se move para outra sala.")

    print_ambient(ambient, vacuum_cleaner_pos)
    print("Todas as salas estão limpas!")


def main():
    print("+-----------------------------+")
    print("|         VacuumCleaner       |")
    print("|                             |")
    print("+-----------------------------+")
    print("| Escolha o modo de operação: |")
    print("+-----------------------------+")
    print("| 1 - Manual                  |")
    print("| 2 - Base                    |")
    print("| 3 - Onisciente              |")
    print("+-----------------------------+")
    print()

    mode = int(input())
    if mode not in [1, 2, 3]:
        print("Modo inválido. Escolha entre 1, 2 ou 3.")
        return

    num_rooms = int(input("\nDigite o número de salas (até 10): "))
    if num_rooms <= 0 or num_rooms > 10:
        print("Número de salas inválido. Deve ser de 1 a 10.")
        return

    num_dirt = int(input("\nDigite o número de salas com sujeira: "))
    if num_dirt < 0 or num_dirt > num_rooms:
        print("Número de sujeiras inválido. Deve ser de 0 a", num_rooms)
        return

    ambient = create_ambient(num_rooms, num_dirt)
    vacuum_cleaner_pos = random.randint(0, num_rooms - 1)

    if mode == 1:
        manual_mode(ambient, vacuum_cleaner_pos)
    elif mode == 2:
        base_mode(ambient, vacuum_cleaner_pos)
    elif mode == 3:
        omniscient_mode(ambient, vacuum_cleaner_pos)


if __name__ == "__main__":
    main()
