"""
Quick test for UML diagram generation
Run: python test_uml_quick.py
"""
import asyncio
import sys
sys.path.insert(0, '.')

from app.core.uml_agent import get_uml_agent


async def test_uml_generation():
    """Test UML diagram generation with sample code."""
    
    # Sample Python code
    sample_code = """
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.orders = []
    
    def place_order(self, order):
        self.orders.append(order)
        order.assign_user(self)
        return order

class Order:
    def __init__(self, order_id, total):
        self.order_id = order_id
        self.total = total
        self.user = None
        self.items = []
    
    def assign_user(self, user):
        self.user = user
    
    def add_item(self, item):
        self.items.append(item)
        self.total += item.price

class OrderItem:
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price
"""
    
    print("=" * 60)
    print("UML DIAGRAM GENERATION TEST")
    print("=" * 60)
    
    try:
        agent = get_uml_agent()
        
        # Test 1: Auto-detect diagram types
        print("\n1. Detecting diagram types...")
        detected = agent.detect_diagram_types(sample_code, "python")
        print(f"   Detected: {detected}")
        
        # Test 2: Generate diagrams
        print("\n2. Generating UML diagrams...")
        diagrams = await agent.generate_diagrams(
            code=sample_code,
            language="python",
            diagram_types=["auto"]
        )
        
        print(f"\n   Generated {len(diagrams)} diagrams:")
        for i, diagram in enumerate(diagrams, 1):
            print(f"\n   Diagram {i}: {diagram['type']}")
            print(f"   Description: {diagram['description']}")
            print(f"   Mermaid code length: {len(diagram['mermaid_code'])} characters")
            print(f"\n   Preview:")
            print("   " + "\n   ".join(diagram['mermaid_code'].split('\n')[:10]))
            if len(diagram['mermaid_code'].split('\n')) > 10:
                print("   ...")
        
        print("\n" + "=" * 60)
        print("✅ TEST PASSED - UML generation successful!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_uml_generation())
