# model.py
import uuid
from app import db
from datetime import datetime
from sqlalchemy.dialects.mysql import FLOAT


def gen_uuid():
    return uuid.uuid4().hex


def to_json(news_data):
    try:
        if isinstance(news_data, list):
            r = list()
            for item in news_data:
                r.append({c.name: getattr(item, c.name) for c in item.__table__.columns})
        else:
            r = {c.name: getattr(news_data, c.name) for c in news_data.__table__.columns}
    except AttributeError:
        return news_data
    return r


class FaceAll(db.Model):
    __bind_key__ = 'face_all'
    face_id = db.Column(db.String(32), default=gen_uuid, primary_key=True)  # UUID
    create_time = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.now, index=True)
    user_name = db.Column(db.String(5), unique=False, nullable=False, default='')
    rec = db.Column(db.Integer, unique=False, nullable=False, default=0)  # int 0 ~ 100
    clarity = db.Column(db.Integer, unique=False, nullable=False, default=0)  # int 0 ~ 无穷大
    status = db.Column(db.SmallInteger, nullable=False, default=0)  # 1：确认过Model，3：确认过Model但删除，2：照片出现多个人或质量差

    def file_name(self):
        return f"{self.face_id}_{self.create_time.strftime('%Y%m%d')}.jpg"

    def encodings(self):
        return sql_select(self.face_id)

    def __repr__(self):
        return '<face_all %r>' % self.user_name


class FaceEncodings(db.Model):
    __bind_key__ = 'face_encodings'
    face_id = db.Column(db.String(32), db.ForeignKey('face_all.face_id', ondelete="CASCADE"), primary_key=True)  # UUID
    f0 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f1 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f2 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f3 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f4 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f5 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f6 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f7 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f8 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f9 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f10 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f11 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f12 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f13 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f14 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f15 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f16 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f17 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f18 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f19 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f20 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f21 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f22 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f23 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f24 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f25 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f26 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f27 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f28 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f29 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f30 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f31 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f32 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f33 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f34 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f35 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f36 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f37 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f38 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f39 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f40 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f41 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f42 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f43 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f44 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f45 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f46 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f47 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f48 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f49 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f50 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f51 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f52 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f53 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f54 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f55 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f56 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f57 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f58 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f59 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f60 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f61 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f62 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f63 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f64 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f65 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f66 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f67 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f68 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f69 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f70 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f71 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f72 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f73 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f74 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f75 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f76 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f77 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f78 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f79 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f80 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f81 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f82 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f83 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f84 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f85 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f86 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f87 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f88 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f89 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f90 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f91 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f92 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f93 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f94 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f95 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f96 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f97 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f98 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f99 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f100 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f101 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f102 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f103 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f104 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f105 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f106 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f107 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f108 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f109 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f110 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f111 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f112 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f113 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f114 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f115 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f116 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f117 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f118 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f119 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f120 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f121 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f122 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f123 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f124 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f125 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f126 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)
    f127 = db.Column(FLOAT(precision=22, scale=20), nullable=False, default=0)

    def __repr__(self):
        return '<face_encodings %r>' % self.face_id


