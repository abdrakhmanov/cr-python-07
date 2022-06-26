"""
Ваш проект - что-то похожее на шахматы, ваша задача
написать класс/иерархию классов для фигуры в вашей игре.
Важно понимать, реализация никакая не требуется,
необходимо написать только их интерфейсы, для примера вот:
"""


class FigureNames(object):
    PAWN = 'Pawn'
    KING = 'King'
    QUEEN = 'Queen'


class ChessBoard(object):
    FigurePositions = {}

    def can_eat(self, attacking_position, aim_position) -> bool:
        pass

    def get_figure(position) -> Figure:
        pass


class Figure(object):
    name  # type: FigureNames
    position  # type:str

    def __init__(self, name: FigureNames, position: str):
        self.name = FigureNames.PAWN
        self.position = position

    def check_new_position(new_position) -> bool:
        pass

    def go(self, new_position):
        if self.check_new_position(new_position):
            self.position = new_position

    def check_eatable(self, aim_position) -> bool:
        return ChessBoard.can_eat(self.position, aim_position)

    def eat(self, aim_position):
        pass


"""
Написать иерархию классов для работы карты с дорожными знаками.
Также, никакой внутренней реализации, только интерфейс.
"""


class RoadSignTypes():
    pass


class RoadSign():
    coordinate = {
        "lat": 0.0,
        "lon": 0.0
    }
    type = ''  # type: RoadSignTypes


class Map():
    def add_road_sign(self, road_sign: RoadSign):
        pass

    def get_road_signs(self):
        pass

    def get_roas_sign(self, id):
        pass

    def remove_road_sign(self, id)
    pass

    def get_road_signs_by_type(self):
        pass

    def get_road_signs_by_polygone(self):
        pass
