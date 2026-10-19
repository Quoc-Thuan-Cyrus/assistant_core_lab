from assistant_core.router import route
from assistant_core.models import Intent

def test_route_greeting():
    assert route("Xin chao!", set()) == Intent.GREETING

def test_route_fee():
    assert route("How much is the tuition fee?", set()) == Intent.FEE

def test_route_office():
    assert route("Where is the library?", {"library", "academic affairs"}) == Intent.OFFICE

def test_route_rule():
    # Nếu không khớp cái nào ở trên, nó sẽ trả về RULE
    assert route("Tell me about thesis registration.", {"library"}) == Intent.RULE