def sql_inset_encodings(face_id, encodings: list):
    fe = FaceEncodings.query.filter_by(face_id=face_id).first()
    if fe is None:
        db.session.add(FaceEncodings(
            face_id=face_id, f0=encodings[0], f1=encodings[1], f2=encodings[2], f3=encodings[3], f4=encodings[4],
            f5=encodings[5], f6=encodings[6], f7=encodings[7], f8=encodings[8], f9=encodings[9], f10=encodings[10],
            f11=encodings[11], f12=encodings[12], f13=encodings[13], f14=encodings[14], f15=encodings[15],
            f16=encodings[16], f17=encodings[17], f18=encodings[18], f19=encodings[19], f20=encodings[20],
            f21=encodings[21], f22=encodings[22], f23=encodings[23], f24=encodings[24], f25=encodings[25],
            f26=encodings[26], f27=encodings[27], f28=encodings[28], f29=encodings[29], f30=encodings[30],
            f31=encodings[31], f32=encodings[32], f33=encodings[33], f34=encodings[34], f35=encodings[35],
            f36=encodings[36], f37=encodings[37], f38=encodings[38], f39=encodings[39], f40=encodings[40],
            f41=encodings[41], f42=encodings[42], f43=encodings[43], f44=encodings[44], f45=encodings[45],
            f46=encodings[46], f47=encodings[47], f48=encodings[48], f49=encodings[49], f50=encodings[50],
            f51=encodings[51], f52=encodings[52], f53=encodings[53], f54=encodings[54], f55=encodings[55],
            f56=encodings[56], f57=encodings[57], f58=encodings[58], f59=encodings[59], f60=encodings[60],
            f61=encodings[61], f62=encodings[62], f63=encodings[63], f64=encodings[64], f65=encodings[65],
            f66=encodings[66], f67=encodings[67], f68=encodings[68], f69=encodings[69], f70=encodings[70],
            f71=encodings[71], f72=encodings[72], f73=encodings[73], f74=encodings[74], f75=encodings[75],
            f76=encodings[76], f77=encodings[77], f78=encodings[78], f79=encodings[79], f80=encodings[80],
            f81=encodings[81], f82=encodings[82], f83=encodings[83], f84=encodings[84], f85=encodings[85],
            f86=encodings[86], f87=encodings[87], f88=encodings[88], f89=encodings[89], f90=encodings[90],
            f91=encodings[91], f92=encodings[92], f93=encodings[93], f94=encodings[94], f95=encodings[95],
            f96=encodings[96], f97=encodings[97], f98=encodings[98], f99=encodings[99], f100=encodings[100],
            f101=encodings[101], f102=encodings[102], f103=encodings[103], f104=encodings[104], f105=encodings[105],
            f106=encodings[106], f107=encodings[107], f108=encodings[108], f109=encodings[109], f110=encodings[110],
            f111=encodings[111], f112=encodings[112], f113=encodings[113], f114=encodings[114], f115=encodings[115],
            f116=encodings[116], f117=encodings[117], f118=encodings[118], f119=encodings[119], f120=encodings[120],
            f121=encodings[121], f122=encodings[122], f123=encodings[123], f124=encodings[124], f125=encodings[125],
            f126=encodings[126], f127=encodings[127]
        ))
    else:
        fe.f0 = encodings[0]
        fe.f1 = encodings[1]
        fe.f2 = encodings[2]
        fe.f3 = encodings[3]
        fe.f4 = encodings[4]
        fe.f5 = encodings[5]
        fe.f6 = encodings[6]
        fe.f7 = encodings[7]
        fe.f8 = encodings[8]
        fe.f9 = encodings[9]
        fe.f10 = encodings[10]
        fe.f11 = encodings[11]
        fe.f12 = encodings[12]
        fe.f13 = encodings[13]
        fe.f14 = encodings[14]
        fe.f15 = encodings[15]
        fe.f16 = encodings[16]
        fe.f17 = encodings[17]
        fe.f18 = encodings[18]
        fe.f19 = encodings[19]
        fe.f20 = encodings[20]
        fe.f21 = encodings[21]
        fe.f22 = encodings[22]
        fe.f23 = encodings[23]
        fe.f24 = encodings[24]
        fe.f25 = encodings[25]
        fe.f26 = encodings[26]
        fe.f27 = encodings[27]
        fe.f28 = encodings[28]
        fe.f29 = encodings[29]
        fe.f30 = encodings[30]
        fe.f31 = encodings[31]
        fe.f32 = encodings[32]
        fe.f33 = encodings[33]
        fe.f34 = encodings[34]
        fe.f35 = encodings[35]
        fe.f36 = encodings[36]
        fe.f37 = encodings[37]
        fe.f38 = encodings[38]
        fe.f39 = encodings[39]
        fe.f40 = encodings[40]
        fe.f41 = encodings[41]
        fe.f42 = encodings[42]
        fe.f43 = encodings[43]
        fe.f44 = encodings[44]
        fe.f45 = encodings[45]
        fe.f46 = encodings[46]
        fe.f47 = encodings[47]
        fe.f48 = encodings[48]
        fe.f49 = encodings[49]
        fe.f50 = encodings[50]
        fe.f51 = encodings[51]
        fe.f52 = encodings[52]
        fe.f53 = encodings[53]
        fe.f54 = encodings[54]
        fe.f55 = encodings[55]
        fe.f56 = encodings[56]
        fe.f57 = encodings[57]
        fe.f58 = encodings[58]
        fe.f59 = encodings[59]
        fe.f60 = encodings[60]
        fe.f61 = encodings[61]
        fe.f62 = encodings[62]
        fe.f63 = encodings[63]
        fe.f64 = encodings[64]
        fe.f65 = encodings[65]
        fe.f66 = encodings[66]
        fe.f67 = encodings[67]
        fe.f68 = encodings[68]
        fe.f69 = encodings[69]
        fe.f70 = encodings[70]
        fe.f71 = encodings[71]
        fe.f72 = encodings[72]
        fe.f73 = encodings[73]
        fe.f74 = encodings[74]
        fe.f75 = encodings[75]
        fe.f76 = encodings[76]
        fe.f77 = encodings[77]
        fe.f78 = encodings[78]
        fe.f79 = encodings[79]
        fe.f80 = encodings[80]
        fe.f81 = encodings[81]
        fe.f82 = encodings[82]
        fe.f83 = encodings[83]
        fe.f84 = encodings[84]
        fe.f85 = encodings[85]
        fe.f86 = encodings[86]
        fe.f87 = encodings[87]
        fe.f88 = encodings[88]
        fe.f89 = encodings[89]
        fe.f90 = encodings[90]
        fe.f91 = encodings[91]
        fe.f92 = encodings[92]
        fe.f93 = encodings[93]
        fe.f94 = encodings[94]
        fe.f95 = encodings[95]
        fe.f96 = encodings[96]
        fe.f97 = encodings[97]
        fe.f98 = encodings[98]
        fe.f99 = encodings[99]
        fe.f100 = encodings[100]
        fe.f101 = encodings[101]
        fe.f102 = encodings[102]
        fe.f103 = encodings[103]
        fe.f104 = encodings[104]
        fe.f105 = encodings[105]
        fe.f106 = encodings[106]
        fe.f107 = encodings[107]
        fe.f108 = encodings[108]
        fe.f109 = encodings[109]
        fe.f110 = encodings[110]
        fe.f111 = encodings[111]
        fe.f112 = encodings[112]
        fe.f113 = encodings[113]
        fe.f114 = encodings[114]
        fe.f115 = encodings[115]
        fe.f116 = encodings[116]
        fe.f117 = encodings[117]
        fe.f118 = encodings[118]
        fe.f119 = encodings[119]
        fe.f120 = encodings[120]
        fe.f121 = encodings[121]
        fe.f122 = encodings[122]
        fe.f123 = encodings[123]
        fe.f124 = encodings[124]
        fe.f125 = encodings[125]
        fe.f126 = encodings[126]
        fe.f127 = encodings[127]
    db.session.commit()


