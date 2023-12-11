from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://otrova:@localhost/FlaskAPI'
db = SQLAlchemy(app)

class ConfiguracaoCliente(db.Model):
    idCliente = db.Column(db.Integer, primary_key=True)
    idTipoLimite = db.Column(db.SmallInteger)
    idLimite = db.Column(db.SmallInteger)
    idInputCarteira = db.Column(db.SmallInteger)
    idConversao = db.Column(db.SmallInteger)
    valorBaseProprietaria = db.Column(db.Float)
    qtdDiasValidadeAnalise = db.Column(db.Integer)
    qtdDiasIntervaloMinimoAprovacoes = db.Column(db.Integer)
    qtdDiasIntervaloMaximoAprovacoes = db.Column(db.Integer)

class TiposRating(db.Model):
    idCliente = db.Column(db.Integer, db.ForeignKey('configuracao_cliente.idCliente'), primary_key=True)
    codigo = db.Column(db.String)
    descricao = db.Column(db.String)
    probDefaultInicial = db.Column(db.Float)
    probDefaultFinal = db.Column(db.Float)


# Use app.app_context() to create tables within the Flask application context
with app.app_context():
    # Create tables
    db.create_all()

# CRUD routes for ConfiguracaoCliente
@app.route('/configuracaocliente', methods=['GET', 'POST'])
def configuracao_cliente():
    if request.method == 'GET':
        configuracaocliente = ConfiguracaoCliente.query.all()
        return jsonify([{
            'idCliente': c.idCliente,
            'idTipoLimite': c.idTipoLimite,
            'idLimite': c.idLimite,
            'idInputCarteira': c.idInputCarteira,
            'idConversao': c.idConversao,
            'valorBaseProprietaria': c.valorBaseProprietaria,
            'qtdDiasValidadeAnalise': c.qtdDiasValidadeAnalise,
            'qtdDiasIntervaloMinimoAprovacoes': c.qtdDiasIntervaloMinimoAprovacoes,
            'qtdDiasIntervaloMaximoAprovacoes': c.qtdDiasIntervaloMaximoAprovacoes,
        } for c in configuracaocliente])
    elif request.method == 'POST':
        try:
            data = request.get_json()
            new_configuracao = ConfiguracaoCliente(**data)
            db.session.add(new_configuracao)
            db.session.commit()
            return jsonify({'message': 'ConfiguracaoCliente created successfully'}), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Duplicate key or invalid data'}), 400

# CRUD routes for TiposRating
@app.route('/tiposrating', methods=['GET', 'POST'])
def tipos_rating():
    if request.method == 'GET':
        tiposrating = TiposRating.query.all()
        return jsonify([{
            'idCliente': t.idCliente,
            'codigo': t.codigo,
            'descricao': t.descricao,
            'probDefaultInicial': t.probDefaultInicial,
            'probDefaultFinal': t.probDefaultFinal,
        } for t in tiposrating])
    elif request.method == 'POST':
        try:
            data = request.get_json()
            new_tiposrating = TiposRating(**data)
            db.session.add(new_tiposrating)
            db.session.commit()
            return jsonify({'message': 'TiposRating created successfully'}), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Duplicate key or invalid data'}), 400

if __name__ == '__main__':
    app.run(debug=True)
