import pytest
import pydantic
import copy
import uuid

from app.schemas import CustomerSchema


class TestCustomerSchema():

    VALID_PARAMS = {
        "id": uuid.uuid4(),
        "full_name": "Daniel Luis Costa",
        "email": "dluiscosta@gmail.com",
    }

    def __get_valid_params_copy(self):
        return copy.deepcopy(self.VALID_PARAMS)

    def test_valid_params(self):
        CustomerSchema(**self.VALID_PARAMS)

    def test_invalid_email(self):
        params = self.__get_valid_params_copy()
        params["email"] = "not_an_email"
        with pytest.raises(pydantic.ValidationError):
            CustomerSchema(**params)

    def test_empty_name(self):
        params = self.__get_valid_params_copy()
        params["full_name"] = ""
        with pytest.raises(pydantic.ValidationError):
            CustomerSchema(**params)
