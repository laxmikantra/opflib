from collections import defaultdict, OrderedDict
from xmlprocessor.epub_xml_processor import ePubXMLProcessor as ePXP


class OPFProcessor(object):

    def __init__(self, opffile=None):
        self.opffile = opffile
        self.__opf_dict = defaultdict(dict)
        self.__manifest = defaultdict(dict)

    def read_opf(self):
        epxpobj = ePXP(self.opffile)
        self.__opf_dict = epxpobj.todict()

    def package(self):
        return self.__opf_dict.get('package')

    def opfns(self):
        return {key: value for key, value in  self.package().items()
                if key.startswith('@')}   

    def metadata(self):
        metadata  = self.package().get('metadata')
        meta = defaultdict(dict)
        for metakey, val in metadata.items():
            if isinstance(val, OrderedDict):
                meta[metakey] = val.get("#text")
            else:
                meta[metakey] = val
        return meta

    def manifest(self):
        manifest = self.package().get('manifest')
        for i in manifest.get('item'):
            self.__manifest.update({i.get('@id'): i})

    def spine(self):
        spine = self.package().get('spine')
        return spine.get('itemref')

    def item_ref(self):
        manifest = self.manifest()
        for item in self.spine():
            _id = item.get('@idref')
            yield {_id: self.__manifest.get(item.get('@idref'))}

    def pages(self):
        self.read_opf()
        for item in self.item_ref():
            for id, page_info in item.items():
                yield id, page_info.get('@href') 
            
if __name__ == '__main__':
    opf = "/home/sofycomps/work/input/accessible_epub/EPUB/package.opf"
    opfp = OPFProcessor(opf)
    for page in opfp.pages():
        print(page)
    
