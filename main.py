import flet as ft
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate


def main(page):
    number_players = ft.TextField(label="Количество игроков за столом")
    hand_cards = ft.TextField(label="Карты в руке")
    table_cards = ft.TextField(label="Карты на столе")
    greetings = ft.Column()

    def btn_click(e):
        NB_SIMULATION = 10000

        hole_card = []
        hole_card.append(hand_cards.value[0] + hand_cards.value[1])
        hole_card.append(hand_cards.value[3] + hand_cards.value[4])

        community_card = []
        if len(table_cards.value) >= 8:
            community_card.append(table_cards.value[0] + table_cards.value[1])
            community_card.append(table_cards.value[3] + table_cards.value[4])
            community_card.append(table_cards.value[6] + table_cards.value[7])

        if len(table_cards.value) >= 11:
            community_card.append(table_cards.value[9] + table_cards.value[10])

        if len(table_cards.value) >= 14:
            community_card.append(table_cards.value[12] + table_cards.value[13])

        hole_card_ = gen_cards(hole_card)
        community_card_ = gen_cards(community_card)

        win_rate = estimate_hole_card_win_rate(
            nb_simulation=NB_SIMULATION,
            nb_player=int(number_players.value),
            hole_card=hole_card_,
            community_card=community_card_
        )

        wall = 1 / int(number_players.value)

        if win_rate < wall:
            rate = "FOLD"
        elif win_rate > 0.85:
            rate = "ALL IN"
        elif win_rate < (2 * wall):
            rate = "CALL"
        elif win_rate < (2.5 * wall):
            rate = "2x"
        elif win_rate < (3 * wall):
            rate = "2.5x"
        else:
            rate = "3x"

        greetings.controls.append(
            ft.Text(f"Вероятность на победу: {round(win_rate * 100, 2)}% Рекомендованная ставка: {rate}"))

        page.update()
        table_cards.focus()

    page.add(
        number_players,
        hand_cards,
        table_cards,
        ft.ElevatedButton("Рассчитать вероятность", on_click=btn_click),
        greetings,
    )


ft.app(target=main, view=ft.WEB_BROWSER)