def sql_inset_data(face_id, encodings: list, user_name='', rec=0, clarity=0, create_time=None, status=0):
    if create_time is None:
        create_time = datetime.now()
    fa = FaceAll.query.filter_by(face_id=face_id).first()
    if fa is None:
        db.session.add(FaceAll(
            face_id=face_id, create_time=create_time, user_name=user_name, status=status, rec=rec, clarity=clarity
        ))
    else:
        fa.create_time = create_time
        fa.user_name = user_name
        fa.status = status
        fa.rec = rec
        fa.clarity = clarity
    db.session.commit()
    sql_inset_encodings(face_id, encodings)


def sql_predict(encodings: list, limit=5):
    c = '+'.join([f'power({encodings[i]}-face_encodings.f{i},2)' for i in range(128)])
    d = f'SELECT face_all.face_id, face_all.user_name, MIN(sqrt({c})) AS dist FROM face_recognition.face_all LEFT JOIN face_recognition.face_encodings ON face_all.face_id=face_encodings.face_id WHERE face_all.`status` = 1 GROUP BY user_name ORDER BY dist LIMIT {limit}'
    return [list(item) for item in db.session.execute(d)]


def sql_select(face_id: str):
    fe = to_json(FaceEncodings.query.filter_by(face_id=face_id).first())
    if fe is None:
        return None
    return [fe[f'f{i}'] for i in range(128)]


if __name__ == '__main__':
    db.drop_all(bind=['face_all', 'face_encodings'])
    db.create_all(bind=['face_all', 'face_encodings'])
