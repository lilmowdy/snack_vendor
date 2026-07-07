from app import create_app
from models import db, Vendor, MenuItem, Order, OrderItem

app = create_app()

with app.app_context():
    # delete order items first (foreign key dependencies)
    OrderItem.query.delete()
    Order.query.delete()
    
    # delete menu items and vendors created under wrong owner
    # keep only vendor id 3 (Mama Pima under correct account)
    # keep only vendor id 2 (Ghetto Smocha - check who owns it)
    
    bad_vendors = Vendor.query.filter(Vendor.id.in_([1, 2])).all()
    for v in bad_vendors:
        MenuItem.query.filter_by(vendor_id=v.id).delete()
        db.session.delete(v)
    
    db.session.commit()
    print("cleaned up. remaining vendors:")
    for v in Vendor.query.all():
        print(f"  id:{v.id} | {v.name} | owner_id:{v.owner_id}")
