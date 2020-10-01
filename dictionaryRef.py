
import json

# load tesaurus data
with open('source/tesaurus-master/dict.json') as file:
    tesaurus = json.load(file)

# keyword from (Philip R. Saver, 2002) and manual collections
init_dict = {
    'marah' : ['bosan','jenuh','cemburu','curiga','tinggi hati','iri','berdengki','dengki','gemas','geregetan',
         'ngambek','tersinggung','muak','benci','dendam','histeris','senewen','emosi','kesal','sebal','mangkel',
        'dongkol','jengkel','panas hati','kalap','murka','naik darah','naik pitam','marah','berang','geram'],
    'senang': ['bangga','kagum','asik','sukacita','sukaria','bahagia','senang','girang','gembira','ceria',
              'riang','damai','aman','tenteram','lega','kepuasan','puas','berani','yakin','ikhlas','tulus',
              'berbesar','besar hati','rendah hati','sabar','tabah'],
    'takut' : ['gentar','takut','berdebar','kebat-kebit','kalut','gusar','kecemasan','cemas','kawatir','waswas',
              'bimbang','bingung','galau','gundah','gelisah','risau'],
    'sedih' : ['kecil hati','malu','simpati','tersentuh','hard','keharuan','prihatin','iba','kasihan','murung',
              'pilu','sendu','sedih','duka','dukacita','sakit hati','pedih hati','patah hati','remuk hati',
              'frustasi','putus asa','putus harapan','berat hati','penyesal','sesal'],
    'percaya':['percaya','yakin','pasti','optimis','serius','bimbang','curiga','dubius','ragu','ragu-ragu',
              'rambang','sangsi','sinis','skeptis','surut','syak','ciut hati','pesimis','pesimistis',
              'tidak percaya','tidak yakin','sungguh-sungguh','sungguh'],
    'terkejut':['terkejut','wow','kejutan','kagum','takjub','terpukau','terpesona','heran','kaget','terperanjat',
               'kejut','terheran','terheran-heran','benarkah','tidak percaya','gila','luar biasa','mengejutkan',
               'astaga','tidak mungkin','demi tuhan','ya tuhan','serius','bercanda'],
    'jijik' : ['jijik','risih','benci','jelah','kesal','muak','pasai','sebal','bosan','jemu','jenuh','dengki',
              'ih','busuk','mesum','bejat','mengkal',],
    'antisipasi':['was-was','siap-siap','jaga-jaga','bersiap','persiapan','duga','dugaan','firasat','ramal',
                 'peramalan','kira','perkiraan','anggapan','praduga','prakiraan','sangka','prasangka',
                 'prediksi','rekaan','bayangan','kira kira','kirain']
}

# list words or phrase that didn't related to emotion class
exclude_dict = {
    'antisipasi': ['bisikan hati','faal','fenomena','gejala','perasaan (hati)','semboyan','melihat',
                    'memberitahukan','menceritakan','anggaran','citra','hemat','kesan','pikiran',],
    'jijik': ['berang','berkesan','bingit','salah','keki','sebal','bosan','langkah','kenyang',
              'masygul','jahat','buntung','mati','padat','khianat','mangkel','dendam','keji',
              'puas','dengki','keras','penuh','benci','gondok','gregetan'],
    'terkejut': ['jatuh cinta','kasmaran','tercantol','terpaut','terpikat','terpincut','tertambat',
                  'terpelet','tersirep','tertawan','miring','bermain-main','bertukar akal','bercumbu-cumbu',
                  'tersengsem','khusyuk','memikat','a heran','a ki gandrung','nomor satu','v bertuah',
                  ''],
    'percaya': ['galau','tetap'],
    'sedih': ['takut','kelompok','kerabang','kulit telur','kulit kerang','rumah','n aib','a dukacita','ngeri',
              'tersipu','mengirik','rawan','terawai','sipu','noda','afinitas','kekesalan','jengah','borok',
              ''],
    'marah': ['penuh','bingit','awas','berhati-hati','waspada','angkuh','arogan','besar','tersenggol',
               'tersentuh','a berputih mata','kecil','nek','berkesan','jijik','hati','jiwa','kalbu','perasaan',
               'apes','langkah','menyeleweng','menyempal','a durhaka','subversif','dengkul','sakit','membawang',
               'meraba','hangat','makan bawang','menepuk','kenyang','rambang','pampat','dogol','panik','jemu',
               'debek','jejap','hangus dada','buntung','menyangkak hati','padat','jaki','afeksi',
               'jelak','puas','murih','tumpat','membayang','telentung','silap','buntur','pekat','menceku',
               'bosan','jenuh'],
    'senang': ['angkuh','bagak','besar diri','besar','heran','takjub','tercengang','terpesona','silau',
                 'terpukau','bersih','kekuatan','kuasa','tenaga','jernih (suasana)','reda','sip',
                'terjaga','terjamin','terlindung','tersembunyi','meyakinkan','pasti','pada','plong',
                 'kenyang','nekat','nyali','benar benar percaya','bersungguhsungguh','betul-betul percaya',
                'kepala dingin','percaya','serius','tentu','tetap','jujur','lurus hati','mukhlis',
                'mustakim','tahan','aman','enak','rela','baik','sabar','yakin','kuat','kosong','benar-benar percaya',
                'daya','larat','kosen','kalis','kudus','bahaduri','kesatria'],
    'takut': ['a ki cabar','kecil','jengkel','kecil hati','keki','kesal','makan bawang','mangkel','marah',
               'masygul','membawang','mengkal','menyolot','meraba','meradang','murka','naik darah','naik pitam',
               'palak','sebal','sewot','tersinggung','hidup liar','merampang','bertualang','berang','bergerak',
               'gerak','menyangkak hati','nanar','gemas','berdesar','sesak','runsing','kembang tengkuk','gerah',
               'hampir-hampir','berkeliaran','hidup tanpa aturan','berwalang hati','samara','keruh','gondok',
               'hormat','hampir','rewel','gemang','']
}

# create new dictionary reference for emotion classification
result = {}
for key in init_dict:
    result[key] = []

    for item in init_dict[key]:
        try:
            result[key].extend(tesaurus[item]['sinonim'])
        except:
            pass
    result[key] = list(set(result[key]))
    result[key] = [word for word in result[key] if word not in exclude_dict[key]]
    result[key].extend([word for word in init_dict[key] if word not in exclude_dict[key]])

# save the dictionary into json file
with open('source/ref.json','w') as f:
    json.dump(result, f)