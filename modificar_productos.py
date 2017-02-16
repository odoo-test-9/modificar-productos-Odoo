import os
import csv
import xmlrpclib
import re


HOST='190.114.253.252'
PORT=8069
DB='db'
USER='falconsoft.3d@gmail.com'
PASS='1234567890'
url ='http://%s:%d/xmlrpc/' % (HOST,PORT)

common_proxy = xmlrpclib.ServerProxy(url+'common')
object_proxy = xmlrpclib.ServerProxy(url+'object')
uid = common_proxy.login(DB,USER,PASS)

def _create(estado):
    if estado is True:
        path_file = './ej.csv'
        archive = csv.DictReader(open(path_file))

        cont = 1
        # field['name'] captura valor del campo name solo si estas seguro
        # field.get('name', False) captura el valor  y devuelve el segundo
        for field in archive:
            print field
            vals = {'name': field['name1'],'list_price': field['price1']}
            do_write = object_proxy.execute(DB,uid,PASS,'product.template','create',vals)
            print  "se ha creado el producto %d descripcion %s" % (cont, object_proxy.execute(DB,uid,PASS,'product.template','read',[product_id],['name']))
            cont = cont + 1
            print "Contador:",cont

def _update(estado):
    if estado is True:
        path_file = './ej.csv'
        archive = csv.DictReader(open(path_file))

        cont = 1
        # field['name'] captura valor del campo name solo si estas seguro q vendra un valor en el diccionario
        # field.get('name', False) captura el valor  y devuelve el segundo parametro en caso de no encontar
        for field in archive:
            print field
            vals = field['price1']
            product = object_proxy.execute(DB,uid,PASS,'product.template','search',[('name','=',field['name1'])])
            product_id = product and product[0]
            do_write = object_proxy.execute(DB,uid,PASS,'product.template', 'write', product_id, {'list_price': vals })
            if do_write:
                print "OK:",cont
            cont = cont + 1
            print "Contador:",cont


def _update_mass(estado):
    if estado is True:
        cont = 1

        product = object_proxy.execute(DB,uid,PASS,'product.template','search',[('active','=',True)])
        code_du = object_proxy.execute(DB,uid,PASS,'account.account','search',[('code','=','630000')])

        for id in product:
            do_write = object_proxy.execute(DB,uid,PASS,'product.template', 'write',id, {'property_account_expense_id':code_du[0]})
            if do_write:
                print "OK:",cont
            cont = cont + 1
            print "Contador:",cont

def __main__():
    print 'Ha comenzado el proceso'
    _create(False)
    _update(True)
    _update_mass(True)
    print 'Ha finalizado la carga tabla'
__main__()
