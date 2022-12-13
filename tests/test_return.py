from src.basic_return.BasicReturn import BasicReturn
import pytest
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()


class Test:
    
    def test_basic_definition(self):
        ret = BasicReturn()
        ret.status = 10
        ret.message = "ok"
        ret.payload = {"success": True}
        assert ret.status == 10
        assert ret.message == "ok"
        assert ret.payload["success"] is True
    
    def test_print_payload(self):
        ret = BasicReturn()
        ret.status = 10
        ret.message = "ok"
        ret.payload = {"success": True}
        assert str(ret) == "Retorno da função: test_return.test_print_payload\nStatus: 10\nMessage: ok\nPayload: {\n    \"success\": true\n}"
        
        ret.payload = "b64 of a image"
        assert str(ret) == "Retorno da função: test_return.test_print_payload\nStatus: 10\nMessage: ok\nPayload: b64 of a image"
        
        
        ret.print_payload = False
        ret.payload = {"something": 123}
        assert str(ret) == "Retorno da função: test_return.test_print_payload\nStatus: 10\nMessage: ok"
        
    def test_function_properties(self):
        def params_test_function(a, b, c=30, d=40, e=60):
            return BasicReturn()
        
        ret = params_test_function(10, 20, e=50)
        assert ret.owner == "test_return.params_test_function"
        assert ret.owner_args == "a=10, b=20, c=30, d=40, e=50"
        assert ret.owner_call == "params_test_function(a=10, b=20, c=30, d=40, e=50)"
        assert ret.file == "test_return"
        
    def test_function_properties_lists(self):
        def list_param_test_function(a):
            return BasicReturn()
        
        ret = list_param_test_function([1, 2, 3])
        assert ret.owner == "test_return.list_param_test_function"
        assert ret.owner_args == "a=[1, 2, 3]"
        assert ret.owner_call == "list_param_test_function(a=[1, 2, 3])"
        assert ret.file == "test_return"
        
    def test_function_properties_classes(self):
        class SomeClass: ...
        def class_param_test_function(a):
            return BasicReturn()
        
        ret = class_param_test_function(SomeClass())
        assert "SomeClass object" in ret.owner_args
        
            
        
    def test_wrong_status_type(self):
        ret = BasicReturn()
        with pytest.raises(ValueError):
            ret.status = "this should be an int or float"
        