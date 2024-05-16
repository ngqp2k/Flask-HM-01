from app import db


class InvoiceDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))
    invoice = db.relationship('Invoice', backref=db.backref('invoive_detail', lazy=True))
    description = db.Column(db.String(255))
    unit_price = db.Column(db.DECIMAL)
    qty = db.Column(db.Integer)
    amount = db.Column(db.DECIMAL)
    