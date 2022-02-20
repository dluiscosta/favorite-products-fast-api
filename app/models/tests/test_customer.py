import pytest
import pydantic
import copy

from app.models.customer import CustomerModel


class TestCustomerModel():

    VALID_PARAMS = {
        "full_name": "Daniel Luis Costa",
        "email": "dluiscosta@gmail.com",
    }

    def __get_valid_params_copy(self):
        return copy.deepcopy(self.VALID_PARAMS)

    def test_valid_params(self):
        CustomerModel(**self.VALID_PARAMS)

    def test_invalid_email(self):
        params = self.__get_valid_params_copy()
        params["email"] = "not_an_email"
        with pytest.raises(pydantic.ValidationError):
            CustomerModel(**params)
