import pytest
from unittest.mock import Mock

from praktikum.burger import Burger


@pytest.fixture
def burger_with_three_ingredients():
    """Фикстура: бургер с тремя ингредиентами"""
    burger = Burger()
    mock_ingredients = [
        Mock(),
        Mock(),
        Mock()
    ]
    
    mock_ingredients[0].get_name.return_value = 'Ингредиент_0'
    mock_ingredients[0].get_price.return_value = 10
    mock_ingredients[0].get_type.return_value = 'FILLING'
    burger.add_ingredient(mock_ingredients[0])
    
    mock_ingredients[1].get_name.return_value = 'Ингредиент_1'
    mock_ingredients[1].get_price.return_value = 20
    mock_ingredients[1].get_type.return_value = 'FILLING'
    burger.add_ingredient(mock_ingredients[1])
    
    mock_ingredients[2].get_name.return_value = 'Ингредиент_2'
    mock_ingredients[2].get_price.return_value = 30
    mock_ingredients[2].get_type.return_value = 'FILLING'
    burger.add_ingredient(mock_ingredients[2])
    
    return burger, mock_ingredients


class TestBurger:

    def test_set_buns(self):
        mock_bun = Mock()
        mock_bun.get_name.return_value = 'Черная булка'
        mock_bun.get_price.return_value = 100

        burger = Burger()
        burger.set_buns(mock_bun)

        assert burger.bun == mock_bun

    def test_add_ingredient(self):
        mock_ingredient = Mock()
        mock_ingredient.get_name.return_value = 'Сыр'
        mock_ingredient.get_price.return_value = 50
        mock_ingredient.get_type.return_value = 'FILLING'

        burger = Burger()
        burger.add_ingredient(mock_ingredient)

        assert burger.ingredients[0] == mock_ingredient

    @pytest.mark.parametrize('index', [0, 1, 2])
    def test_remove_ingredient(self, burger_with_three_ingredients, index):
        burger, mock_ingredients = burger_with_three_ingredients

        burger.remove_ingredient(index)

        expected_ingredients = [mock_ingredients[i] for i in range(3) if i != index]
        assert burger.ingredients == expected_ingredients

    def test_remove_ingredient_invalid_index(self):
        burger = Burger()
        mock_ingredient = Mock()
        mock_ingredient.get_name.return_value = 'Сыр'
        mock_ingredient.get_price.return_value = 50
        mock_ingredient.get_type.return_value = 'FILLING'
        burger.add_ingredient(mock_ingredient)

        with pytest.raises(IndexError):
            burger.remove_ingredient(10)

    @pytest.mark.parametrize('index, new_index', [
        (0, 1),
        (1, 2),
        (2, 0),
        (0, 2),
    ])
    def test_move_ingredient(self, burger_with_three_ingredients, index, new_index):
        burger, mock_ingredients = burger_with_three_ingredients

        burger.move_ingredient(index, new_index)

        expected_ingredients = mock_ingredients.copy()
        element = expected_ingredients.pop(index)
        expected_ingredients.insert(new_index, element)
        assert burger.ingredients == expected_ingredients

    def test_get_price(self):
        mock_bun = Mock()
        mock_bun.get_name.return_value = 'Черная булка'
        mock_bun.get_price.return_value = 100

        mock_ingredient1 = Mock()
        mock_ingredient1.get_name.return_value = 'Котлета'
        mock_ingredient1.get_price.return_value = 150
        mock_ingredient1.get_type.return_value = 'FILLING'

        mock_ingredient2 = Mock()
        mock_ingredient2.get_name.return_value = 'Соус'
        mock_ingredient2.get_price.return_value = 30
        mock_ingredient2.get_type.return_value = 'SAUCE'

        burger = Burger()
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient1)
        burger.add_ingredient(mock_ingredient2)

        price = burger.get_price()

        expected_price = 100 * 2 + 150 + 30
        assert price == expected_price

    def test_get_price_no_ingredients(self):
        mock_bun = Mock()
        mock_bun.get_name.return_value = 'Черная булка'
        mock_bun.get_price.return_value = 100

        burger = Burger()
        burger.set_buns(mock_bun)

        price = burger.get_price()

        expected_price = 100 * 2
        assert price == expected_price

    def test_get_receipt(self):
        mock_bun = Mock()
        mock_bun.get_name.return_value = 'Черная булка'
        mock_bun.get_price.return_value = 100

        mock_ingredient1 = Mock()
        mock_ingredient1.get_name.return_value = 'Котлета'
        mock_ingredient1.get_price.return_value = 150
        mock_ingredient1.get_type.return_value = 'FILLING'

        mock_ingredient2 = Mock()
        mock_ingredient2.get_name.return_value = 'Соус'
        mock_ingredient2.get_price.return_value = 30
        mock_ingredient2.get_type.return_value = 'SAUCE'

        burger = Burger()
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient1)
        burger.add_ingredient(mock_ingredient2)

        receipt = burger.get_receipt()

        expected_receipt = (
            '(==== Черная булка ====)\n'
            '= filling Котлета =\n'
            '= sauce Соус =\n'
            '(==== Черная булка ====)\n'
            '\n'
            'Price: 380'
        )
        assert receipt == expected_receipt

    def test_get_receipt_no_ingredients(self):
        mock_bun = Mock()
        mock_bun.get_name.return_value = 'Черная булка'
        mock_bun.get_price.return_value = 100

        burger = Burger()
        burger.set_buns(mock_bun)

        receipt = burger.get_receipt()

        expected_receipt = (
            '(==== Черная булка ====)\n'
            '(==== Черная булка ====)\n'
            '\n'
            'Price: 200'
        )
        assert receipt == expected_receipt