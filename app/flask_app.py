from flask import Flask,jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

##app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://Gabriel14:@Gabriel14.mysql.pythonanywhere-services.com/Gabriel14$bdpythonapi'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost:3306/bdpythonapi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db= SQLAlchemy(app)
ma = Marshmallow(app)

#creacion de tabla categoria
class Categoria(db.Model):
    cat_id = db.Column(db.Integer,primary_key=True)
    cat_nom = db.Column(db.String(100))
    cat_desp = db.Column(db.String(100))

    def __init__(self,cat_nom,cat_desp):
        self.cat_nom= cat_nom
        self.cat_desp= cat_desp


db.create_all()


#schema categoria
class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('cat_id','cat_nom','cat_desp')


#una sola respuesta
categoria_schema = CategoriaSchema()


#cuando sean muchas respuesta
categorias_schema = CategoriaSchema(many=True)


#Get ######
@app.route('/categoria',methods=['GET'])
def get_categoria():
    all_categorias = Categoria.query.all()
    result = categorias_schema.dump(all_categorias)
    return jsonify(result)

#get X ID #####
@app.route('/categoria/<id>',methods=['GET'])
def get_categoria_x_id(id):
    una_categoria = Categoria.query.get(id)
    return categoria_schema.jsonify(una_categoria)


#POST ############
@app.route('/categoria',methods=['POST'])
def insert_categoria():
    data = request.get_json(force=True)
    cat_nom = data['cat_nom']
    cat_desp = data['cat_desp']

    nuevo_registro= Categoria(cat_nom,cat_desp)

    db.session.add(nuevo_registro)
    db.session.commit()
    return categoria_schema.jsonify(nuevo_registro)

##PUT update ########
@app.route('/categoria/<id>',methods=['PUT'])
def update_categoria(id):
    actualizar_categoria = Categoria.query.get(id)
    cat_nom = request.json['cat_nom']
    cat_desp = request.json['cat_desp']
    
    actualizar_categoria.cat_nom = cat_nom
    actualizar_categoria.cat_desp = cat_desp

    db.session.commit()

    return categoria_schema.jsonify(actualizar_categoria)


##DELETE ########
@app.route('/categoria/<id>',methods=['DELETE'])
def delete_categoria(id):
    eliminar_categoria = Categoria.query.get(id)
    db.session.delete(eliminar_categoria)
    db.session.commit()
    return categoria_schema.jsonify(eliminar_categoria)

#mensaje de bienvenida

@app.route('/',methods=['GET'])
def index():
    return jsonify({'Mensaje':'Bieeenvenido'})

if __name__=="__main__":
    app.run(debug=True)