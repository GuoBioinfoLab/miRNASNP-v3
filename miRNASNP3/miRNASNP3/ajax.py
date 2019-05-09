import flask_restful


from miRNASNP3 import app, api
from miRNASNP3.core import mongo

from flask_restful import Resource, fields, marshal_with, reqparse, marshal

gain_hit_info = {
    'mir_id':fields.String,
    'snp_id':fields.String,
    'utr3_pos':fields.String,
    'query':fields.String,
    'score':fields.String,
    'energy':fields.String,
    'utr_map_start':fields.String,
    'utr_map_end':fields.String,
    'effect':fields.String
}
hit_list = {
    'hit_list':fields.List(fields.Nested(gain_hit_info))
}

class GainHits(Resource):
    @marshal_with(hit_list)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('search_ids',type = str)
        args = parser.parse_args()
        if args['search_ids'] is None:
         #   gain_hit = {'mir_id': 'tmir', 'snp_id': 'tsnp', 'utr3_pos': 'tutr', 'query': 'tquery', 'score': 'tscore','energy': 'tenergy', 'utr_map_start':'0','utr_map_end':'0','effect': 'tgian'}
            return {'hit_list':None}
        if args['search_ids'].lower().startswith('hsa'):
            mir_id = args['search_ids']
            gain_hit = mongo.db.target_gain_test.find({'mir_id': mir_id})
        elif args['search_ids'].lower().startswith('mir'):
            mir_id = 'hsa'+args['search_ids']
            gain_hit = mongo.db.target_gain_test.find_one({'mir_id': mir_id})
        elif args['search_ids'].lower().startswith('rs'):
            snp_id = args['search_ids']
            gain_hit = mongo.db.target_gain_test.find({'snp_id': snp_id}).limit(10)
        else:
            symbol = args['search_ids']
            gain_hit ={'mir_id':'tmir','snp_id':'tsnp','utr3_pos':'tutr','query':'tquery','score':'tscore','energy':'tenergy','effect':'tgian'}
        #gain_hit['effect'] = 'gain'
        app.logger.debug("gain_hit={}".format(gain_hit))
        return {'hit_list':list(gain_hit)}


api.add_resource(GainHits, '/api/gain_hit')



'''
test_fields = {
    'fields1': fields.String,
    'fields2': fields.Integer,
    'fieldsx': fields.String(attribute='fields3'),
}


class FuzzyFoo(Resource):
    @marshal_with(test_fields)
    def get(self):
        a = {'fields1': 'abc', 'fields2': 1, 'fields3': 'ABC'}
        return a

api.add_resource(FuzzyFoo, '/api/test')


lncrna_snp_fields = {
    'chromosome': fields.String(attribute='chr'),
    'start': fields.Integer,
    'end': fields.Integer,
    'strand': fields.String,
    'lnc': fields.String,
    'snp': fields.String(attribute='dbsnp'),
    'ID': fields.Integer,
}

class LncRNASNP(Resource):
    @marshal_with(lncrna_snp_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ID', type=int)
        args = parser.parse_args()
        if args['ID']:
            lncrna_snp = mongo.db.SNP_lnc_relate.find_one({'ID': args['ID']})
        else:
            lncrna_snp = mongo.db.SNP_lnc_relate.find_one()
        app.logger.debug("lncrna_snp={}".format(lncrna_snp))
        return lncrna_snp

api.add_resource(LncRNASNP, '/api/lncrna_snp')


lncrna_snp_list_fields = {
    'lncrna_snp_list':  fields.List(fields.Nested(lncrna_snp_fields)),
    'records_number': fields.Integer
}

class LncRNASNPList(Resource):
    @marshal_with(lncrna_snp_list_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('per_page', type=int, default=30)
        parser.add_argument('lncrna')
        args = parser.parse_args()
        page = args['page']
        per_page = args['per_page']
        record_skip = (page - 1) * per_page
        condition = {}
        if args['lncrna']:
            condition = {"lnc": args['lncrna']}
        lncrna_snp_list = mongo.db.SNP_lnc_relate.find(condition).skip(record_skip).limit(per_page)
        records_number = mongo.db.SNP_lnc_relate.find().count()
        print("test")
        print(records_number)
        return {"lncrna_snp_sfs": 1,"records_number":records_number}
api.add_resource(LncRNASNPList, '/api/lncrna_snp_list')
'''